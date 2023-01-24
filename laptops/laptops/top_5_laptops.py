import sqlite3
from sqlite3 import Error
import os


def create_connection(db_file):
    con = None
    try:
        con = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return con


def select_top_5_laptops(con):
    cur = con.cursor()
    cur.execute("SELECT url FROM laptops ORDER BY rank DESC LIMIT 5")

    rows = cur.fetchall()
    for row in rows:
        print(row)


def main():
    database = os.path.join(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
            ), 'laptops.db'
        )
    con = create_connection(database)

    with con:
        select_top_5_laptops(con)


if __name__ == '__main__':
    main()
