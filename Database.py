import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def connect_to_database():
    try:
        con = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "postgres"),
            database=os.getenv("DB_NAME", "bankingSystem"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", "5432")
        )

        print("Connection established")
        return con

    except psycopg2.Error as e:
        print("Connection failed")
        print(e)
        return None
 
if __name__ == "__main__":
    conn = connect_to_database()
    if conn:
        conn.close()
        print("connection closed")