import os
import pytest
import tempfile
import sqlite3
from pathlib import Path
from backend.app.core.config import Settings
from backend.app.core.database import check_db_health, check_database_status

def test_missing_database_file_detected():
    """Verify check_database_status returns 2 and check_db_health fails when database file is missing."""
    custom_settings = Settings()
    custom_settings.DB_TYPE = "sqlite"
    custom_settings.SQLITE_DATABASE_PATH = "non_existent_dir/missing_bharatagri.db"
    
    # Check that status correctly reports file not found (code 2)
    # temporarily patch settings in database module
    import backend.app.core.database as db_mod
    orig_settings = db_mod.settings
    db_mod.settings = custom_settings
    try:
        status = check_database_status()
        assert status == 2, f"Expected status 2 for missing file, got {status}"
        assert check_db_health() is False, "check_db_health must be False when file is missing"
    finally:
        db_mod.settings = orig_settings

def test_empty_database_detected():
    """Verify check_database_status returns 3 (tables missing) for an empty SQLite file."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tf:
        temp_path = tf.name

    try:
        custom_settings = Settings()
        custom_settings.DB_TYPE = "sqlite"
        custom_settings.SQLITE_DATABASE_PATH = temp_path

        import backend.app.core.database as db_mod
        orig_settings = db_mod.settings
        db_mod.settings = custom_settings
        try:
            status = check_database_status()
            assert status == 3, f"Expected status 3 for empty file, got {status}"
            assert check_db_health() is False, "check_db_health must be False for empty SQLite file"
        finally:
            db_mod.settings = orig_settings
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_production_secret_enforcement():
    """Verify production requires a valid strong secret and rejects empty/insecure defaults."""
    # Test 1: Production with empty secret raises RuntimeError
    prod_settings_empty = Settings()
    prod_settings_empty.ENVIRONMENT = "production"
    
    # Save original env
    orig_secret = os.environ.get("SECRET_KEY")
    try:
        os.environ["SECRET_KEY"] = ""
        with pytest.raises(RuntimeError) as exc_info:
            _ = prod_settings_empty.SECRET_KEY
        assert "Production security violation" in str(exc_info.value)

        # Test 2: Production with insecure default raises RuntimeError
        os.environ["SECRET_KEY"] = "bharatagri_secure_jwt_secret_key_2026_iteration2"
        with pytest.raises(RuntimeError) as exc_info:
            _ = prod_settings_empty.SECRET_KEY
        assert "Production security violation" in str(exc_info.value)

        # Test 3: Production with valid strong 32+ character key succeeds
        strong_key = "a" * 64
        os.environ["SECRET_KEY"] = strong_key
        assert prod_settings_empty.SECRET_KEY == strong_key

    finally:
        if orig_secret is not None:
            os.environ["SECRET_KEY"] = orig_secret
        else:
            os.environ.pop("SECRET_KEY", None)

def test_development_ephemeral_secret_fallback():
    """Verify development mode generates a secure ephemeral secret when unset."""
    dev_settings = Settings()
    dev_settings.ENVIRONMENT = "development"
    
    orig_secret = os.environ.get("SECRET_KEY")
    try:
        os.environ["SECRET_KEY"] = ""
        key1 = dev_settings.SECRET_KEY
        assert len(key1) >= 32, "Ephemeral dev key must be at least 32 characters"
        key2 = dev_settings.SECRET_KEY
        assert key1 == key2, "Ephemeral dev key must remain stable across instance calls"
    finally:
        if orig_secret is not None:
            os.environ["SECRET_KEY"] = orig_secret
        else:
            os.environ.pop("SECRET_KEY", None)
