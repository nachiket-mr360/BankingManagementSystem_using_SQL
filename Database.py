import psycopg2

def connect_to_database():
    try:
        connection = psycopg2.connect(
            host = 'localhost',
            database = 'bankingSystem',
            user = 'postgres',
            password = 'Nachiket',
            port= '5432'
         )
        print('Connected to PostgreSQL')
        return connection
    except psycopg2.Error as e:
        print('error connecting postgresSQL database: ',e)
        return None
        
if __name__ == "__main__":
    conn = connect_to_database()
    if conn:
        conn.close()
        print("connection closed")