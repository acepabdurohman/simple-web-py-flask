import pymysql

host = "localhost"
username = "root"
password = "admin1234"
database = "db_training"

def get_connection():
    return pymysql.connect(
        host,
        username,
        password,
        database
    )