import mysql.connector
import sqlite3;

def create_database(name):
    conn = sqlite3.connect("output/"+name+".db")
    conn.close()

create_database("brocku_available_courses")

def create_table(name, table, columns):
    conn = sqlite3.connect("output/"+name+".db")
    cursor = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS `{n}` ".format(**{"n":table})
    query+="("
    for column in columns:
        query += " " + column + ","
    query = query[:-1]
    query+=")"

    cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()

def delete_all_rows(name, table):
    conn = sqlite3.connect("output/"+name+".db")

    cursor = conn.cursor()
    cursor.execute("DELETE FROM `{}`".format(table))
    conn.commit()
    cursor.close()
    conn.close()

def insert_row(name, table, columns, values):
    conn = sqlite3.connect("output/"+name+".db")

    cursor = conn.cursor()

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

    conn.commit()
    cursor.close()
    conn.close()

def query(query, name):
    conn = sqlite3.connect("output/"+name+".db")

    cursor = conn.cursor()

    cursor.execute(query)

    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result
