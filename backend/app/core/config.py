import os
from pathlib import Path
from dotenv import load_dotenv

# Search for .env in project root or current working dir
root_dir = Path(__file__).resolve().parent.parent.parent.parent
env_path = root_dir / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "BharatAgri Iteration 3 API")
    VERSION: str = "3.0.0"
    API_V1_STR: str = "/api"

    # Database Type Selection: "sqlite" (default for self-contained Render prototype) or "mysql"
    DB_TYPE: str = os.getenv("DB_TYPE", "sqlite").lower()
    SQLITE_DATABASE_PATH: str = os.getenv("SQLITE_DATABASE_PATH", "")

    # MySQL Configuration (Retained for seamless dual-database support and rollback)
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "bharatagri_iteration2")
    DB_SSL_CA: str = os.getenv("DB_SSL_CA", "")
    DB_SSL_DISABLED: bool = os.getenv("DB_SSL_DISABLED", "").lower() in ("true", "1", "yes")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "bharatagri_secure_jwt_secret_key_2026_iteration2")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))
    PORT: int = int(os.getenv("PORT", 5000))
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "")

    @property
    def is_sqlite(self) -> bool:
        url = self.DATABASE_URL
        return url.startswith("sqlite")

    @property
    def resolved_sqlite_path(self) -> str:
        if self.SQLITE_DATABASE_PATH:
            return Path(self.SQLITE_DATABASE_PATH).resolve().as_posix()
        default_db = root_dir / "database" / "bharatagri.db"
        return default_db.resolve().as_posix()

    @property
    def DATABASE_URL(self) -> str:
        # 1. Direct DATABASE_URL environment variable has highest precedence
        env_url = os.getenv("DATABASE_URL")
        if env_url:
            env_url = env_url.strip()
            if env_url.startswith("mysql://"):
                return "mysql+pymysql://" + env_url[len("mysql://"):]
            elif env_url.startswith("mysql2://"):
                return "mysql+pymysql://" + env_url[len("mysql2://"):]
            return env_url

        # 2. If SQLITE_DATABASE_PATH is set or DB_TYPE is sqlite, use SQLite
        if self.SQLITE_DATABASE_PATH or self.DB_TYPE == "sqlite":
            return f"sqlite:///{self.resolved_sqlite_path}"

        # 3. Otherwise build MySQL URL from discrete parameters
        from urllib.parse import quote_plus
        user = quote_plus(self.DB_USER) if self.DB_USER else ""
        pw = f":{quote_plus(self.DB_PASSWORD)}" if self.DB_PASSWORD else ""
        return f"mysql+pymysql://{user}{pw}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"

    @property
    def sanitized_database_url(self) -> str:
        url = self.DATABASE_URL
        if url.startswith("sqlite"):
            return f"sqlite:///{Path(self.resolved_sqlite_path).name}"
        if "://" in url:
            proto, rest = url.split("://", 1)
            if "@" in rest:
                creds, host_part = rest.split("@", 1)
                user = creds.split(":", 1)[0] if ":" in creds else creds
                return f"{proto}://{user}:***@{host_part}"
        return url

settings = Settings()
