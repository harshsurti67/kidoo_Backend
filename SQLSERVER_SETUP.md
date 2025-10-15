# SQL Server Database Setup for KIDOO Django Project

This guide will help you connect your Django backend to the existing SQL Server database named "KIDOO".

## 📋 Prerequisites

### 1. SQL Server Requirements
- SQL Server 2012 or later
- SQL Server Authentication enabled
- Database "KIDOO" created and accessible
- User with appropriate permissions (read/write access)

### 2. ODBC Driver
Install **ODBC Driver 17 for SQL Server**:
- **Windows**: Download from [Microsoft's official page](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- **Linux**: Follow [Linux installation guide](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server)
- **macOS**: Follow [macOS installation guide](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos)

## 🚀 Setup Instructions

### Step 1: Install Required Packages

The required packages are already added to `requirements.txt`:
```bash
cd backend
pip install -r requirements.txt
```

This installs:
- `mssql-django==1.4` - Django backend for SQL Server
- `pyodbc==4.0.39` - Python ODBC driver

### Step 2: Configure Environment Variables

1. Copy the environment template:
```bash
cp env.example .env
```

2. Edit the `.env` file and configure your SQL Server settings:
```env
# Database Configuration
USE_SQLSERVER=True

# SQL Server Database Settings
DB_HOST=your_sql_server_host
DB_PORT=1433
DB_NAME=KIDOO
DB_USER=your_sqlserver_username
DB_PASSWORD=your_sqlserver_password
```

**Example configuration:**
```env
USE_SQLSERVER=True
DB_HOST=localhost
DB_PORT=1433
DB_NAME=KIDOO
DB_USER=kidoo_user
DB_PASSWORD=your_secure_password
```

### Step 3: Test Database Connection

Run the database connection test:
```bash
python test_db_connection.py
```

This script will:
- ✅ Verify Django configuration
- ✅ Test database connectivity
- ✅ Display SQL Server version information
- ✅ Show connected database name

### Step 4: Run Migrations

If the connection test passes, run Django migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)

Create an admin user for the Django admin panel:
```bash
python manage.py createsuperuser
```

## 🔧 Configuration Details

### Database Settings in `settings.py`

The Django settings automatically switch between SQLite and SQL Server based on the `USE_SQLSERVER` environment variable:

```python
if USE_SQLSERVER:
    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
                'extra_params': 'Trusted_Connection=no;Encrypt=yes;TrustServerCertificate=yes;'
            },
        }
    }
```

### Connection Options Explained

- `Trusted_Connection=no` - Use SQL Server authentication instead of Windows authentication
- `Encrypt=yes` - Enable encryption for the connection
- `TrustServerCertificate=yes` - Trust the server certificate (useful for development)

## 🐛 Troubleshooting

### Common Issues

#### 1. "Driver not found" Error
```
Error: [Microsoft][ODBC Driver Manager] Data source name not found
```
**Solution**: Install ODBC Driver 17 for SQL Server (see Prerequisites section)

#### 2. "Login failed" Error
```
Error: Login failed for user 'username'
```
**Solutions**:
- Verify username and password are correct
- Ensure SQL Server Authentication is enabled
- Check if the user has access to the KIDOO database
- Verify the user exists in SQL Server

#### 3. "Cannot connect to server" Error
```
Error: [Microsoft][ODBC Driver 17 for SQL Server]TCP Provider: No connection could be made
```
**Solutions**:
- Verify SQL Server is running
- Check if port 1433 is accessible
- Ensure SQL Server Browser service is running
- Check firewall settings

#### 4. "Database does not exist" Error
```
Error: Cannot open database "KIDOO"
```
**Solutions**:
- Create the KIDOO database in SQL Server
- Verify database name spelling
- Ensure the user has access to the database

### Testing Connection Manually

You can test the connection using the provided script:
```bash
python test_db_connection.py
```

The script provides detailed error messages and troubleshooting suggestions.

### SQL Server Configuration Checklist

- [ ] SQL Server is running
- [ ] SQL Server Authentication is enabled
- [ ] Database "KIDOO" exists
- [ ] User account exists with proper permissions
- [ ] ODBC Driver 17 is installed
- [ ] Port 1433 is accessible
- [ ] Firewall allows connections

## 🔄 Switching Between Databases

You can easily switch between SQLite and SQL Server by changing the `USE_SQLSERVER` variable in your `.env` file:

**For SQLite (default):**
```env
USE_SQLSERVER=False
```

**For SQL Server:**
```env
USE_SQLSERVER=True
```

## 📊 Database Schema

When you run migrations, Django will create the necessary tables in your KIDOO database. The existing models include:

- User management (Django's built-in auth)
- Program models
- Team member models
- FAQ models
- And more...

## 🚀 Running the Application

Once everything is configured:

1. Start the Django development server:
```bash
python manage.py runserver
```

2. Access the admin panel at: `http://localhost:8000/admin`

3. Access the API at: `http://localhost:8000/api/`

## 📞 Support

If you encounter issues:

1. Run the connection test: `python test_db_connection.py`
2. Check the troubleshooting section above
3. Verify your SQL Server configuration
4. Ensure all prerequisites are met

The connection test script provides detailed error messages and suggestions for common issues.
