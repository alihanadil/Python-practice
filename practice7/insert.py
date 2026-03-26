import psycopg2
from config import load_config

def insert_data():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    sql = """INSERT INTO phonebook (username, phone) VALUES (%s, %s);"""
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (username, phone))

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

insert_data()