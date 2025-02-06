# table_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap

class TableGenerator:
    def __init__(self, checkpoint_response_details, page_width, page_height):
        self.pdf = checkpoint_response_details
        self.page_width = page_width
        self.page_height = page_height
        
    def generate_table(self, table_data, y_position, styles="Helvetica"):
        
        table_column_widths = {
            
            "3":  [250, 100, 60],
            "4":  [200, 100, 80,80],
            "5":  [250, 60, 60, 90, 100],
            "6":  [100, 60, 140, 90, 90, 60],
            "7":  [100, 60, 80, 90, 90, 60, 50],
            "8":  [120, 60, 40, 70, 80, 60, 50, 50],
            "9":  [70, 40, 40, 50, 140, 60, 50, 50, 80],
            "10": [70, 30, 30, 50, 80, 80, 50, 50, 50,60],
            "11": [50, 30, 50, 50, 60, 60, 50, 50, 50,50,40]
        }
        
        table_code = table_data["code"]
        column_widths = table_column_widths[table_code]


        self.pdf.setFont(styles, 10)

        # Check if there is enough space, otherwise start a new page
        if y_position < 150:
            self.pdf.showPage()  # Start a new page
            y_position = self.page_height - 50  # Reset y_position

        # Background for site details section
        self.pdf.setFillColor((0.8, 0.9, 1))  
        self.pdf.rect(28, y_position - 40, self.page_width - 60, 40, fill=1, stroke=0)
        self.pdf.setFillColor((0, 0, 0))

        general_cleaning_name = table_data["checkpoint_response_details"]["General_Cleaning_name"]
        receiving_text = table_data["checkpoint_response_details"]["Receiving_text"]
        submitted_on = table_data["checkpoint_response_details"]["submitted_on"]
        submitted_by = table_data["checkpoint_response_details"]["submitted_by"]

        self.pdf.drawString(32, y_position - 20, f"General Cleaning: {general_cleaning_name}")
        self.pdf.setFont("Helvetica", 10)
        self.pdf.drawString(33, y_position - 35, receiving_text)
        self.pdf.drawString(self.page_width - 220, y_position - 20, f"Submitted On: {submitted_on}")
        self.pdf.drawString(self.page_width - 220, y_position - 35, f"Submitted By: {submitted_by}")

        y_position -= 60

        headers = table_data["headers"]
        max_header_lines = 1
        wrapped_headers = []

        for i, title in enumerate(headers):
            wrapped_header = wrap(title, width=int(column_widths[i] // 7))
            wrapped_headers.append(wrapped_header)
            max_header_lines = max(max_header_lines, len(wrapped_header))

        header_y_position = y_position

        # Check space for headers, if needed add a new page
        if header_y_position - (max_header_lines * 12) < 100:
            self.pdf.showPage()  
            y_position = self.page_height - 50  
            header_y_position = y_position

        for line_idx in range(max_header_lines):
            for i, wrapped_header in enumerate(wrapped_headers):
                if line_idx < len(wrapped_header):
                    self.pdf.setFont(styles, 10)
                    self.pdf.drawString(30 + sum(column_widths[:i]), header_y_position, wrapped_header[line_idx])
            header_y_position -= 12

        self.pdf.line(30, header_y_position - 5, self.page_width - 30, header_y_position - 5)
        y_position = header_y_position - 20

        for row in table_data["response details"]:
            max_lines = 1
            row_y_position = y_position

            # **Check before adding new rows**
            if row_y_position - 20 < 100:
                self.pdf.showPage()
                y_position = self.page_height - 50  
                row_y_position = y_position

            for i, key in enumerate(headers):
                text = str(row.get(key, ""))
                wrapped_text = wrap(text, width=int(column_widths[i] // 7))

                for j, line in enumerate(wrapped_text):
                    self.pdf.setFont(styles, 10)
                    self.pdf.drawString(30 + sum(column_widths[:i]), row_y_position - (j * 12), line)

                max_lines = max(max_lines, len(wrapped_text))

            y_position -= max_lines * 14

        return y_position