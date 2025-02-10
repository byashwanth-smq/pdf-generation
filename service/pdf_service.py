import os
import json
import sys
import copy
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))    
__package__ = 'db'

from db.handler import AlloyDBHandler
from db.tables import TABLES

@dataclass
class DBConfig:
    """Configuration class for database operations."""
    date: str
    site_id: str

class PdfService:
    """Service class to handle CRUD operations using AlloyDB connection."""
    
    def __init__(self, date: str):
        """Initialize PDF service with date."""
        self.db_handler = AlloyDBHandler()
        self.date = date

    def _ensure_connection(self) -> None:
        """Ensure database connection is active."""
        conn = self.db_handler.db_connection.conn
        if conn is None or conn.closed:
            self.db_handler.db_connection.connect()

    @staticmethod
    def process_mapping_data(data: List[Dict], key_field: str, value_field: str) -> Dict:
        """Create a mapping dictionary from list of dictionaries.
        
        Args:
            data: List of dictionaries containing mapping data
            key_field: Field name to use as dictionary key
            value_field: Field name to use as dictionary value
            
        Returns:
            Dict: Processed mapping dictionary
        """
        return {item[key_field]: item[value_field] for item in data}

    @staticmethod
    def process_checkpoint_mapping(data: List[Dict], key_field: str) -> Dict:
        """Create checkpoint mapping dictionary from list of dictionaries.
        
        Args:
            data: List of dictionaries containing checkpoint data
            key_field: Field name to use as dictionary key
            
        Returns:
            Dict: Processed checkpoint mapping
        """
        return {
            item[key_field]: {
                "General_Cleaning_name": item["checkpoint_name"],
                "code": item["checkpoint_code"],
                "Receiving_text": item['document_id']
            }
            for item in data
        }

    def get_areas(self) -> Tuple[List[Dict], Dict]:
        """Fetch areas and create area mapping.
        
        Returns:
            Tuple[List[Dict], Dict]: List of areas and area mapping dictionary
        """
        self._ensure_connection()
        query = f"""
            SELECT row_to_json(t) 
            FROM (SELECT area_id, name FROM {TABLES.AREA.value}) t;
        """
        area_arr = self.db_handler.fetch_all_data(query)
        area_list  = []
        if len(area_arr):
            area_list = [area for [area] in area_arr]
        area_mapping = self.process_mapping_data(area_list, "area_id", "name")
        return area_list, area_mapping

    def get_site_details(self, site_id: str) -> List[List]:
        """Fetch site details.
        
        Args:
            site_id: Site identifier
            
        Returns:
            List[List]: Site details
        """
        self._ensure_connection()
        return self.db_handler.fetch_all_data(
            f"SELECT site_id, site_code, site_name FROM {TABLES.SITE_DETAILS.value} WHERE site_id = '{site_id}';"
        )

    def get_cafe_info(self, site_id: str) -> Dict:
        """Fetch cafe information for a site.
        
        Args:
            site_id: Site identifier
            
        Returns:
            Dict: Cafe information dictionary
        """
        self._ensure_connection()
        query = f"""
            SELECT row_to_json(t) 
            FROM (SELECT cafe_id, cafe_name as Cafeteria_Name, cafe_code 
                  FROM {TABLES.CAFE_INFO.value} 
                  WHERE site_id = '{site_id}') t;
        """
        cafe_info = self.db_handler.fetch_all_data(query)
        return {cafe_data[0]["cafe_code"]: cafe_data[0] for cafe_data in cafe_info}

    def get_checkpoint_response(self, cafe_id: str, area_id: str) -> List:
        """Fetch checkpoint responses for a cafe and area.
        
        Args:
            cafe_id: Cafe identifier
            area_id: Area identifier
            
        Returns:
            List: Checkpoint responses
        """
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
                AND created_on >= '{start_date}' AND created_on <= '{end_date}'
                AND skipped = false
            ) t;
            """
        ) or []

    def get_checkpoints(self) -> Tuple[List[Dict], Dict]:
        """Fetch checkpoints and create checkpoint mapping.
        
        Returns:
            Tuple[List[Dict], Dict]: List of checkpoints and checkpoint mapping
        """
        self._ensure_connection()
        query = f"""
            SELECT row_to_json(t) 
            FROM (SELECT checkpoint_id, checkpoint_name, checkpoint_code, document_id 
                  FROM {TABLES.CHECKPOINT.value}) t;
        """
        checkpoint_data = self.db_handler.fetch_all_data(query)
        checkpoint_list = [checkpoint[0] for checkpoint in checkpoint_data]
        checkpoint_mappings = self.process_checkpoint_mapping(checkpoint_list, "checkpoint_id")
        return checkpoint_list, checkpoint_mappings

    def get_users(self) -> Tuple[List[Dict], Dict]:
        """Fetch users and create user mapping.
        
        Returns:
            Tuple[List[Dict], Dict]: List of users and user mapping
        """
        self._ensure_connection()
        query = f"""
            SELECT row_to_json(t) 
            FROM (SELECT user_id, fullname FROM {TABLES.USERS.value}) t;
        """
        users_data = self.db_handler.fetch_all_data(query)
        users_list = [user[0] for user in users_data]
        users_mappings = self.process_mapping_data(users_list, "user_id", "fullname")
        return users_list, users_mappings

    def get_response(self, checkpoint_response_id: str) -> List:
        """Fetch responses for a checkpoint response.
        
        Args:
            checkpoint_response_id: Checkpoint response identifier
            
        Returns:
            List: Response data
        """
        self._ensure_connection()
        query = f"""
            SELECT row_to_json(t) 
            FROM (SELECT action_taken, quantity, comment, dynamic_question, 
                         response_id, question_description, question_type, 
                         sanitizer_concentration, selected_answer, unit
                  FROM {TABLES.RESPONSE.value} 
                  WHERE checkpoint_response_id = '{checkpoint_response_id}') t;
        """
        return self.db_handler.fetch_all_data(query)

    def process_responses(self, checkpoint_response_list: Dict, 
                         checkpoint_mappings: Dict, users_mappings: Dict) -> Dict:
        """Process all responses for checkpoint responses.
        
        Args:
            checkpoint_response_list: Dictionary of checkpoint responses
            checkpoint_mappings: Checkpoint mapping dictionary
            users_mappings: User mapping dictionary
            
        Returns:
            Dict: Processed responses
        """
        response_list = {}
        
        for checkpoint_response in checkpoint_response_list.values():
            response_data = self.get_response(checkpoint_response['checkpoint_response_id'])
            
            # Process submitted by
            submitted_by = users_mappings.get(checkpoint_response['submitted_by'], " ")
            checkpoint_response['submitted_by'] = submitted_by
            
            # Process submission date
            submitted_on = checkpoint_response['submitted_on']
            checkpoint_response['submitted_on'] = " " if submitted_on is None else str(
                datetime.fromisoformat(submitted_on).date()
            )
            
            # Update checkpoint response with checkpoint details
            if checkpoint_response['checkpoint_id'] in checkpoint_mappings:
                checkpoint_response.update(checkpoint_mappings[checkpoint_response['checkpoint_id']])
            else:
                checkpoint_response['checkpoint_response_details'] = ''
            
            # Process responses
            for [response] in response_data:
                response_list[response['response_id']] = {
                    "Dish name" : response['dynamic_question'],
                    "Quantity": response["quantity"],
                    "Product temperature": response['product_temp'],
                    "Response": response['selected_answer'],
                    "Sanitizer Concentration": response["sanitizer_concentration"],
                    "Start temp": response['start_temp'] if response['start_temp'] else response['selected_answer'],
                    "Not in service": response['not_in_service'],
                    "MOG-Name":response["dynamic_question"],
                    "Sub-Checkpoint": response['question_description'],
                    "Comment": response["comment"],
                    "Category": response['category'],
                    "Action_taken": response['action_taken'],
                    "Image": None,
                    "Unit": response['unit'],
                    "Equipment Temperature°C": response['selected_answer'],
                    "Duration": response['minutes'],
                    "Start time / end time": response['start_time'] + ' ' + response['end_time'] ,
                    "End temp": response['product_temp'] if response['product_temp'] else response['end_temp_or_storage_temp'],
                    "After 90 min": response['end_temp_or_storage_temp'],
                    "Reheating Temp (°C)": response['end_temp_or_storage_temp'],
                    "Cooking Completion Temp (°C)": response['start_temp'] if response['start_temp'] else response['selected_answer']
                }
            
            checkpoint_response['response_details'] = response_list
        
        return response_list

    def get_area_cafe_association(self, cafe_id: str) -> List:
        """Fetch area-cafe associations.
        
        Args:
            cafe_id: Cafe identifier
            
        Returns:
            List: Area-cafe associations
        """
        self._ensure_connection()
        return self.db_handler.fetch_all_data(
            f"SELECT area_id FROM {TABLES.AREA_CAFE_ASSOCIATION.value} WHERE cafe_id = '{cafe_id}';"
        )

    def process_cafe_area_association(self, cafe_dict: Dict, area_mapping: Dict) -> Dict:
        """Process cafe-area associations and return new dictionary.
        
        Args:
            cafe_dict: Dictionary containing cafe information
            area_mapping: Dictionary mapping area IDs to names
            
        Returns:
            Dict: New dictionary with processed cafe-area associations
        """
        processed_cafe_dict = copy.deepcopy(cafe_dict)
        
        for cafe in processed_cafe_dict.values():
            area_list = self.get_area_cafe_association(cafe['cafe_id'])
            
            area_dict = {}
            if area_list:
                area_set = set(area[0] for area in area_list)
                area_dict = {
                    area_mapping[area]: {'area_id': area}
                    for area in area_set
                }
            
            cafe['Areas'] = area_dict
        
        return processed_cafe_dict

    def process_checkpoint_responses_and_response_data(self, cafe_dict: Dict) -> Dict:
        processed_cafe_dict = copy.deepcopy(cafe_dict)
        
        _, checkpoint_mappings = self.get_checkpoints()
        _, users_mappings = self.get_users()
        
        for cafe in processed_cafe_dict.values():
            processed_areas = {}
            
            for area_name, area in cafe['Areas'].items():
                processed_area = dict(area)
                
                checkpoint_response_data = self.get_checkpoint_response(
                    cafe_id=cafe['cafe_id'],
                    area_id=area['area_id']
                )
                
                checkpoint_response_col = {checkpoint_response['checkpoint_response_id']: checkpoint_response for [checkpoint_response] in checkpoint_response_data}
                
                if 'area_id' in processed_area:
                    del processed_area['area_id']
                
                processed_area.update(checkpoint_response_col)
                
                # Store the returned responses and update the processed area
                response_details = self.process_responses(
                    checkpoint_response_col,
                    checkpoint_mappings,
                    users_mappings
                )
                processed_area['response_details'] = response_details
                
                processed_areas[area_name] = processed_area
            
            cafe['Areas'] = processed_areas
        
        return processed_cafe_dict

    def generate_pdf_data(self, site_uuid: str) -> Dict:
        """Generate complete PDF data.
        
        Args:
            site_uuid: Site UUID
            
        Returns:
            Dict: Complete PDF data
        """
        try:
            [[site_id, site_code, site_name]] = self.get_site_details(site_uuid)
            
            pdf_data = {
                "Site Name": site_name,
                "Site ID": site_code,
                "Report Date": self.date,
                "Verified By": "Test",
                "cafes": self.get_cafe_info(site_id)
            }
            
            _, area_mapping = self.get_areas()
            
            # Process associations and responses using pure functions
            cafe_dict = pdf_data['cafes']
            processed_cafe_dict = self.process_cafe_area_association(cafe_dict, area_mapping)
            final_cafe_dict = self.process_checkpoint_responses_and_response_data(processed_cafe_dict)
            
            return {
                **pdf_data,
                "cafes": final_cafe_dict
            }
            
        finally:
            self.db_handler.close()

def main():
    """Main function to generate PDF data."""
    site_uuid = '00000000-0000-4000-8122-000000000001'
    date = '2024-11-11'
    
    service = PdfService(date)
    
    try:
        pdf_data = service.generate_pdf_data(site_uuid)
        
        # Write JSON data to a file
        with open("pdf-generation.json", "w", encoding="utf-8") as json_file:
            json.dump(pdf_data, json_file, ensure_ascii=False, indent=4)
        
        print("JSON data saved successfully")
        
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    main()