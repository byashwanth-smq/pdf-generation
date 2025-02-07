if __name__ == '__main__' and __package__ is None:
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = 'db'

from .connection import AlloyDBConnection
import psycopg2.extras

class AlloyDBHandler:
    """Handles data fetching from AlloyDB using a centralized connection configuration."""
    def __init__(self):
        self.db_connection = AlloyDBConnection()

    def fetch_all_data(self, query):
        # Fetch all rows from response table
        conn = self.db_connection.connect()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def close(self):
        # Closes the underlying DB connection
        self.db_connection.close()

    def __enter__(self):
        self.db_connection.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

if __name__ == '__main__':
    print('This module is not meant to be executed directly. Please run the application from the project root or use an appropriate entry point.')