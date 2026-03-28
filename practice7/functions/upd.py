import psycopg2
from config import load_config


def update():
    print("what do you wanna update: Username or Phone? ")
    choice = input()
    # if (choice == "Username"): 
    #     print("Original: ")
    #     u1 = input()
    #     print("New: ")
    #     u2 = input()
    #     sql1 = """ UPDATE phonebook
    #             SET username = %s
    #             WHERE username = %s"""
    # if (choice == "Phone"): 
    #     print("Original: ")
    #     u1 = input()
    #     print("New: ")
    #     u2 = input()
    #     sql2 = """ UPDATE phonebook
    #             SET phone = %s
    #             WHERE phone = %s"""
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
                if (choice == "Phone"): 
                    print("Original: ", end="")
                    u1 = input()
                    print("New: ", end="")
                    u2 = input()
                    sql2 = """ UPDATE phonebook
                            SET phone = %s
                            WHERE phone = %s"""
                    cur.execute(sql2, (u2, u1))

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

update()