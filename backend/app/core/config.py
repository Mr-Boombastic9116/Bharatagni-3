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
    def DATABASE_URL(self) -> str:
        # Check direct DATABASE_URL first (standard on Render and cloud DB providers)
        env_url = os.getenv("DATABASE_URL")
        if env_url:
            env_url = env_url.strip()
            # Normalize mysql:// or mysql2:// dialect to mysql+pymysql://
            if env_url.startswith("mysql://"):
                env_url = "mysql+pymysql://" + env_url[len("mysql://"):]
            elif env_url.startswith("mysql2://"):
                env_url = "mysql+pymysql://" + env_url[len("mysql2://"):]
            return env_url

        from urllib.parse import quote_plus
        user = quote_plus(self.DB_USER) if self.DB_USER else ""
        pw = f":{quote_plus(self.DB_PASSWORD)}" if self.DB_PASSWORD else ""
        return f"mysql+pymysql://{user}{pw}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"

    @property
    def sanitized_database_url(self) -> str:
        url = self.DATABASE_URL
        if "://" in url:
            proto, rest = url.split("://", 1)
            if "@" in rest:
                creds, host_part = rest.split("@", 1)
                user = creds.split(":", 1)[0] if ":" in creds else creds
                return f"{proto}://{user}:***@{host_part}"
        return url

settings = Settings()
