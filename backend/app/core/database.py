import os
import sqlite3
import urllib.parse
from pathlib import Path
from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.core.config import settings

Base = declarative_base()

connect_args = {}
if settings.is_sqlite:
    connect_args["check_same_thread"] = False
else:
    if settings.DB_SSL_CA:
        connect_args["ssl"] = {"ca": settings.DB_SSL_CA}
    elif not settings.DB_SSL_DISABLED and any(provider in settings.DATABASE_URL.lower() for provider in ("render", "aiven", "tidb", "rds", "aws")):
        connect_args["ssl"] = {"ssl_mode": "REQUIRED"}

try:
    engine_kwargs = {
        "connect_args": connect_args,
        "pool_pre_ping": True,
    }
    if not settings.is_sqlite:
        engine_kwargs["pool_recycle"] = 3600
        engine_kwargs["pool_size"] = 10
        engine_kwargs["max_overflow"] = 20

    engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

    # Enable foreign keys enforcement for SQLite connections
    if settings.is_sqlite:
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"[Warning] Failed to initialize SQLAlchemy engine for {settings.sanitized_database_url}: {e}")
    engine = None
    SessionLocal = None

def get_db():
    if SessionLocal is None:
        raise RuntimeError(f"Database engine is not initialized. Please check connection to {settings.sanitized_database_url}")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_db_health() -> bool:
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"[HealthCheck] Database connection check failed for {settings.sanitized_database_url}: {e}")
        return False

check_db_connection = check_db_health

def check_database_status() -> int:
    """
    Checks database connectivity and initialization safely using read-only queries.
    Supports both SQLite and MySQL backends.
    Returns:
        0: Database exists and contains users table with existing records
        1: Connection failed (server unreachable / offline)
        2: Database does not exist / file not found
        3: Database exists but tables are missing or empty
    """
    if settings.is_sqlite:
        db_path = Path(settings.resolved_sqlite_path)
        if not db_path.exists():
            print(f"[Warning] SQLite database file not found at {db_path}")
            return 2
        try:
            conn = sqlite3.connect(db_path.as_posix(), timeout=5)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if not cur.fetchone():
                conn.close()
                return 3
            cur.execute("SELECT COUNT(*) FROM users")
            user_count = cur.fetchone()[0]
            conn.close()
            if user_count == 0:
                return 3
            print(f"[OK] SQLite database '{db_path.name}' verified ({user_count} users preserved).")
            return 0
        except Exception as e:
            print(f"[Error] SQLite database verification failed: {e}")
            return 1

    # MySQL Verification
    import pymysql
    host = settings.DB_HOST
    port = settings.DB_PORT
    user = settings.DB_USER
    password = settings.DB_PASSWORD
    dbname = settings.DB_NAME

    env_url = settings.DATABASE_URL
    if "://" in env_url:
        try:
            parsed = urllib.parse.urlparse(env_url)
            if parsed.hostname:
                host = parsed.hostname
            if parsed.port:
                port = parsed.port
            if parsed.username:
                user = urllib.parse.unquote(parsed.username)
            if parsed.password:
                password = urllib.parse.unquote(parsed.password)
            if parsed.path and len(parsed.path) > 1:
                dbname = parsed.path.lstrip("/").split("?")[0]
        except Exception:
            pass

    ssl_opts = None
    if settings.DB_SSL_CA:
        ssl_opts = {"ca": settings.DB_SSL_CA}

    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            ssl=ssl_opts,
            connect_timeout=5
        )
    except Exception as e:
        print(f"[Error] MySQL connection failed to {host}:{port}: {e}")
        return 1

    try:
        cur = conn.cursor()
        cur.execute("SHOW DATABASES LIKE %s", (dbname,))
        if not cur.fetchone():
            return 2

        cur.execute(f"USE `{dbname}`")
        cur.execute("SHOW TABLES LIKE 'users'")
        if not cur.fetchone():
            return 3

        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0]
        print(f"[OK] MySQL database '{dbname}' verified on {host}:{port} ({user_count} users preserved).")
        return 0
    except Exception as e:
        print(f"[Error] Database query check failed: {e}")
        return 1
    finally:
        try:
            conn.close()
        except Exception:
            pass

# Backward compatibility alias
check_mysql_status = check_database_status


