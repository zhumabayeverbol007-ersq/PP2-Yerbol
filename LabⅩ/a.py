import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    dbname="phonebook",  
    user="postgres",   
    password="1234",  
    host="localhost",
    port="5433",          
)

cursor = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS phonetry2 (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    numberph INT DEFAULT 0
);
"""
cursor.execute(create_table_query)

conn.commit()

cursor.close()
conn.close()

print("tamasha")