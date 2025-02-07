import json
import sys
from datetime import datetime
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
    
    def process_mapping_checkpoint(self, data, key_field: str):
        """Process mapping data into a dictionary.
        
        Args:
            data: List of dictionaries containing mapping data
            key_field: Field name to use as dictionary key
            value_field: Field name to use as dictionary value
        """
        mapping = {}
        for item in data:
            mapping[item[key_field]] = {
                "General_Cleaning_name": item["checkpoint_name"],
                "code": item["checkpoint_code"],
                "Receiving_text": item['document_id'],
            }
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
            FROM (SELECT cafe_id, cafe_name as Cafeteria_Name, cafe_code FROM {TABLES.CAFE_INFO.value} WHERE site_id = '{site_id}') t;
        """
        cafe_info_ids_array = self.db_handler.fetch_all_data(query) # 
        return {cafe_data["cafe_code"]: cafe_data for [cafe_data] in cafe_info_ids_array} # destructure into flat array

    def get_checkpoint_response(self, cafe_id, area_id):
        self._ensure_connection()
        start_date = f"{self.date}T00:00:00"
        end_date = f"{self.date}T23:59:59"
        return self.db_handler.fetch_all_data(
            f"""
            SELECT row_to_json(t)
            FROM (
                SELECT checkpoint_response_id, checkpoint_id, submitted_by, submitted_on
                FROM {TABLES.CHECKPOINT_RESPONSE.value}
               WHERE cafe_id = '{cafe_id}' 
                AND area_id = '{area_id}' 
                AND submitted = true
                AND created_on >= '{start_date}' AND  created_on <= '{end_date}'
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
    
    def get_checkpoint(self):
        self._ensure_connection()
        query = f"""
            SELECT row_to_json(t) 
            FROM (SELECT checkpoint_id, checkpoint_name, checkpoint_code, document_id FROM {TABLES.CHECKPOINT.value}) t;
        """
        checkpoint_data = self.db_handler.fetch_all_data(query)
        checkpoint_list = [checkpoint for [checkpoint] in checkpoint_data]
        checkpoint_mappings = self.process_mapping_checkpoint(checkpoint_list, "checkpoint_id")
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
    
    def get_users(self):
        self._ensure_connection()
        query = f"""
            SELECT row_to_json(t) 
            FROM (SELECT user_id, fullname FROM {TABLES.USERS.value}) t;
        """
        users_data = self.db_handler.fetch_all_data(query)
        users_list = [question for [question] in users_data]
        users_mappings = self.process_mapping_data(users_list, "user_id", "fullname")
        return users_list, users_mappings
    
            
    def get_response(self, checkpoint_response_id):
        self._ensure_connection()
        query = f"""
            SELECT row_to_json(t) 
            FROM (SELECT action_taken, quantity, comment, dynamic_question, response_id, question_description, question_type, sanitizer_concentration, selected_answer, unit  FROM {TABLES.RESPONSE.value} WHERE checkpoint_response_id = '{checkpoint_response_id}') t;
        """
        return self.db_handler.fetch_all_data(query)

    def get_all_responses(self, checkpoint_response_list):
        response_list = {}
        self._ensure_connection()
        checkpoint_list, checkpoint_mappings = service.get_checkpoint()
        users_list, users_mappings = self.get_users()
        # question_list, question_mappings = service.get_questions()
        for checkpoint_response in checkpoint_response_list.values():
            response_col = self.get_response(checkpoint_response['checkpoint_response_id'])
            submitted_by = " "
            if checkpoint_response['submitted_by'] not in users_mappings:
                submitted_by = " "
            else:
                submitted_by = users_mappings[checkpoint_response['submitted_by']]
            
            checkpoint_response['submitted_by'] = submitted_by
            checkpoint_response['submitted_on'] = " " if checkpoint_response['submitted_on'] == None else str(datetime.fromisoformat(checkpoint_response['submitted_on']).date())

            if checkpoint_response['checkpoint_id'] not in checkpoint_mappings:
                checkpoint_response['checkpoint_response_details'] = ''
            else :
                checkpoint_response.update(checkpoint_mappings[checkpoint_response['checkpoint_id']])
            if response_col:
                for [response] in response_col:
                    response_list[response['response_id']] = {
                         "Quantity": response["quantity"],
                         "response": response['selected_answer'], 
                         "Sanitizer Concentration": response["sanitizer_concentration"],
                         "MOG-Name":response["dynamic_question"],
                         "question": response['question_description'], 
                         "comment": response["comment"], 
                         "action_taken": response['action_taken'], 
                         "image": None,
                         "unit": response['unit'],
                    }

            
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
        cafe_dict = dict['cafes']
        for cafe in cafe_dict.values():
            area_list = self.get_area_cafe_association(cafe['cafe_id'])
            area_dict = {}
            if area_list:
                area_set = set(area[0] for area in area_list)
                for area in area_set:
                    area_dict[area_mapping[area]] = {'area_id': area}
            cafe['Areas'] = area_dict
        return dict

    def construct_json_checkpoint_response(self, dict):
        cafes = dict['cafes']
        for cafe in cafes.values():
            areas = cafe['Areas']
            for area in areas.values():
                cafe_id = cafe['cafe_id']
                area_id = area['area_id']
                checkpoint_response_data = self.get_checkpoint_response(cafe_id=cafe_id, area_id=area_id)
                checkpoint_response_col = {checkpoint_response['checkpoint_response_id']: checkpoint_response for [checkpoint_response] in checkpoint_response_data}
                if 'area_id' in area:
                    del area['area_id']
                area.update(checkpoint_response_col)
                self.get_all_responses(checkpoint_response_col)

if __name__ == '__main__':
    dict = {}
    service = PdfService()
    site_uuid = '00000000-0000-4000-8122-000000000001'
    service.date = '2024-11-11' #todo
    try:
        [[site_id, site_code, site_name]] = service.get_site_details(site_uuid)
        dict["Site Name"] = site_name
        dict["Site ID"] = site_code
        dict["Report Date"] = service.date
        dict["Verified By"] = "Test"
        cafe_list = service.get_cafeinfo(site_id)
        dict['cafes'] = cafe_list
        
        area_list, area_mapping = service.get_areas()

        checkpoint_list, checkpoint_mappings = service.get_checkpoint()
        service.get_cafe_area_association(dict, area_mapping)
        service.construct_json_checkpoint_response(dict)

        # Write JSON data to a file
        with open("pdf-generation.json", "w", encoding="utf-8") as json_file:
            json.dump(dict, json_file, ensure_ascii=False, indent=4)  # Pretty formatting

        print(f"JSON data saved")

    except Exception as e:
        print('Error:', e)
    finally:
        service.db_handler.close()