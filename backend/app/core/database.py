import urllib.parse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.core.config import settings

Base = declarative_base()

connect_args = {}
if settings.DB_SSL_CA:
    connect_args["ssl"] = {"ca": settings.DB_SSL_CA}
elif not settings.DB_SSL_DISABLED and any(provider in settings.DATABASE_URL.lower() for provider in ("render", "aiven", "tidb", "rds", "aws")):
    connect_args["ssl"] = {"ssl_mode": "REQUIRED"}

try:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=10,
        max_overflow=20
    )
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

def check_mysql_status() -> int:
    """
    Checks MySQL connectivity and database initialization safely using read-only queries.
    Returns:
        0: Database exists and contains users table with existing records
        1: MySQL connection failed (server unreachable / offline)
        2: Database does not exist
        3: Database exists but tables are missing
    """
    import pymysql
    
    # Extract connection parameters from DATABASE_URL if provided
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
        print(f"[OK] Database '{dbname}' verified on {host}:{port} ({user_count} users preserved).")
        return 0
    except Exception as e:
        print(f"[Error] Database query check failed: {e}")
        return 1
    finally:
        try:
            conn.close()
        except Exception:
            pass

