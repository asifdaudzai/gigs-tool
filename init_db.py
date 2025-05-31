from db import get_db_connection

def create_user_table():
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    cursor = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        cursor.execute(create_table_query)
        conn.commit()
        print("User table created successfully.")
    except Exception as e:
        print(f"Error creating user table: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_user_table()
