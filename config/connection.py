import pymysql

host = "mysql56"
port = 3306
username = "root"
password = "admin1234"
database = "db_training"

def get_connection():
    return pymysql.connect(
        host,
        username,
        password,
        database,
        port
    )