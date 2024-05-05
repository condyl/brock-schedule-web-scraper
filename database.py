import mysql.connector

def create_database(name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS `{}`".format(name))
    mydb.commit()
    cursor.close()
    mydb.close()

def create_table(database, table, columns):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=database
    )
    cursor = mydb.cursor()
    query = "CREATE TABLE IF NOT EXISTS `{n}` ".format(**{"n":table})
    query+="("
    for column in columns:
        query += " " + column + ","
    query = query[:-1]
    query+=")"

    cursor.execute(query)

    mydb.commit()
    cursor.close()
    mydb.close()

def delete_all_rows(database, table):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=database
    )

    cursor = mydb.cursor()
    cursor.execute("DELETE FROM `{}`".format(table))
    mydb.commit()
    cursor.close()
    mydb.close()

def insert_row(database, table, columns, values):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=database
    )

    cursor = mydb.cursor()

    query = "INSERT INTO `{n}` ".format(**{"n":table})
    query+="("
    for column in columns:
        query += " " + column + ","
    query = query[:-1]
    query+=")"

    query += " VALUES "

    query+="("
    for value in values:
        query += ' "' + value + '",'
    query = query[:-1]
    query+=")"

    cursor.execute(query)

    mydb.commit()
    cursor.close()
    mydb.close()

def query(query, database):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=database
    )

    cursor = mydb.cursor()

    cursor.execute(query)

    result = cursor.fetchall()
    mydb.commit()
    cursor.close()
    mydb.close()
    return result
