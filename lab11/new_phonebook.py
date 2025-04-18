import psycopg2
import csv


conn = psycopg2.connect(
    host="localhost",
    dbname="mydatabase",
    user="postgres",
    password="Nurassyl1948"
)
cur = conn.cursor()


def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            phone VARCHAR(20) UNIQUE
        );
    """)
    conn.commit()

def insert_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()

def add_or_update():
    p_name = input("Enter name: ")
    p_phone = input("Enter phone: ")
    cur.execute(f"CALL add_or_update('{p_name}','{p_phone}')")


def insert_from_console():
    first_name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (first_name, phone))
    conn.commit()

def search_by_pattern():
    print("1.Starts with a letter")
    print("2.Exactly n-letter names ")
    pattern = int(input("Choose pattern: "))

    if pattern == 1:
        first_letter = input("First letter: ").upper()
        cur.execute(f"SELECT * FROM phonebook WHERE first_name LIKE '{first_letter}%' ")

        for row in cur.fetchall():
            print(row[1])
    elif pattern == 2:
        length = int(input("How many letters it must have: "))
        symbol = ""
        for i in range(length):
            symbol += "_"
        cur.execute(f"SELECT * FROM phonebook WHERE first_name LIKE '{symbol}'")

        for row in cur.fetchall():
            print(row[1])


def update_user():
    phone_or_name = input("Update by (phone or name)? ").lower()
    if phone_or_name == "phone":
        phone = input("Enter existing phone: ")
        new_name = input("New name: ")
        cur.execute("UPDATE phonebook SET first_name = %s WHERE phone = %s", (new_name, phone))
    else:
        name = input("Enter existing name: ")
        new_phone = input("New phone: ")
        cur.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s", (new_phone, name))
    conn.commit()


def query_data():
    keyword = input("Search for name or phone: ")
    cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s OR phone ILIKE %s", (f"%{keyword}%", f"%{keyword}%"))
    for row in cur.fetchall():
        print(row)


def delete_user():
    by = input("Delete by (name or phone)? ").lower()
    if by == "name":
        name = input("Enter a name to delete: ")
        cur.execute(f"CALL del_by_name('{name}')")
    else:
        phone = input("Enter phone to delete: ")
        cur.execute(f"CALL del_by_phone('{phone}')")
    conn.commit()

def limit_query():
    start = int(input("Show the next results: "))
    end = int(input("Skip results: "))
    cur.execute(f"SELECT * FROM phonebook LIMIT {start} OFFSET {end}")

    rows = cur.fetchall()
    for row in rows:
        print(row)

def insert_many_users():
    names = ['Alice', 'Bob', 'Charlie']
    phones = ['1234567890', 'bad-phone', '0987654321']
    cur.execute("""CALL insert_users_bulk_proc(%s::text[], %s::text[])""", (names, phones))

    cur.execute("SELECT * FROM invalid_users")
    invalid = cur.fetchall()

    print("Invalid entries:")
    for row in invalid:
        print(f"Name: {row[0]}, Phone: {row[1]}")

    conn.commit()

def main():
    create_table()

    while True:
        print("\n1. Insert from CSV")
        print("2. Insert from Console")
        print("3. Update User")
        print("4. Search by pattern")
        print("5. Query Data")
        print("6. Delete User")
        print("7. Add or Update User")
        print("8. Pagination")
        print("9. Insert many users")
        print("10. Exit")
        choice = input("Choose an action: ")

        if choice == "1":
            path = input("Enter CSV path: ")
            insert_from_csv(path)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_user()
        elif choice == "4":
            search_by_pattern()
        elif choice == "5":
            query_data()
        elif choice == "6":
            delete_user()
        elif choice == "7":
            add_or_update()
        elif choice == "8":
            limit_query()
        elif choice == "9":
            insert_many_users()
        elif choice == "10":
            break
        else:
            print("Invalid choice.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()