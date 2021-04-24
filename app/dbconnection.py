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

def find_table(table):
    cursor.execute(f"SELECT * FROM {table}")
    result = cursor.fetchall()
    try:
        return result
    except Exception as e:
        pass


def find_column(table, column):
    cursor.execute(f"SELECT {column} FROM {table}")
    result = cursor.fetchall()
    try:
        return result
    except Exception as e:
        pass


def find_row(table, parameter_name, parameter_value):
    cursor.execute(f"SELECT * FROM {table} WHERE {parameter_name} = '{parameter_value}'")
    result = cursor.fetchall()
    try:
        return result
    except Exception as e:
        pass


def find_parameter(table, column, parameter_name, parameter_value):
    cursor.execute(f"SELECT {column} FROM {table} WHERE {parameter_name} = '{parameter_value}'")
    result = cursor.fetchall()[0]
    try:
        return result[0]
    except Exception as e:
        pass


def update_parameter(table, column, parameter_name, parameter_value, new_value):
    sql_query = f"UPDATE {table} SET {column} = '{new_value}' WHERE {parameter_name} = '{parameter_value}'"
    try:
        cursor.execute(sql_query)
        link.commit()
    except Exception as e:
        pass


def insert_account(parameter_values):
    sql_query = f"INSERT INTO konta (login, haslo, uprawnienia, imie, nazwisko) VALUES ('{parameter_values[0]}', " \
                f"'{parameter_values[1]}', {0}, '{parameter_values[2]}', '{parameter_values[3]}')"
    try:
        cursor.execute(sql_query)
        link.commit()
    except Exception as e:
        pass


def insert_planned_service(data):
    sql_query = f"INSERT INTO usluga (id_firmy, id_rodzaju, data, czas, status) VALUES ({data[0]}, " \
                f"{data[1]}, '{data[2]}', {data[3]}, {data[4]})"
    try:
        cursor.execute(sql_query)
        link.commit()
    except Exception as e:
        pass
