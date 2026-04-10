import psycopg2
from config import load_config

def create_table():
    """Create the phonebook table if it doesn't exist."""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        phone VARCHAR(20) NOT NULL
        );
        """
    )
    conn = None
    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        cur.execute(commands)
        conn.commit()
        cur.close()
        print("Table 'phonebook' is ready.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def ups():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    sql = """CALL upsert_u(%s, %s);"""
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (username, phone))

            # commit the changes to the database
            conn.commit()
            print(f"User {username} upserted successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def hz():
    print("Enter list of usernames and list of phones")
    print("Usernames: ", end="")
    u = input().split()
    print("Phones: ", end="")
    p = input().split()
    if len(u) != len(p):
        print("Error: number of usernames and phones must match.")
        return
    sql = "CALL loophz(%s, %s)"
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            conn.notices.clear()   # Clear any previous notices
            with conn.cursor() as cur:
                cur.execute("CALL loophz(%s, %s)", (u, p))
                conn.commit()
                # Print any notices raised during the call
                for notice in conn.notices:
                    print(notice.strip())

            # commit the changes to the database
            conn.commit()
            print(f"Lists inserted successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def delete_contact():
    print("Delete by (1) username or (2) phone? ")
    choice = input().strip()
    
    if choice == "1":
        username = input("Enter username: ").strip()
        sql = "CALL del_user(%s)"
        param = (username,)
    elif choice == "2":
        phone = input("Enter phone: ").strip()
        sql = "CALL del_user(%s)"
        param = (phone,)
    else:
        print("Invalid choice.")
        return

    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, param)
                conn.commit()
                print(f"User deleted succesfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def match_return():
    print("Write the username or phone part that you want to match.")
    a = input()
    sql = "SELECT * FROM records(%s) ORDER BY out_id"
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (a,))
                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
                else:
                    print("No matching contacts.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def pages():
    print("Write the limit of the returned query and how much offset you want it to be.")
    lim = int(input())
    offs = int(input())
    sql = "SELECT * FROM pagination(%s, %s) ORDER BY out_id"
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (lim, offs))
                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def main():
    while True:
        print("1. Create table\n2. upsert user\n3.Insert list of users and their phones \n4. delete contact \n5. Return matching records\n6. Paginated data\n7. Exit")
        try:
            a = int(input())
            if a == 1: create_table()
            elif a == 2: ups()
            elif a == 3: hz()
            elif a == 4: delete_contact()
            elif a == 5: match_return()
            elif a == 6: pages()
            elif a == 7: 
                return
            else: 
                print("Try again!")
                continue
        except ValueError:
            print("Please enter a number.")
        print("Would you like to continue? y/n")
        while (True):
            a = input()
            if (a == "y"):
                break
            elif (a == "n"): 
                print("Bye!")
                return
            else:
                print("Try again!")
        

main()
