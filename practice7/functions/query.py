import psycopg2
from config import load_config

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
query_data()