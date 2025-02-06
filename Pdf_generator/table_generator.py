# table_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap
import json

class TableGenerator:
    def __init__(self, pdf, page_width, page_height):  # Corrected pdf argument name
        self.pdf = pdf
        self.page_width = page_width
        self.page_height = page_height

    def generate_table(self, table_data, y_position, styles="Helvetica"):
        # Load JSON data from the file
        file_path = "Pdf_generator/table_config.json"
        
        with open(file_path, "r") as json_file:
            table_conf = json.load(json_file)
    
        table_code = table_data["code"]
        # Accessing the column widths using the table_code
        column_widths = table_conf["table_column_widths"][str(table_code)]

        self.pdf.setFont("Helvetica", 10)  # Set default font here

        if y_position < 150:
            self.pdf.showPage()
            y_position = self.page_height - 50

        # Background for checkpoint details
        self.pdf.setFillColor((0.8, 0.9, 1))
        self.pdf.rect(28, y_position - 40, self.page_width - 60, 40, fill=1, stroke=0)
        self.pdf.setFillColor((0, 0, 0))

        general_cleaning_name = table_data["General_Cleaning_name"]  # Access directly
        receiving_text = table_data["Receiving_text"]  # Access directly
        submitted_on = table_data["submitted_on"]  # Access directly
        submitted_by = table_data["submitted_by"]  # Access directly

        self.pdf.drawString(32, y_position - 20, f"General Cleaning: {general_cleaning_name}")
        self.pdf.setFont("Helvetica", 10)
        self.pdf.drawString(33, y_position - 35, receiving_text)
        self.pdf.drawString(self.page_width - 220, y_position - 20, f"Submitted On: {submitted_on}")
        self.pdf.drawString(self.page_width - 220, y_position - 35, f"Submitted By: {submitted_by}")

        y_position -= 60

        headers = table_conf["table_headers"][str(table_code)]
        max_header_lines = 1
        wrapped_headers = []

        for i, title in enumerate(headers):
            wrapped_header = wrap(title, width=int(column_widths[i] // 7))
            wrapped_headers.append(wrapped_header)
            max_header_lines = max(max_header_lines, len(wrapped_header))

        header_y_position = y_position

        if header_y_position - (max_header_lines * 12) < 100:
            self.pdf.showPage()
            y_position = self.page_height - 50
            header_y_position = y_position

        for line_idx in range(max_header_lines):
            for i, wrapped_header in enumerate(wrapped_headers):
                if line_idx < len(wrapped_header):
                    self.pdf.setFont("Helvetica", 10)
                    self.pdf.drawString(30 + sum(column_widths[:i]), header_y_position, wrapped_header[line_idx])
            header_y_position -= 12

        self.pdf.line(30, header_y_position - 5, self.page_width - 30, header_y_position - 5)
        y_position = header_y_position - 20

        for response_id, row in table_data["response details"].items():  # Iterate through responses using .items()
            max_lines = 1
            row_y_position = y_position

            if row_y_position - 20 < 100:
                self.pdf.showPage()
                y_position = self.page_height - 50
                row_y_position = y_position

            for i, key in enumerate(headers):
                text = str(row.get(key.lower(), row.get(key, "")))  # Case-insensitive key lookup
                wrapped_text = wrap(text, width=int(column_widths[i] // 7))

                for j, line in enumerate(wrapped_text):
                    self.pdf.setFont("Helvetica", 10)
                    self.pdf.drawString(30 + sum(column_widths[:i]), row_y_position - (j * 12), line)

                max_lines = max(max_lines, len(wrapped_text))

            y_position -= max_lines * 14

        return y_position