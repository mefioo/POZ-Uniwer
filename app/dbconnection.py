import mysql.connector
import string

config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '3306',
    'database': 'poz_uniwer',
    'raise_on_warnings': True,
}

link = mysql.connector.connect(**config)
cursor = link.cursor(buffered=True)

def find_and_return_by_table(table):
    cursor.execute(f"SELECT * FROM {table}")
    result = cursor.fetchall()
    try:
        return result
    except Exception as e:
        pass
