import sys
sys.path.append("/Users/Yashwanth.B/Library/CloudStorage/OneDrive-CPGPLC/projects/python/pdf-generator")
from db.handler import AlloyDBHandler
from db.tables import TABLES

class PdfService:
    """Service class to handle CRUD operations using AlloyDB connection."""
    def __init__(self):
        self.db_handler = AlloyDBHandler()
        self.site_details = []

    def _ensure_connection(self):
        conn = self.db_handler.db_connection.conn
        if conn is None or conn.closed:
            self.db_handler.db_connection.connect()

    def get_site_details(self, site_code):
        self._ensure_connection()
        return self.db_handler.fetch_all_data(f"SELECT site_id FROM {TABLES.SITE_DETAILS.value} WHERE site_code = '{site_code}';")

    def get_cafeinfo(self, site_id):
        self._ensure_connection()
        cafe_info_ids_array = self.db_handler.fetch_all_data(f"SELECT cafe_id FROM {TABLES.CAFE_INFO.value} WHERE site_id = '{site_id}'; ")
        return [cafe_id for [cafe_id] in cafe_info_ids_array] # destructure into flat array

    def get_checkpoint_response(self, cafe_id):
        self._ensure_connection()
        return self.db_handler.fetch_all_data(
            f"""
            SELECT row_to_json(t)
            FROM (
                SELECT checkpoint_response_id, checkpoint_id, created_on, area_id
                FROM {TABLES.CHECKPOINT_RESPONSE.value}
                WHERE cafe_id = '{cafe_id}' and submitted = true
            ) t;
            """
        ) or []

    def get_all_checkpoint_response(self, cafe_ids):
        self._ensure_connection()
        checkpoint_response_list = []
        for cafe_id in cafe_ids:
            checkpoint_response_col = self.get_checkpoint_response(cafe_id)
            for [checkpoint_response] in checkpoint_response_col:
                checkpoint_response_list.append(checkpoint_response)
        return checkpoint_response_list
    
    def get_checkpoint(self, checkpoint_id):
        self._ensure_connection()
        return self.db_handler.fetch_all_data(f"SELECT row_to_json(t) FROM {TABLES.CHECKPOINT.value} t WHERE t.checkpoint_id = '{checkpoint_id}';")
    
    def get_all_checkpoint(self, checkpoint_response_list):
        checkpoint_list = []
        self._ensure_connection()
        for checkpoint_response in checkpoint_response_list:
            checkpoint_col = self.get_checkpoint(checkpoint_response['checkpoint_id'])
            if checkpoint_col:
                for checkpoint in checkpoint_col:
                    checkpoint_list.append(checkpoint)
            return checkpoint_list
            
    def get_response(self, checkpoint_response_id):
        self._ensure_connection()
        return self.db_handler.fetch_all_data(f"SELECT row_to_json(t) FROM {TABLES.RESPONSE.value} t WHERE t.checkpoint_response_id = '{checkpoint_response_id}';")
    
    def get_all_responses(self, checkpoint_response_list):
        response_list = []
        self._ensure_connection()
        for checkpoint_response in checkpoint_response_list:
            response_col = self.get_response(checkpoint_response['checkpoint_response_id'])
            if response_col:
                for response in response_col:
                    response_list.append(response)
            return response_list
        
    def get_area(self, area_id):
        self._ensure_connection()
        return self.db_handler.fetch_all_data(f"SELECT row_to_json(t) FROM {TABLES.AREA.value} t WHERE t.area_id = '{area_id}';")
    
    def get_all_area(self, checkpoint_response_list):
        area_list = []
        self._ensure_connection()
        for checkpoint_response in checkpoint_response_list:
            area_col = self.get_area(checkpoint_response['area_id'])
            if area_col:
                for area in area_col:
                    area_list.append(area)
            return area_list

if __name__ == '__main__':
    service = PdfService()
    site_code = '137Y'
    try:
        [[site_id]] = service.get_site_details(site_code)
        cafe_ids = service.get_cafeinfo(site_id)
        checkpoint_response_list = service.get_all_checkpoint_response(cafe_ids)
        response_list = service.get_all_responses(checkpoint_response_list)
        checkpoint_list = service.get_all_checkpoint(checkpoint_response_list)
        area_list = service.get_all_area(checkpoint_response_list)
        print('area_list--', area_list)
    except Exception as e:
        print('Error:', e)
    finally:
        service.db_handler.close()