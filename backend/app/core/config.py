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

    # Environment mode: 'production', 'development', or 'test'
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production" if os.getenv("RENDER") else "development").lower()

    _INSECURE_SECRETS = {
        "bharatagri_secure_jwt_secret_key_2026_iteration2",
        "your_secure_jwt_random_secret_key_change_in_production",
        "secret",
        "change_me",
        "default_secret"
    }

    @property
    def SECRET_KEY(self) -> str:
        env_secret = os.getenv("SECRET_KEY", "").strip()
        if self.ENVIRONMENT == "production":
            if not env_secret or env_secret in self._INSECURE_SECRETS or len(env_secret) < 32:
                raise RuntimeError(
                    "Production security violation: SECRET_KEY is missing, too short (<32 chars), or using an insecure default. "
                    "You must supply a strong SECRET_KEY in production environment variables (e.g., Render 'generateValue: true' or 'openssl rand -hex 32')."
                )
            return env_secret
        
        # Development / Test mode
        if env_secret and env_secret not in self._INSECURE_SECRETS:
            return env_secret
        
        if not hasattr(self, "_ephemeral_secret"):
            import secrets
            self._ephemeral_secret = secrets.token_hex(32)
        return self._ephemeral_secret

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
        raw_path = (self.SQLITE_DATABASE_PATH or "").strip()
        if raw_path:
            p = Path(raw_path)
            if not p.is_absolute():
                p = (root_dir / p).resolve()
            else:
                p = p.resolve()
        else:
            p = (root_dir / "database" / "bharatagri.db").resolve()
        return p.as_posix()

    @property
    def DATABASE_URL(self) -> str:
        # If DB_TYPE is explicitly 'sqlite' or SQLITE_DATABASE_PATH is provided:
        if self.DB_TYPE == "sqlite" or self.SQLITE_DATABASE_PATH:
            env_url = (os.getenv("DATABASE_URL") or "").strip()
            # If an explicit SQLite DATABASE_URL was provided, resolve its path accurately
            if env_url.startswith("sqlite"):
                raw = env_url
                for prefix in ("sqlite:///", "sqlite://"):
                    if raw.startswith(prefix):
                        raw = raw[len(prefix):]
                        break
                if raw:
                    p = Path(raw)
                    if not p.is_absolute():
                        p = (root_dir / p).resolve()
                    else:
                        p = p.resolve()
                    p.parent.mkdir(parents=True, exist_ok=True)
                    return f"sqlite:///{p.as_posix()}"

            # Use resolved_sqlite_path and ensure its parent directory exists
            p = Path(self.resolved_sqlite_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            return f"sqlite:///{p.as_posix()}"

        # Otherwise, MySQL mode: check DATABASE_URL first
        env_url = (os.getenv("DATABASE_URL") or "").strip()
        if env_url:
            if env_url.startswith("mysql://"):
                return "mysql+pymysql://" + env_url[len("mysql://"):]
            elif env_url.startswith("mysql2://"):
                return "mysql+pymysql://" + env_url[len("mysql2://"):]
            return env_url

        # Otherwise build MySQL URL from discrete parameters
        from urllib.parse import quote_plus
        user = quote_plus(self.DB_USER) if self.DB_USER else ""
        pw = f":{quote_plus(self.DB_PASSWORD)}" if self.DB_PASSWORD else ""
        return f"mysql+pymysql://{user}{pw}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"

    @property
    def sanitized_database_url(self) -> str:
        url = self.DATABASE_URL
        if url.startswith("sqlite"):
            # Expose the full resolved SQLite URL in logs so the exact file path is transparent
            return url
        if "://" in url:
            proto, rest = url.split("://", 1)
            if "@" in rest:
                creds, host_part = rest.split("@", 1)
                user = creds.split(":", 1)[0] if ":" in creds else creds
                return f"{proto}://{user}:***@{host_part}"
        return url

settings = Settings()
