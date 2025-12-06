# Database Configuration - Quick Reference

## What Was Changed

### 1. **app/config.py** - Enhanced Configuration Loading
- Added validation for `DB_VENDOR` (must be 'postgres' or 'mysql')
- Added warning if `DB_PASS` is empty or not set
- Smart defaults for port based on vendor (5432 for Postgres, 3306 for MySQL)
- All environment variables use consistent `DB_*` naming

### 2. **app/db/db.py** - Improved Connection Handling
- **Before connection attempt**: Logs INFO message with connection parameters
  ```
  Attempting PostgreSQL connection: user=postgres, host=localhost, port=5432, database=olist
  ```
- **On success**: Logs DEBUG message confirming connection
- **On failure**: Logs ERROR with detailed info:
  - Vendor, host, port, database, user (NOT password)
  - Exception type and message
  - Raises `ConnectionError` with full context
- Added step 7 in docstring: Test connection before running Flask

### 3. **.env.example** - Comprehensive Documentation
- Clear sections for Postgres vs MySQL configuration
- 10-step development workflow with detailed instructions
- Troubleshooting section
- Emphasizes changing 'changeme' password
- Documents the new health check utility

### 4. **tools/test_db_connection.py** - New Health Check Utility
- Tests DB connection using same config as Flask app
- Shows connection parameters (vendor, host, port, db, user)
- Attempts connection and runs simple query
- Provides clear success/failure messages with troubleshooting steps
- Exit code 0 = success, 1 = failure

### 5. **tools/__init__.py** - Package Initialization
- Makes `tools/` a proper Python package
- Enables `python -m tools.test_db_connection` syntax

## How to Use

### Quick Start
1. **Set your database credentials** in `.env`:
   ```bash
   DB_VENDOR=postgres
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=olist
   DB_USER=postgres
   DB_PASS=your_actual_password  # Change this!
   ```

2. **Test the connection** (before running Flask):
   ```bash
   python -m tools.test_db_connection
   ```

3. **If test passes**, start Flask:
   ```bash
   flask run
   ```

### When You See Connection Errors

#### Error: "psycopg library not installed"
```bash
pip install 'psycopg[binary]>=3.0'
```

#### Error: "mysql-connector-python library not installed"
```bash
pip install mysql-connector-python
```

#### Error: "Connection failed... authentication failed"
- Check `DB_USER` and `DB_PASS` in `.env`
- Verify credentials with: `psql -U postgres -d olist` (for Postgres)

#### Error: "Connection failed... could not connect to server"
- Check if database server is running
- Verify `DB_HOST` and `DB_PORT` are correct
- For Postgres: `pg_ctl status` or check service
- For MySQL: `systemctl status mysql` or check service

#### Error: "database 'olist' does not exist"
```bash
# For Postgres:
psql -U postgres -c "CREATE DATABASE olist;"

# For MySQL:
mysql -u root -p -e "CREATE DATABASE olist;"
```

## Environment Variable Reference

All database configuration uses consistent `DB_*` naming:

| Variable | Description | Postgres Default | MySQL Default |
|----------|-------------|------------------|---------------|
| `DB_VENDOR` | Database type | `postgres` | `mysql` |
| `DB_HOST` | Server hostname | `localhost` | `localhost` |
| `DB_PORT` | Server port | `5432` | `3306` |
| `DB_NAME` | Database name | `olist` | `olist` |
| `DB_USER` | Username | `postgres` | `root` |
| `DB_PASS` | Password | *(empty)* | *(empty)* |

## Example Log Output

### Successful Connection (INFO level)
```
INFO:app.config:Attempting PostgreSQL connection: user=postgres, host=localhost, port=5432, database=olist
DEBUG:app.db.db:PostgreSQL connection successful
```

### Failed Connection (ERROR level)
```
INFO:app.config:Attempting PostgreSQL connection: user=postgres, host=localhost, port=5432, database=olist
ERROR:app.db.db:PostgreSQL connection failed - vendor=postgres, host=localhost, port=5432, database=olist, user=postgres. Error: OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
```

### Health Check Success
```
======================================================================
DATABASE CONNECTION TEST
======================================================================
Vendor:   postgres
Host:     localhost
Port:     5432
Database: olist
User:     postgres
----------------------------------------------------------------------
Attempting connection...

✓ Connection successful!

PostgreSQL version: PostgreSQL 15.3 on x86_64-pc-linux-gnu...

======================================================================
✓ Database connection test PASSED
======================================================================
```

### Health Check Failure
```
======================================================================
DATABASE CONNECTION TEST
======================================================================
Vendor:   postgres
Host:     localhost
Port:     5432
Database: olist
User:     postgres
----------------------------------------------------------------------
Attempting connection...

✗ Connection Error: PostgreSQL connection failed - vendor=postgres, host=localhost, port=5432, database=olist, user=postgres. Error: OperationalError: connection refused

Common causes:
  - Database server is not running
  - Incorrect host or port in .env
  - Database does not exist
  - Invalid credentials (username/password)
  - Firewall blocking the connection

Troubleshooting steps:
  1. Verify postgres server is running
  2. Check .env file has correct DB_HOST, DB_PORT, DB_NAME
  3. Verify DB_USER and DB_PASS are correct
  4. Create database if needed: CREATE DATABASE olist;

======================================================================
✗ Database connection test FAILED
======================================================================
```

## Troubleshooting Workflow

1. **Run health check first**:
   ```bash
   python -m tools.test_db_connection
   ```

2. **Check the output** - it will tell you:
   - What vendor/host/port/database it's trying to connect to
   - The specific error if it fails
   - Troubleshooting steps

3. **Common fixes**:
   - Server not running → Start Postgres/MySQL service
   - Wrong credentials → Update `.env` file
   - Database doesn't exist → Create it with `CREATE DATABASE olist;`
   - Driver not installed → `pip install psycopg[binary]` or `pip install mysql-connector-python`

4. **Once health check passes**, Flask should work fine

## Next Steps

1. Make sure your `.env` file has the correct password (not 'changeme')
2. Start your database server
3. Run `python -m tools.test_db_connection` to verify
4. Apply DDL scripts to create tables (if not done already)
5. Run ETL scripts to load data
6. Start Flask with `flask run`

---

**Note**: The `.env` file is gitignored, so your credentials stay private. Always use `.env.example` as a template and copy it to `.env` with your real credentials.
