import psycopg2

def get_table_names():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            dbname='insightsms',
            user='postgres',
            password='postgres'
        )
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # Query to get all table names
        cursor.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        
        # Fetch all table names
        tables = cursor.fetchall()
        
        # Print table names
        print("Tables in the database:")
        for table in tables:
            print(table[0])
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    get_table_names()