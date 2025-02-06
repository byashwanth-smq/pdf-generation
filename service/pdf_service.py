import json
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
        
    def process_mapping_data(self, data, key_field: str, value_field: str):
        """Process mapping data into a dictionary.
        
        Args:
            data: List of dictionaries containing mapping data
            key_field: Field name to use as dictionary key
            value_field: Field name to use as dictionary value
        """
        mapping = {}
        for item in data:
            mapping[item[key_field]] = item[value_field]
        return mapping

    def get_areas(self):
        self._ensure_connection()
        query = f"""
            SELECT row_to_json(t) 
            FROM (SELECT area_id, name FROM {TABLES.AREA.value}) t;
        """
        area_arr = self.db_handler.fetch_all_data(query)
        area_list = [area for [area] in area_arr]
        area_mapping = self.process_mapping_data(area_list, "area_id", "name")
        return area_list, area_mapping
        

    def get_site_details(self, site_id):
        self._ensure_connection()
        return self.db_handler.fetch_all_data(f"SELECT site_id, site_code, site_name FROM {TABLES.SITE_DETAILS.value} WHERE site_id = '{site_id}';")

    def get_cafeinfo(self, site_id):
        self._ensure_connection()
        query = f"""
            SELECT row_to_json(t) 
            FROM (SELECT cafe_id, cafe_name FROM {TABLES.CAFE_INFO.value} WHERE site_id = '{site_id}') t;
        """
        cafe_info_ids_array = self.db_handler.fetch_all_data(query)
        return [cafe_data for [cafe_data] in cafe_info_ids_array] # destructure into flat array

    def get_checkpoint_response(self, cafe_id, area_id):
        self._ensure_connection()
        return self.db_handler.fetch_all_data(
            f"""
            SELECT row_to_json(t)
            FROM (
                SELECT checkpoint_response_id, checkpoint_id
                FROM {TABLES.CHECKPOINT_RESPONSE.value}
                WHERE cafe_id = '{cafe_id}' and area_id = '{area_id}' 
            ) t;
            """ 
        ) or [] #  and createdon = date # 1 day and submitted = true
    
    def get_all_checkpoint_response(self, cafe_ids):
        self._ensure_connection()
        checkpoint_response_list = []
        for cafe_id in cafe_ids:
            checkpoint_response_col = self.get_checkpoint_response(cafe_id)
            for [checkpoint_response] in checkpoint_response_col:
                checkpoint_response_list.append(checkpoint_response)
        return checkpoint_response_list
    
    def get_checkpoint(self):
        self._ensure_connection()
        query = f"""
            SELECT row_to_json(t) 
            FROM (SELECT checkpoint_id, checkpoint_name FROM {TABLES.CHECKPOINT.value}) t;
        """
        checkpoint_data = self.db_handler.fetch_all_data(query)
        checkpoint_list = [checkpoint for [checkpoint] in checkpoint_data]
        checkpoint_mappings = self.process_mapping_data(checkpoint_list, "checkpoint_id", "checkpoint_name")
        return checkpoint_list, checkpoint_mappings
    
    def get_questions(self):
        self._ensure_connection()
        query = f"""
            SELECT row_to_json(t) 
            FROM (SELECT question_id, description, answer_options FROM {TABLES.QUESTION.value}) t;
        """
        question_data = self.db_handler.fetch_all_data(query)
        question_list = [question for [question] in question_data]
        question_mappings = self.process_mapping_data(question_list, "question_id", "answer_options")
        return question_list, question_mappings
    
            
    def get_response(self, checkpoint_response_id):
        self._ensure_connection()
        query = f"""
            SELECT row_to_json(t) 
            FROM (SELECT response_id, question_description, selected_answer FROM {TABLES.RESPONSE.value} WHERE checkpoint_response_id = '{checkpoint_response_id}') t;
        """
        return self.db_handler.fetch_all_data(query)

    def get_all_responses(self, checkpoint_response_list):
        response_list = []
        self._ensure_connection()
        checkpoint_list, checkpoint_mappings = service.get_checkpoint()
        # question_list, question_mappings = service.get_questions()
        for checkpoint_response in checkpoint_response_list:
            response_col = self.get_response(checkpoint_response['checkpoint_response_id'])
            if checkpoint_response['checkpoint_id'] not in checkpoint_mappings:
                checkpoint_response['checkpoint_name'] = ''
            else :
                checkpoint_response['checkpoint_name'] = checkpoint_mappings[checkpoint_response['checkpoint_id']]
            if response_col:                
                for [response] in response_col:
                    
                    response_list.append({"response_id":response['response_id'], "question": response['question_description'], "answer": response['selected_answer']})
            checkpoint_response['response_details'] = response_list
        
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
    
    def get_area_cafe_association(self, cafe_id):
        self._ensure_connection()
        return self.db_handler.fetch_all_data(f"SELECT area_id  FROM {TABLES.AREA_CAFE_ASSOCIATION.value} WHERE cafe_id = '{cafe_id}';")

    def get_cafe_area_association(self, dict, area_mapping):
        cafe_list = dict['cafes']
        for cafe in cafe_list:
            area_list = self.get_area_cafe_association(cafe['cafe_id'])
            temp_area_list = []
            if area_list:
                area_set = set(area[0] for area in area_list)
                for area in area_set:
                    area_dict = {
                        'area_id': area,
                        'name':  area_mapping[area]
                    }
                    temp_area_list.append(area_dict)
            cafe['Areas'] = temp_area_list
        return dict

    def construct_json_checkpoint_response(self, dict):
        cafes = dict['cafes']
        for cafe in cafes:
            areas = cafe['Areas']
            for area in areas:
                cafe_id = cafe['cafe_id']
                area_id = area['area_id']                
                checkpoint_response = self.get_checkpoint_response(cafe_id=cafe_id, area_id=area_id)
                checkpoint_response_col = [item[0] for item in checkpoint_response]
                area['checkpoint_response_details'] = checkpoint_response_col
                self.get_all_responses(checkpoint_response_col)

if __name__ == '__main__':
    dict = {}
    service = PdfService()
    site_uuid = '00000000-0000-4000-8122-000000000001'
    start_date = None #todo
    end_date = None #todo
    try:
        [[site_id, site_code, site_name]] = service.get_site_details(site_uuid)
        dict["Site Name"] = site_name
        dict["Site Id"] = site_code
        cafe_list = service.get_cafeinfo(site_id)
        dict['cafes'] = cafe_list
        
        area_list, area_mapping = service.get_areas()

        # checkpoint_list, checkpoint_mappings = service.get_checkpoint()
        service.get_cafe_area_association(dict, area_mapping)
        service.construct_json_checkpoint_response(dict)
        print('dict---', json.dumps(dict))
    except Exception as e:
        print('Error:', e)
    finally:
        service.db_handler.close()

#  self.get_all_responses(checkpoint_response_col)