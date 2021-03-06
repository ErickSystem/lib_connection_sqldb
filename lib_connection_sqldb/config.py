"""Default constants"""

# RELATIONAL DATABASE
MYSQL_DATABASE_SERVER = '127.0.0.1'
MYSQL_DATABASE_PORT = 3306
MYSQL_DATABASE_USERNAME = 'root'
MYSQL_DATABASE_PASSWORD = 'abc123'
MYSQL_DATABASE_DATABASE = 'test'

MYSQL_DATABASE_CONN = {
    'drivername': 'mysql+pymysql',
    'host': MYSQL_DATABASE_SERVER,
    'port': MYSQL_DATABASE_PORT,
    'username': MYSQL_DATABASE_USERNAME,
    'password': MYSQL_DATABASE_PASSWORD,
    'database': MYSQL_DATABASE_DATABASE
}

# RELATIONAL DATABASE SQL SERVER
SQLSERVER_DATABASE_SERVER = '127.0.0.1'
SQLSERVER_DATABASE_PORT = 1433
SQLSERVER_DATABASE_USERNAME = 'root'
SQLSERVER_DATABASE_PASSWORD = 'root'
SQLSERVER_DATABASE_DATABASE = 'test'

SQLSERVER_DATABASE_CONN = {
    'drivername': 'mssql+pymssql',
    'host': SQLSERVER_DATABASE_SERVER,
    'port': SQLSERVER_DATABASE_PORT,
    'username': SQLSERVER_DATABASE_USERNAME,
    'password': SQLSERVER_DATABASE_PASSWORD,
    'database': SQLSERVER_DATABASE_DATABASE
}
