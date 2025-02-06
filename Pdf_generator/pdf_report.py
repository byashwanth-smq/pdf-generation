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

        for cafe_id, cafe_data in report_data["cafes"].items():  # Iterate through cafes (using items())
            self.pdf_gen.add_footer()
            if current_y_position < 150:
                self.pdf_gen.new_page()
                current_y_position = self.pdf_gen.page_height + 30

            current_y_position -= 25
            self.add_cafeteria_name(cafe_data["Cafeteria Name"], current_y_position - 10)

            for area_name, area_data in cafe_data["Areas"].items():  # Iterate through areas
                if current_y_position < 150:
                    self.pdf_gen.new_page()
                    current_y_position = self.pdf_gen.page_height + 100

                self.add_section_header(area_name, current_y_position - 120)
                current_y_position -= 30

                for checkpoint_id, checkpoint_response in area_data.items():  # Iterate through checkpoints
                    self.pdf_gen.add_footer()
                    if current_y_position < 150:
                        self.pdf_gen.new_page()
                        current_y_position = self.pdf_gen.page_height + 100

                    current_y_position = table_generator.generate_table(checkpoint_response, y_position=current_y_position - 125)
                    current_y_position += 80

        if current_y_position < 150:
            self.pdf_gen.new_page()
            current_y_position = self.pdf_gen.page_height + 10

        self.pdf_gen.draw_footer_text(current_y_position - 120, Verified_By=report_data["Verified By"])
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
                "Verified By": "UM",
                "cafes": {
                    "1082": {
                    "Cafeteria Name": "Level - 6 Embassy",
                    "Areas": {
                        "Receiving & Stores": {
                        "00000000-0000-4000-80d4-00001d9353e7": {
                            "code": "5",
                            "General_Cleaning_name": "General Cleaning: Receiving",
                            "Receiving_text": "HSEQ-FS/F/SOP-34",
                            "submitted_on": "14-Jan-2025 07:53:45PM",
                            "submitted_by": "AJITHA NEELAVARN",
                            "response details": {
                            "00000000-0000-4000-80d4-0000009353e7": {
                                "question": "Common touchpoints are disinfected?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            },
                            "00000000-0000-4000-80d4-00023409353e7": {
                                "question": "Food contact surfaces like crates/pallets, trolleys,",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            },
                            "00000000-0000-4000-80d4-0000009353e8": {
                                "question": "Receiving area is free from supplier cartons or if",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            }
                            }
                        },
                        "00000000-0000-4000-80d4-56701d9353e7": {
                            "code": "10",
                            "General_Cleaning_name": "Eggs Disinfection Treatment",
                            "Receiving_text": "HSEQ-FS/F/SOP-4,5",
                            "submitted_on": "14-Jan-2025 07:53:45PM",
                            "submitted_by": "AJITHA NEELAVARN",
                            "response details": {
                            "00000000-0000-4000-80d4-0000009353e8": {
                                "MOG-Name": "Egg Whole White",
                                "Quantity": "1000.0",
                                "Unit": "Pieces",
                                "Duration": "20 Sec",
                                "Sanitizer Concentration": "50 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            }
                            }
                        },
                        "00000000-0000-4000-80d4-00001d935547": {
                            "code": "5",
                            "General_Cleaning_name": "General Cleaning: Stores",
                            "Receiving_text": "HSEQ-FS/F/SOP-34",
                            "submitted_on": "14-Jan-2025 07:53:45PM",
                            "submitted_by": "AJITHA NEELAVARN",
                            "response details": {
                            "00000000-0000-4000-80d4-0000009353e7": {
                                "question": "Common touchpoints are disinfected?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            },
                            "00000000-0000-4000-80d4-21000093432e7": {
                                "question": "Walls, ceilings, floor & doors are cleaned ",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            },
                            "00000000-0000-4000-80d4-0000009353e8": {
                                "question": "Food contact surfaces cleaned?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            }
                            }
                        }
                        },
                        "Kichan": {
                        "00000000-0000-4000-80d4-00001d9353e7": {
                            "code": "5",
                            "General_Cleaning_name": "Vegetables/ Fruits Disinfection Treatment",
                            "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                            "submitted_on": "14-Jan-2025 07:53:45PM",
                            "submitted_by": "AJITHA NEELAVARN",
                            "response details": {
                            "00000000-0000-4000-80d4-0000009353e7": {
                                "question": "Common touchpoints are disinfected?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            },
                            "00000000-0000-4000-80d4-0000009353e8": {
                                "question": "Food contact surfaces cleaned?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            }
                            }
                        },
                        "00000000-0000-4000-80d4-56701d9353e7": {
                            "code": "10",
                            "General_Cleaning_name": "Eggs Disinfection Treatment",
                            "Receiving_text": "HSEQ-FS/F/SOP-4,5",
                            "submitted_on": "14-Jan-2025 07:53:45PM",
                            "submitted_by": "AJITHA NEELAVARN",
                            "response details": {
                            "00000000-0000-4000-80d4-0000009353e8": {
                                "MOG-Name": "Egg Whole White",
                                "Quantity": "1000.0",
                                "Unit": "Pieces",
                                "Duration": "20 Sec",
                                "Sanitizer Concentration": "50 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            }
                            }
                        }
                        },
                        "Pest Sighting": {
                        
                        },
                        "Healthcare": {
                        
                        },
                        "Service": {
                        
                        }
                    }
                    },
                    "1085": {
                    "Cafeteria Name": "Level - 6 Embassy",
                    "Areas": {
                        "Receiving & Stores": {
                        "00000000-0000-4000-80d4-00001d9353e7": {
                            "code": "5",
                            "General_Cleaning_name": "Vegetables/ Fruits Disinfection Treatment",
                            "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                            "submitted_on": "14-Jan-2025 07:53:45PM",
                            "submitted_by": "AJITHA NEELAVARN",
                            "response details": {
                            "00000000-0000-4000-80d4-0000009353e7": {
                                "question": "Common touchpoints are disinfected?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            },
                            "00000000-0000-4000-80d4-0000009353e8": {
                                "question": "Food contact surfaces cleaned?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            }
                            }
                        },
                        "00000000-0000-4000-80d4-56701d9353e7": {
                            "code": "10",
                            "General_Cleaning_name": "Eggs Disinfection Treatment",
                            "Receiving_text": "HSEQ-FS/F/SOP-4,5",
                            "submitted_on": "14-Jan-2025 07:53:45PM",
                            "submitted_by": "AJITHA NEELAVARN",
                            "response details": {
                            "00000000-0000-4000-80d4-0000009353e8": {
                                "MOG-Name": "Egg Whole White",
                                "Quantity": "1000.0",
                                "Unit": "Pieces",
                                "Duration": "20 Sec",
                                "Sanitizer Concentration": "50 PPM",
                                "Sub-Checkpoint": "Is following procedure compliant?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            }
                            }
                        }
                        },
                        "Pest Sighting": {
                        
                        },
                        "Healthcare": {
                        
                        }
                    }
                    },
                    "123N": {
                    "Cafeteria Name": "Level - 6 Embassy",
                    "Areas": {
                        "Receiving & Stores": {
                        "00000000-0000-4000-80d4-00001d9353e7": {
                            "code": "5",
                            "General_Cleaning_name": "Vegetables/ Fruits Disinfection Treatment",
                            "Receiving_text": "HSEQ-FS/F/SOP -4 &5",
                            "submitted_on": "14-Jan-2025 07:53:45PM",
                            "submitted_by": "AJITHA NEELAVARN",
                            "response details": {
                            "00000000-0000-4000-80d4-0000009353e7": {
                                "question": "Common touchpoints are disinfected?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            },
                            "00000000-0000-4000-80d4-0000009353e8": {
                                "question": "Food contact surfaces cleaned?",
                                "response": "Yes",
                                "comment": "",
                                "action_taken": "",
                                "image": ""
                            }
                            }
                        }
                        },
                        "Pest Sighting": {
                        
                        },
                        "Healthcare": {
                        
                        }
                    }
                    }
                }
                }
    report.generate_report(report_data)