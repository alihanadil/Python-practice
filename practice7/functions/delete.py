import psycopg2
from config import load_config

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

delete_contact()