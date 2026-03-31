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

def insert_data():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    sql = """INSERT INTO phonebook (username, phone) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING;"""
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

def csv_insert_data():
    print("Input the csv path")
    path = input()
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.execute("""
                    CREATE TEMP TABLE staging (
                        username VARCHAR(50),
                        phone VARCHAR(20)
                    ) ON COMMIT DROP;
                """)
                with open(path, 'r') as f:
                    print("does your csv file have header? y/n")
                    c = input()
                    if (c == 'y'): next(f)
                    cur.copy_from(f, 'staging', sep=',', columns=('username', 'phone'))
                    cur.execute("INSERT INTO phonebook (username, phone) SELECT username, phone FROM staging ON CONFLICT (username) DO NOTHING;")
            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def update():
    print("what do you wanna update: Username or Phone? ")
    choice = input()
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                if (choice == "Username"): 
                    print("Original: ", end="")
                    u1 = input()
                    print("New: ", end="")
                    u2 = input()
                    sql1 = """ UPDATE phonebook
                            SET username = %s
                            WHERE username = %s"""
                    cur.execute(sql1, (u2, u1))
                    if cur.rowcount > 0:
                        print("Update successful.")
                    else:
                        print("No matching record found.")
                if (choice == "Phone"): 
                    print("Original: ", end="")
                    u1 = input()
                    print("New: ", end="")
                    u2 = input()
                    sql2 = """ UPDATE phonebook
                            SET phone = %s
                            WHERE phone = %s"""
                    cur.execute(sql2, (u2, u1))
                    if cur.rowcount > 0:
                        print("Update successful.")
                    else:
                        print("No matching record found.")
                

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def query_data():
    print("How do you want to filter your data? By name or by phone prefix? ", end="")
    choice = input().strip().lower()

    if choice not in ["name", "phone prefix"]:
        print("Invalid choice.")
        return

    if choice == "name":
        print("Write the name (or part of it): ", end="")
        value = input().strip()
        # Use ILIKE for case‑insensitive partial match (contains)
        pattern = f"%{value}%"
        sql = "SELECT * FROM phonebook WHERE username ILIKE %s ORDER BY username;"
    else:  # phone prefix
        print("Write the phone prefix: ", end="")
        value = input().strip()
        # Match numbers starting with the given prefix
        pattern = f"{value}%"
        sql = "SELECT * FROM phonebook WHERE phone LIKE %s ORDER BY phone;"

    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (pattern,))
                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
                else:
                    print("No matching contacts.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def delete_contact():
    print("Delete by (1) username or (2) phone? ")
    choice = input().strip()
    
    if choice == "1":
        username = input("Enter username: ").strip()
        sql = "DELETE FROM phonebook WHERE username = %s"
        param = (username,)
    elif choice == "2":
        phone = input("Enter phone: ").strip()
        sql = "DELETE FROM phonebook WHERE phone = %s"
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
                print(f"Deleted {cur.rowcount} contact(s).")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def main():
    while True:
        print("1. Create table\n2. Insert CSV\n3. Insert console\n4. Update\n5. Query\n6. Delete\n7. Exit")
        try:
            a = int(input())
            if a == 1: create_table()
            elif a == 2: csv_insert_data()
            elif a == 3: insert_data()
            elif a == 4: update()
            elif a == 5: query_data()
            elif a == 6: delete_contact()
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

# To reset the auto‑increment sequence so that new rows receive the next consecutive ID 
# after the current maximum, you can use the following SQL command:

# SELECT setval('phonebook_id_seq', (SELECT COALESCE(MAX(id), 0) FROM phonebook));