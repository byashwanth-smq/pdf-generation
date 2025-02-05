import sys
sys.path.append("/Users/Yashwanth.B/Library/CloudStorage/OneDrive-CPGPLC/projects/python/pdf-generator")
from db.handler import AlloyDBHandler

class CRUDService:
    """Service class to handle CRUD operations using AlloyDB connection."""
    def __init__(self):
        self.db_handler = AlloyDBHandler()

    def _ensure_connection(self):
        conn = self.db_handler.db_connection.conn
        if conn is None or conn.closed:
            self.db_handler.db_connection.connect()

    def get_checkpoint_responses(self):
        self._ensure_connection()
        return self.db_handler.fetch_all_data("SELECT * FROM checkpoint_response;")

    def get_checkpoint_code_mapping(self):
        self._ensure_connection()
        checkpoint_data = self.db_handler.fetch_all_data("SELECT * FROM checkpoint;")
        checkpoint_code_mappings = {}
        for checkpoint in checkpoint_data:
            checkpoint_code_mappings[checkpoint['checkpoint_id']] = checkpoint['checkpoint_code']
        return checkpoint_code_mappings

    def get_responses(self):
        self._ensure_connection()
        return self.db_handler.fetch_all_data("SELECT * FROM response;")
    

    def get_checkpoint_code(self):
        codes = []
        checkpoint_response_data = self.get_checkpoint_responses()
        checkpoint_code_mapping = self.get_checkpoint_code_mapping()
        for checkpoint_response in  checkpoint_response_data:
            checkpoint_code = checkpoint_code_mapping[checkpoint_response['checkpoint_id']]
            codes.append(checkpoint_code)
        return codes

if __name__ == '__main__':
    service = CRUDService()
    try:
        checkpoint_responses = service.get_checkpoint_responses()
        responses = service.get_responses()
        codes = service.get_checkpoint_code()
        print('codes', codes)
    except Exception as e:
        print('Error:', e)
    finally:
        service.db_handler.close()
