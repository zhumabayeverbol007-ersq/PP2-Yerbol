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

def init_db():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(50),
                    phone VARCHAR(20) UNIQUE
                );
            """)
            
            cur.execute("""
                CREATE OR REPLACE FUNCTION search_by_pattern(pattern_text TEXT)
                RETURNS TABLE(id INTEGER, first_name VARCHAR(50), phone VARCHAR(20))
                AS $$
                BEGIN
                    RETURN QUERY
                    SELECT pb.id, pb.first_name, pb.phone
                    FROM phonebook pb
                    WHERE pb.first_name ILIKE '%' || pattern_text || '%'
                       OR pb.phone ILIKE '%' || pattern_text || '%';
                END;
                $$ LANGUAGE plpgsql;
            """)
            
            cur.execute("""
                CREATE OR REPLACE PROCEDURE upsert_user(
                    user_name VARCHAR(50),
                    user_phone VARCHAR(20)
                )
                AS $$
                BEGIN
                    INSERT INTO phonebook (first_name, phone)
                    VALUES (user_name, user_phone)
                    ON CONFLICT (phone) 
                    DO UPDATE SET first_name = EXCLUDED.first_name;
                END;
                $$ LANGUAGE plpgsql;
            """)
            
            cur.execute("""
                CREATE OR REPLACE PROCEDURE insert_many_users(
                    INOUT incorrect_data REFCURSOR DEFAULT 'incorrect_cur'
                )
                AS $$
                BEGIN
                    OPEN incorrect_data FOR
                    SELECT first_name, phone
                    FROM temp_users
                    WHERE phone !~ '^[0-9+()\\- ]+$'
                       OR LENGTH(phone) < 5
                       OR first_name IS NULL OR first_name = '';
                    
                    INSERT INTO phonebook (first_name, phone)
                    SELECT first_name, phone
                    FROM temp_users
                    WHERE phone ~ '^[0-9+()\\- ]+$'
                      AND LENGTH(phone) >= 5
                      AND first_name IS NOT NULL AND first_name != ''
                    ON CONFLICT (phone) 
                    DO UPDATE SET first_name = EXCLUDED.first_name;
                END;
                $$ LANGUAGE plpgsql;
            """)
            
            cur.execute("""
                CREATE OR REPLACE FUNCTION get_paginated_data(
                    page_limit INTEGER,
                    page_offset INTEGER
                )
                RETURNS TABLE(id INTEGER, first_name VARCHAR(50), phone VARCHAR(20), total_count BIGINT)
                AS $$
                BEGIN
                    RETURN QUERY
                    SELECT 
                        pb.id,
                        pb.first_name,
                        pb.phone,
                        COUNT(*) OVER() as total_count
                    FROM phonebook pb
                    ORDER BY pb.id
                    LIMIT page_limit
                    OFFSET page_offset;
                END;
                $$ LANGUAGE plpgsql;
            """)
            
            cur.execute("""
                CREATE OR REPLACE PROCEDURE delete_by_username_or_phone(
                    search_value VARCHAR(50)
                )
                AS $$
                BEGIN
                    DELETE FROM phonebook
                    WHERE first_name = search_value
                       OR phone = search_value;
                END;
                $$ LANGUAGE plpgsql;
            """)
        conn.commit()
    print("Table zhane procedures daiyn.")

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
                        cur.execute(
                            "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING;",
                            (first_name, phone)
                        )
        print("CSV inserted.")
    except FileNotFoundError:
        print("CSV file not found.")
    except Exception as e:
        print(f"Error: {e}")

def upsert_user():
    first_name = input("First name: ").strip()
    phone = input("Phone: ").strip()
    if not first_name or not phone:
        print("All fields required.")
        return
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_user(%s, %s);", (first_name, phone))
                conn.commit()
        print("Upserted successfully.")
    except Exception as e:
        print(f"Error: {e}")

def ins_many():
    users = []
    print("Users (type 'done' when finished):")
    while True:
        first_name = input("First name (or 'done'): ").strip()
        if first_name.lower() == 'done':
            break
        phone = input("Phone: ").strip()
        users.append((first_name, phone))
    
    if not users:
        print("No users to insert.")
        return
    
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE TEMP TABLE temp_users (first_name VARCHAR(50), phone VARCHAR(20));")
                
                for first_name, phone in users:
                    cur.execute("INSERT INTO temp_users (first_name, phone) VALUES (%s, %s);", 
                               (first_name, phone))
                
                cur.execute("CALL insert_many_users();")
                
                cur.execute("FETCH ALL FROM incorrect_cur;")
                incorrect = cur.fetchall()
                
                if incorrect:
                    print("\nIncorrect data tabyldy:")
                    for item in incorrect:
                        print(f"Name: {item[0]}, Phone: {item[1]}")
                else:
                    print("\nAll data qosyldy.")
                
                cur.execute("DROP TABLE temp_users;")
                conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def srch_pat():
    pattern = input("Pattern izdeu (part of name/phone): ").strip()
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_by_pattern(%s);", (pattern,))
                rows = cur.fetchall()
                if rows:
                    for r in rows:
                        print(f"{r[0]} | {r[1]} | {r[2]}")
                else:
                    print("No records found.")
    except Exception as e:
        print(f"Error: {e}")

def show_all():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM phonebook ORDER BY id;")
                rows = cur.fetchall()
                if rows:
                    for r in rows:
                        print(f"{r[0]} | {r[1]} | {r[2]}")
                else:
                    print("No records found.")
    except Exception as e:
        print(f"Error: {e}")

def get_pag_data():
    try:
        limit = int(input("Limit (records per page): ").strip())
        offset = int(input("Offset (records to skip): ").strip())
        
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_paginated_data(%s, %s);", (limit, offset))
                rows = cur.fetchall()
                
                if rows:
                    for r in rows:
                        print(f"{r[0]} | {r[1]} | {r[2]}")
                else:
                    print("No records found.")
    except ValueError:
        print("Please enter valid numbers.")
    except Exception as e:
        print(f"Error: {e}")

def del_name_or_phone():
    value = input("Òshiruge name or phone: ").strip()
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_by_username_or_phone(%s);", (value,))
                conn.commit()
                print("Òshirildi.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    init_db()
    while True:
        print("\nphonebook")
        print("1-Insert from CSV")
        print("2-Insert/Update user")
        print("3-Insert many users")
        print("4-Search by pattern")
        print("5-Show all")
        print("6-Get paginated data")
        print("7-Delete by username or phone")
        print("0-Exit")
        choice = input("Tańdau: ").strip()
        if choice == "1":
            ins_csv(input("CSV path: ").strip())
        elif choice == "2":
            upsert_user()
        elif choice == "3":
            ins_many()
        elif choice == "4":
            srch_pat()
        elif choice == "5":
            show_all()
        elif choice == "6":
            get_pag_data()
        elif choice == "7":
            del_name_or_phone()
        elif choice == "0":
            print("Bye")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()