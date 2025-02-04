import psycopg2
import db.config as config

class AlloyDBConnection:
    """Manages a connection to an AlloyDB database."""
    def __init__(self):
        self.connection_params = {
            'host': config.HOST,
            'port': config.PORT,
            'dbname': config.DBNAME,
            'user': config.USER,
            'password': config.PASSWORD
        }
        self.conn = None

    def connect(self):
        # Establish connection if not already connected
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(**self.connection_params)
        return self.conn

    def close(self):
        # Close the connection
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        # Context manager enter
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Context manager exit
        self.close()
