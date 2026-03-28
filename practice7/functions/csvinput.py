import psycopg2
from config import load_config

def csv_insert_data():
    path = r'C:\Users\User\work\practice7\contacts.csv'
    sql = "COPY phonebook (username, phone) FROM STDIN WITH (FORMAT CSV, HEADER true);"
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
                with open('contacts.csv', 'r') as f:
                    next(f)
                    cur.copy_from(f, 'staging', sep=',', columns=('username', 'phone'))
                    cur.execute("INSERT INTO phonebook (username, phone) SELECT username, phone FROM staging ON CONFLICT (username) DO NOTHING;")
            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

csv_insert_data()