import psycopg2
import csv

DB = {
    'host': 'localhost',
    'database': 'phonebook',
    'user': 'postgres',
    'password': '1234',
    'port': '5433'
}

def connect():
    return psycopg2.connect(**DB)

def create_table():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50),
                    phone VARCHAR(20) UNIQUE
                );
            """)
    print("Table ready.")

def ins_csv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            with connect() as conn:
                with conn.cursor() as cur:
                    for row in reader:
                        if len(row) < 2:
                            continue
                        first_name, phone = row[0].strip(), row[1].strip()
                        try:
                            cur.execute(
                                "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING;",
                                (first_name, phone)
                            )
                        except Exception as e:
                            print(f"Error inserting {first_name}, {phone}: {e}")
        print("CSV inserted.")
    except FileNotFoundError:
        print("CSV file not found.")
    except Exception as e:
        print(f"Error CSV: {e}")

def ins_console():
    first_name = input("First name: ").strip()
    phone = input("Phone: ").strip()
    if not first_name or not phone:
        print("Toltyru kere.")
        return
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s);", (first_name, phone))
        print("User added.")
    except Exception as e:
        print(f"Error: {e}")

def update_user():
    old_first_name = input("Existing first name to update: ").strip()
    new_first_name = input("New first name: ").strip()
    new_phone = input("New phone: ").strip()
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE phonebook SET first_name=%s, phone=%s WHERE first_name=%s;",
                    (new_first_name, new_phone, old_first_name)
                )
                print(f"Updated {cur.rowcount} row(s).")
    except Exception as e:
        print(f"Error: {e}")

def show_all():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM phonebook ORDER BY id;")
                rows = cur.fetchall()
                if rows:
                    print("\nID | First Name | Phone")
                    for r in rows:
                        print(f"{r[0]} | {r[1]} | {r[2]}")
                else:
                    print("No records found.")
    except Exception as e:
        print(f"Error: {e}")

def srch_name():
    first_name = input("First name: ").strip()
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s;", (f"%{first_name}%",))
                rows = cur.fetchall()
                if rows:
                    for r in rows:
                        print(f"{r[0]} | {r[1]} | {r[2]}")
                else:
                    print("No records found.")
    except Exception as e:
        print(f"Error: {e}")

def srch_phone():
    phone = input("Phone: ").strip()
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM phonebook WHERE phone ILIKE %s;", (f"%{phone}%",))
                rows = cur.fetchall()
                if rows:
                    for r in rows:
                        print(f"{r[0]} | {r[1]} | {r[2]}")
                else:
                    print("No records found.")
    except Exception as e:
        print(f"Error: {e}")

def del_user():
    value = input("Òshiruge name or phone: ").strip()
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM phonebook WHERE first_name=%s OR phone=%s;", (value, value))
                print(f"Òshirildi {cur.rowcount} row(s).")
    except Exception as e:
        print(f"Error: {e}")

def main():
    create_table()
    while True:
        print("\nphonebook")
        print("1-Insert from CSV")
        print("2-Insert manually")
        print("3-Update user")
        print("4-Show all")
        print("5-Search by first name")
        print("6-Search by phone")
        print("7-Delete user")
        print("0-Exit")
        choice = input("Tańdau: ").strip()
        if choice == "1":
            ins_csv(input("CSV path: ").strip())
        elif choice == "2":
            ins_console()
        elif choice == "3":
            update_user()
        elif choice == "4":
            show_all()
        elif choice == "5":
            srch_name()
        elif choice == "6":
            srch_phone()
        elif choice == "7":
            del_user()
        elif choice == "0":
            print("Bye")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()