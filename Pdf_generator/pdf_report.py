# checkpoint_report.py
from pdf_generator import PDFGenerator
from table_generator import TableGenerator
from datetime import datetime

class CheckpointReport:
    def __init__(self, pdf_file):
        self.pdf_gen = PDFGenerator(pdf_file)
        self.logo_1_path = "Images/Lens.png"
        self.logo_2_path = "Images/compass.png"
        self.logo_width = 100
        self.logo_height = 50
        self.current_y_position = 0

    def add_logos(self):
        self.pdf_gen.draw_logo(self.logo_1_path, 30, self.pdf_gen.page_height - 100, self.logo_width, self.logo_height)
        self.pdf_gen.draw_logo(self.logo_2_path, self.pdf_gen.page_width - 130, self.pdf_gen.page_height - 100, self.logo_width, self.logo_height)

    def add_header(self, text, font="Helvetica-Bold", font_size=18, y_position=None):
        self.pdf_gen.add_header(text, font, font_size, y_position)

    def add_site_details(self, site_name, site_id, report_date, line_y_position):
        self.pdf_gen.add_site_details(site_name, site_id, report_date, line_y_position)

    def add_cafeteria_name(self, cafeteria_name, line_y_position):
        self.pdf_gen.add_cafeteria_name(f"Cafeteria Name:  {cafeteria_name}", line_y_position)

    def add_section_header(self, header_text, y_position):
        self.pdf_gen.add_section_header(header_text, y_position)

    def generate_report(self, report_data):
        self.add_logos()
        self.add_header("Checkpoint Report", font="Helvetica-Bold", font_size=18)

        line_y_position = self.pdf_gen.page_height - 120
        
        self.add_site_details(report_data["Site Name"], report_data["Site ID"], report_data["Report Date"], line_y_position)

        table_generator = TableGenerator(self.pdf_gen.pdf, self.pdf_gen.page_width, self.pdf_gen.page_height)

        current_y_position = line_y_position - 15
        
        for cafe in report_data["cafes"]:
            self.pdf_gen.add_footer()
            if current_y_position < 150:  # Check space before adding a new section
                    self.pdf_gen.new_page()
                    current_y_position = self.pdf_gen.page_height + 30 # Reset Y position


            current_y_position = current_y_position - 25
            self.add_cafeteria_name(cafe["Cafeteria Name"], current_y_position - 10)
            
            for area in cafe["Areas"]:  # Iterate through Areas
                if current_y_position < 150:  # Check space before adding a new section
                        self.pdf_gen.new_page()
                        current_y_position = self.pdf_gen.page_height + 100 # Reset Y position

          
                self.add_section_header(area["Area name"], current_y_position - 120)  # Section header for each Area
                current_y_position -= 30  # Adjust position after section header (Important!)
                
                for checkpoint_response_details in area["checkpoint_responses"]:
                    self.pdf_gen.add_footer()
                    if current_y_position < 150:  # Check space before adding a new section
                        self.pdf_gen.new_page()
                        current_y_position = self.pdf_gen.page_height + 100 # Reset Y position
                        
                    current_y_position = table_generator.generate_table(checkpoint_response_details, y_position= current_y_position - 125)
                    current_y_position = current_y_position + 80  # Space between tables
                    
                
            
        if current_y_position < 150:  # Check space before adding a new section
                    self.pdf_gen.new_page()
                    current_y_position = self.pdf_gen.page_height + 10 # Reset Y position
                    
        # Call the new function to draw the footer text
        self.pdf_gen.draw_footer_text(current_y_position - 120,Verified_By = report_data["Verified By"] )
    
        self.pdf_gen.add_footer()
        self.pdf_gen.save_pdf()
        print("✅ PDF generated successfully with proper table alignment.")

# Usage
if __name__ == "__main__":
    
    pdf_path = "output_pdf/checkpoint_report.pdf"
    report = CheckpointReport(pdf_file = pdf_path)

    report_data = {
                    "Site Name": "BNY Mellon - Chennai",
                    "Site ID": "1247",
                    "Report Date": "14/01/2025",
                    "Verified By" : "UM",
                    "cafes": [
                        {
                        "Cafeteria Name": "Level - 6 Embassy",
                        "Areas" : [
                            {
                                "Area name": "Receiving & Stores",
                                "checkpoint_responses": [
                                {
                                "code":"5",
                                "checkpoint_response_details": {
                                     
                                    "General_Cleaning_name": "Vegetables/ Fruits Disinfection Treatment",
                                    "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                                    "submitted_on": "14-Jan-2025 07:53:45PM",
                                    "submitted_by": "AJITHA NEELAVARN"
                                },
                                "headers": [
                                                "question",
                                                "response",
                                                "comment",
                                                "action_taken",
                                                "image"
                                            ],
                                "response details": [
                                                {
                                            "question": "Common touchpoints are disinfected?",
                                            "response": "Yes",
                                            "comment": "",
                                            "action_taken": "",
                                            "image": ""
                                            },
                                            {
                                            "question": "Food contact surfaces",
                                            "response": "Yes",
                                            "comment": "",
                                            "action_taken": "",
                                            "image": ""
                                            },
                                            {
                                            "question": "Receiving area is clean & well maintained?",
                                            "response": "Yes",
                                            "comment": "",
                                            "action_taken": "",
                                            "image": ""
                                            },
                                            {
                                            "question": "Receiving area free from pest infestation?",
                                            "response": "Yes",
                                            "comment": "",
                                            "action_taken": "",
                                            "image": ""
                                            },
                                            {
                                            "question": "Receiving area free from supplier cartons",
                                            "response": "Yes",
                                            "comment": "",
                                            "action_taken": "",
                                            "image": ""
                                            }
                                        ]
                            },
                            {
                            "code":"10",
                            "checkpoint_response_details": {
                                "General_Cleaning_name": "tables/ Fruits Disinfection Treatment",
                                "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                                "submitted_on": "14-Jan-2025 07:53:45PM",
                                "submitted_by": "AJITHA NEELAVARN"
                            },
                            "headers": [
                                "MOG-Name",
                                "Quantity",
                                "Unit",
                                "Duration",
                                "Sanitizer Concentration",
                                "Sub-Checkpoint",
                                "Response",
                                "Comment",
                                "Action Taken",
                                "Image"
                            ],
                            "response details": [
                                {
                                "MOG-Name": "Ginger Fresh",
                                "Quantity": "20.0",
                                "Unit": "Kgs",
                                "Duration": "15 Min",
                                "Sanitizer Concentration": "50 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Tomato Fresh (Hybrid)",
                                "Quantity": "60.0",
                                "Unit": "Kgs",
                                "Duration": "20 Min",
                                "Sanitizer Concentration": "100 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Carrot Red Fresh",
                                "Quantity": "40.0",
                                "Unit": "Kgs",
                                "Duration": "15 Min",
                                "Sanitizer Concentration": "50 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                }
                            ]
                            },
                            {
                            "code":"7",
                            "checkpoint_response_details": {
                                "General_Cleaning_name": "Equipment Temperature Record - Level 6 Embassy",
                                "Receiving_text": "HSEQ-FS/F/SOP -13",
                                "submitted_on": "14-Jan-2025 07:53:45PM",
                                "submitted_by": "AJITHA NEELAVARN"
                            },
                            "headers": [
                                "Question",
                                "Not in Service",
                                "Equipment Temperature°C",
                                "Product Temperature°C",
                                "Comment",
                                "Action Taken",
                                "Image"
                            ],
                            "response details": [
                                {
                                "Question": "Store chiller",
                                "Not in Service": "No",
                                "Equipment Temperature°C": "4",
                                "Product Temperature°C": "",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                }
                            ]
                            }
                        ]
                            },
                            {
                                "Area name": "Receiving & Stores",
                                "checkpoint_responses": [
                            {
                            "code":"9",    
                            "checkpoint_response_details": {
                                "General_Cleaning_name": "Vegetables/ Fruits Disinfection Treatment",
                                "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                                "submitted_on": "14-Jan-2025 07:53:45PM",
                                "submitted_by": "AJITHA NEELAVARN"
                            },
                            "headers": [
                                "MOG-Name",
                                "Unit",
                                "Duration",
                                "Sanitizer Concentration",
                                "Sub-Checkpoint",
                                "Response",
                                "Comment",
                                "Action Taken",
                                "Image"
                            ],
                            "response details": [
                                {
                                "MOG-Name": "Ginger Fresh",
                                "Quantity": "20.0",
                                "Unit": "Kgs",
                                "Duration": "15 Min",
                                "Sanitizer Concentration": "50 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Tomato Fresh (Hybrid)",
                                "Quantity": "60.0",
                                "Unit": "Kgs",
                                "Duration": "20 Min",
                                "Sanitizer Concentration": "100 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Carrot Red Fresh",
                                "Quantity": "40.0",
                                "Unit": "Kgs",
                                "Duration": "15 Min",
                                "Sanitizer Concentration": "50 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                }
                            ]
                            },
                            {
                            "code":"8",
                            "checkpoint_response_details": {
                                "General_Cleaning_name": "tables/ Fruits Disinfection Treatment",
                                "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                                "submitted_on": "14-Jan-2025 07:53:45PM",
                                "submitted_by": "AJITHA NEELAVARN"
                            },
                            "headers": [
                                "MOG-Name",
                                "Quantity",
                                "Unit",
                                "Start Temp",
                                "End Temp",
                                "Comment",
                                "Action Taken",
                                "Image"
                            ],
                            "response details": [
                                {
                                "MOG-Name": "Chicken Curry Cut without Skin Frozen",
                                "Quantity": "20.0",
                                "Unit": "Kgs",
                                "Start Temp": "-18.0 ",
                                "End Temp": "-18.0",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Chicken Curry Cut without Skin Frozen",
                                "Quantity": "20.0",
                                "Unit": "Kgs",
                                "Start Temp": "-18.0 ",
                                "End Temp": "-18.0",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Chicken Curry Cut without Skin Frozen",
                                "Quantity": "20.0",
                                "Unit": "Kgs",
                                "Start Temp": "-18.0 ",
                                "End Temp": "-18.0",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Chicken Curry Cut without Skin Frozen",
                                "Quantity": "20.0",
                                "Unit": "Kgs",
                                "Start Temp": "-18.0 ",
                                "End Temp": "-18.0",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Chicken Curry Cut without Skin Frozen",
                                "Quantity": "20.0",
                                "Unit": "Kgs",
                                "Start Temp": "-18.0 ",
                                "End Temp": "-18.0",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                }
                            ]
                            },
                            {
                            "code":"5",
                            "checkpoint_response_details": {
                                "General_Cleaning_name": "1234tables/ Fruits Disinfection Treatment",
                                "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                                "submitted_on": "14-Jan-2025 07:53:45PM",
                                "submitted_by": "AJITHA NEELAVARN"
                            },
                            "headers": [
                                            "question",
                                            "response",
                                            "comment",
                                            "action_taken",
                                            "image"
                             ],
                            "response details": [
                                {
                                "question": "Common touchpoints are disinfected?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "question": "Food contact surfaces",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "question": "Receiving area is clean & well maintained?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "question": "Receiving area free from pest infestation?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "question": "Receiving area free from supplier cartons",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                }
                            ]
                            }
                        ]
                            },
                            {
                                "Area name": "Pest Sighting",
                                "checkpoint_responses": []
                            },
                            {
                                "Area name": "Healthcare",
                                "checkpoint_responses": []
                            },
                            {
                                "Area name": "Staff Grooming",
                                "checkpoint_responses": []
                            }
                            ],
                        },
                        {
                        "Cafeteria Name": "Level - 7 Gateway",
                        "Areas" : [
                            {
                            "Area name": "Receiving & Stores",
                            "checkpoint_responses": [
                            {
                            "code":"11",
                            "checkpoint_response_details": {
                                "General_Cleaning_name": "tables/ Fruits Disinfection Treatment",
                                "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                                "submitted_on": "14-Jan-2025 08:15:30PM",
                                "submitted_by": "JOHN DOE"
                            },
                            "headers": [
                                "Dish-Name",
                                "Qty(inkg)",
                                "Start/End Time",
                                "Catagory",
                                "Cooking Completion temp(°C)",
                                "Reheating temp(°C)",
                                "Question",
                                "Response",
                                "Comment",
                                "Action Taken",
                                "Image"
                            ],
                            "response details": [
                                {
                                "Dish-Name":"Smbar",
                                "Qty(inkg)":"",
                                "Start/End Time":"",
                                "Catagory":"",
                                "Cooking Completion temp(°C)": "",
                                "Reheating temp(°C)": "",
                                "Question":"Select Mealtime",
                                "Response":"Breakfast",
                                "Comment":"",
                                "Action Taken":"",
                                "Image":""
                                },
                                {
                                "Dish-Name":"Sambar",
                                "Qty(inkg)":"25.0",
                                "Start/End Time":"05:54AM 07:15AM",
                                "Catagory":"Hot Veg",
                                "Cooking Completion temp(°C)": "89",
                                "Reheating temp(°C)": "",
                                "Question":"",
                                "Response":"",
                                "Comment":"",
                                "Action Taken":"",
                                "Image":""
                                },
                                {
                                "Dish-Name":"Ragi samiya",
                                "Qty(inkg)":"25.0",
                                "Start/End Time":"05:54AM 07:15AM",
                                "Catagory":"Hot Veg",
                                "Cooking Completion temp(°C)": "89",
                                "Reheating temp(°C)": "",
                                "Question":"",
                                "Response":"",
                                "Comment":"",
                                "Action Taken":"",
                                "Image":""
                                },
                                {
                                "Dish-Name":"Masala vada",
                                "Qty(inkg)":"25.0",
                                "Start/End Time":"05:54AM 07:15AM",
                                "Catagory":"Hot Veg",
                                "Cooking Completion temp(°C)": "89",
                                "Reheating temp(°C)": "",
                                "Question":"",
                                "Response":"",
                                "Comment":"",
                                "Action Taken":"",
                                "Image":""
                                },
                                {
                                "Dish-Name":"Halwa",
                                "Qty(inkg)":"25.0",
                                "Start/End Time":"05:54AM 07:15AM",
                                "Catagory":"Hot Veg",
                                "Cooking Completion temp(°C)": "89",
                                "Reheating temp(°C)": "",
                                "Question":"",
                                "Response":"",
                                "Comment":"",
                                "Action Taken":"",
                                "Image":""
                                },
                                
                            ]
                            },
                             {
                            "code":"6",
                            "checkpoint_response_details": {
                                "General_Cleaning_name": "tables/ Fruits Disinfection Treatment",
                                "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                                "submitted_on": "14-Jan-2025 08:15:30PM",
                                "submitted_by": "JOHN DOE"
                            },
                            "headers": [
                                "Dish Name",
                                "Category",
                                "Question",
                                "Response",
                                "After 90 min",
                                "Comment"
                            ],
                            "response details": [
                                {
                                "Dish Name":"",
                                "Category":"",
                                "Question":"Select Mealtime",
                                "Response":"Lunch",
                                "After 90 min":"",
                                "Comment":""
                                },
                                {
                                "Dish Name":"Chicken biryani ",
                                "Category":"Hot Non Veg ",
                                "Question":"Dish Temperature(in °C) ",
                                "Response":"77.9 ",
                                "After 90 min":"75.00",
                                "Comment":""
                                },
                                {
                                "Dish Name":"Chicken biryani ",
                                "Category":"Hot Non Veg ",
                                "Question":"Dish Temperature(in °C) ",
                                "Response":"77.9 ",
                                "After 90 min":"75.00",
                                "Comment":""
                                },
                                {
                                "Dish Name":"Chicken biryani ",
                                "Category":"Hot Non Veg ",
                                "Question":"Dish Temperature(in °C) ",
                                "Response":"77.9 ",
                                "After 90 min":"75.00",
                                "Comment":""
                                },
                                {
                                "Dish Name":"Mix vegetable paneer kurma",
                                "Category":"Hot Non Veg ",
                                "Question":"Dish Temperature(in °C) ",
                                "Response":"77.9 ",
                                "After 90 min":"75.00",
                                "Comment":""
                                },
                            ]
                            },
                              {
                            "code":"3",
                            "checkpoint_response_details": {
                                "General_Cleaning_name": "tables/ Fruits Disinfection Treatment",
                                "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                                "submitted_on": "14-Jan-2025 08:15:30PM",
                                "submitted_by": "JOHN DOE"
                            },
                            "headers": [
                                "Sub-Checkpoint",
                                "Response",
                                "Image"
                            ],
                            "response details": [
                                {
                                "Sub-Checkpoint": "Product Name",
                                "Response": "Nil",
                                "Image": ""
                                },
                                {
                                "Sub-Checkpoint": "Total Wastage (Kgs)",
                                "Response": "0",
                                "Image": ""
                                },
                                {
                                "Sub-Checkpoint": "Select Reason",
                                "Response": "Spoiled",
                                "Image": ""
                                }
                            ]
                            },
                            {
                            "checkpoint_response_details": {
                                "code":"4",
                                "General_Cleaning_name": "tables/ Fruits Disinfection Treatment",
                                "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                                "submitted_on": "14-Jan-2025 08:15:30PM",
                                "submitted_by": "JOHN DOE"
                            },
                            "headers": [
                                "Sub-Checkpoint",
                                "Quantity(in kgs)",
                                "Comment",
                                "Image"
                            ],
                            "response details": [
                                {
                                "Sub-Checkpoint": "Select Mealtime",
                                "Quantity(in kgs)": "Lunch",
                                "Comment": "Nil",
                                "Image": ""
                                },
                                {
                                "Sub-Checkpoint": "Total Wastage (Kgs)",
                                "Quantity(in kgs)": "00",
                                "Comment": "0",
                                "Image": ""
                                },
                                {
                                "Sub-Checkpoint": "Select Reason",
                                "Quantity(in kgs)": "18.300",
                                "Comment": "Spoiled",
                                "Image": ""
                                }
                            ]
                            }
                        ]  
                            },
                                                        
                            {
                            "Area name": "Receiving & Stores",
                            "checkpoint_responses": [
                            {
                            "code":"9",
                            "checkpoint_response_details": {
                                "General_Cleaning_name": "tables/ Fruits Disinfection Treatment",
                                "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                                "submitted_on": "14-Jan-2025 08:15:30PM",
                                "submitted_by": "JOHN DOE"
                            },
                            "headers": [
                                "MOG-Name",
                                "Unit",
                                "Duration",
                                "Sanitizer Concentration",
                                "Sub-Checkpoint",
                                "Response",
                                "Comment",
                                "Action Taken",
                                "Image"
                            ],
                            "response details": [
                                {
                                "MOG-Name": "Potato Fresh",
                                "Quantity": "30.0",
                                "Unit": "Kgs",
                                "Duration": "10 Min",
                                "Sanitizer Concentration": "40 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Potato Fresh",
                                "Quantity": "30.0",
                                "Unit": "Kgs",
                                "Duration": "10 Min",
                                "Sanitizer Concentration": "40 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Potato Fresh",
                                "Quantity": "30.0",
                                "Unit": "Kgs",
                                "Duration": "10 Min",
                                "Sanitizer Concentration": "40 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Onion Fresh",
                                "Quantity": "50.0",
                                "Unit": "Kgs",
                                "Duration": "12 Min",
                                "Sanitizer Concentration": "60 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                }
                            ]
                            },
                             {
                            "code":"9",     
                            "checkpoint_response_details": {
                                "General_Cleaning_name": "tables/ Fruits Disinfection Treatment",
                                "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                                "submitted_on": "14-Jan-2025 08:15:30PM",
                                "submitted_by": "JOHN DOE"
                            },
                            "headers": [
                                "MOG-Name",
                                "Unit",
                                "Duration",
                                "Sanitizer Concentration",
                                "Sub-Checkpoint",
                                "Response",
                                "Comment",
                                "Action Taken",
                                "Image"
                            ],
                            "response details": [
                                {
                                "MOG-Name": "Potato Fresh",
                                "Quantity": "30.0",
                                "Unit": "Kgs",
                                "Duration": "10 Min",
                                "Sanitizer Concentration": "40 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Potato Fresh",
                                "Quantity": "30.0",
                                "Unit": "Kgs",
                                "Duration": "10 Min",
                                "Sanitizer Concentration": "40 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Potato Fresh",
                                "Quantity": "30.0",
                                "Unit": "Kgs",
                                "Duration": "10 Min",
                                "Sanitizer Concentration": "40 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Onion Fresh",
                                "Quantity": "50.0",
                                "Unit": "Kgs",
                                "Duration": "12 Min",
                                "Sanitizer Concentration": "60 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                }
                            ]
                            },
                              {
                            "code":"9",
                            "checkpoint_response_details": {
                                "General_Cleaning_name": "tables/ Fruits Disinfection Treatment",
                                "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                                "submitted_on": "14-Jan-2025 08:15:30PM",
                                "submitted_by": "JOHN DOE"
                            },
                            "headers": [
                                "MOG-Name",
                                "Unit",
                                "Duration",
                                "Sanitizer Concentration",
                                "Sub-Checkpoint",
                                "Response",
                                "Comment",
                                "Action Taken",
                                "Image"
                            ],
                            "response details": [
                                {
                                "MOG-Name": "Potato Fresh",
                                "Quantity": "30.0",
                                "Unit": "Kgs",
                                "Duration": "10 Min",
                                "Sanitizer Concentration": "40 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Onion Fresh",
                                "Quantity": "50.0",
                                "Unit": "Kgs",
                                "Duration": "12 Min",
                                "Sanitizer Concentration": "60 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                }
                            ]
                            },
                               {
                            "code":"8",
                            "checkpoint_response_details": {
                                "General_Cleaning_name": "tables/ Fruits Disinfection Treatment",
                                "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                                "submitted_on": "14-Jan-2025 08:15:30PM",
                                "submitted_by": "JOHN DOE"
                            },
                            "headers": [
                                "MOG-Name",
                                "Quantity",
                                "Unit",
                                "Minute",
                                "Question",
                                "Response",
                                "Comment",
                                "Image"
                            ],
                            "response details": [
                                {
                                "MOG-Name": "Potato Fresh",
                                "Quantity": "30.0",
                                "Unit": "Kgs",
                                "Duration": "10 Min",
                                "Sanitizer Concentration": "40 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                },
                                {
                                "MOG-Name": "Onion Fresh",
                                "Quantity": "50.0",
                                "Unit": "Kgs",
                                "Duration": "12 Min",
                                "Sanitizer Concentration": "60 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                                }
                            ]
                            }
                        ]  
                            },
                            {
                                "Area name": "Pest Sighting",
                                "checkpoint_responses": []
                            },
                            {
                                "Area name": "Healthcare",
                                "checkpoint_responses": []
                            },
                            {
                                "Area name": "Staff Grooming",
                                "checkpoint_responses": []
                            }

                        ]
                        }
                    ]
                    }

    report.generate_report(report_data)