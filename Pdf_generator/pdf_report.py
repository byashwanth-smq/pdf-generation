# checkpoint_report.py
import json
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
        self.pdf_gen.add_cafeteria_name(f"cafeteria name:  {cafeteria_name}", line_y_position)

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
            self.add_cafeteria_name(cafe_data["cafeteria_name"], current_y_position - 10)

            for area_name, area_data in cafe_data["Areas"].items():  # Iterate through areas
                if current_y_position < 150:
                    self.pdf_gen.new_page()
                    current_y_position = self.pdf_gen.page_height + 100

            current_y_position -= 25
            self.add_cafeteria_name(cafe_data["cafeteria_name"], current_y_position - 10)

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
    report = CheckpointReport(pdf_file=pdf_path)

    # Load JSON data from a file
    with open("pdf-generation.json", "r", encoding="utf-8") as json_file:
        report_data = json.load(json_file)  # Load JSON into a Python dictionary
    # Pass JSON data to the report
    report.generate_report(report_data)