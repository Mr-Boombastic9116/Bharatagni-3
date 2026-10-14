# Absolute Database & Data Preservation Rules

This document outlines the strict operational and programmatic safeguards implemented in **BharatAgri-3** to guarantee zero data loss, zero table modification, and complete preservation of all existing records.

---

## 1. High-Priority Preservation Policy

BharatAgri Iteration 3 connects to an authoritative MySQL database containing **58 tables and tens of thousands of active agricultural, financial, and operational records**.

### Strictly Prohibited Operations
Under no circumstances may any code, startup script, CLI tool, or automated procedure execute:
- `DROP DATABASE` or `DROP TABLE`
- `TRUNCATE TABLE`
- `DELETE FROM` statements designed to purge records
- Destructive migrations, schema rollbacks, or column type reductions
- Automatic table recreation via ORM startup hooks (`create_all()` / `drop_all()`)
- Automatic database replacement or silent fallback to SQLite, in-memory, or dummy databases
- Seed scripts that overwrite existing users, roles, farmers, or credentials
- Resetting existing passwords, password hashes, or role permissions

---

## 2. Implemented Code Safeguards

### A. Non-Destructive Application Startup
In `backend/app/main.py`:
- The application startup event executes a **read-only** connectivity check (`SELECT 1`).
- No DDL statements (`CREATE`, `ALTER`, `DROP`) are executed during application bootstrap.
- If the database is unreachable, the API marks its database health as degraded and returns descriptive HTTP 503 errors on database-dependent routes. It **never** silently swaps in an empty database.

### B. Safe Connection Lifecycle & Error Handling
In `backend/app/core/database.py`:
- Connection pooling is configured with `pool_pre_ping=True` and `pool_recycle=3600` to prevent stale connection exceptions without dropping or altering sessions.
- Credentials, passwords, and sensitive connection strings are masked using `settings.sanitized_database_url` (e.g., `mysql+pymysql://root:***@localhost:3306/bharatagri_iteration2`).
- The `check_mysql_status()` utility executes only `SHOW DATABASES`, `SHOW TABLES`, and `SELECT COUNT(*)`, returning diagnostic codes without making modifications.

### C. Hardened Startup Launchers
In `start.bat` and `start-local.sh`:
- Automatic piping of `database/bharatagri_iteration2.sql` has been **completely removed**.
- If a configured database does not exist or has missing tables, the launcher outputs a clear warning advising manual verification rather than destroying or recreating data.

---

## 3. Safe Database Backup Protocol

To create a non-destructive point-in-time snapshot before testing or deploying:

```bash
# Export schema and data safely using single-transaction (InnoDB consistent read)
mysqldump -h <DB_HOST> -P <DB_PORT> -u <DB_USER> -p \
  --single-transaction \
  --quick \
  --skip-lock-tables \
  --routines \
  --triggers \
  bharatagri_iteration2 > backup_bharatagri_$(date +%Y%m%d_%H%M%S).sql
```

> **IMPORTANT**: Never commit SQL backup files, database dumps, or credentials into the public Git repository.

---

## 4. Verification Checklist Before Deployment

- [x] Verify `DATABASE_URL` or `DB_HOST` in environment points to the intended existing database.
- [x] Confirm no `DROP TABLE` commands exist in startup sequences.
- [x] Confirm no seed scripts are triggered by web service start commands.
- [x] Verify table counts: Live database should contain all 58 core tables.
- [x] Verify record counts: `users` (~5,052), `farmers` (~5,011), `bookings` (~19,046).
