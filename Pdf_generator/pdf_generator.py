from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime

class PDFGenerator:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.page_width, self.page_height = A4
        self.pdf = canvas.Canvas(self.pdf_file, pagesize=A4)

    def draw_logo(self, logo_path, x_position, y_position, logo_width, logo_height):
        """
        Method to draw a logo on the PDF.
        Arguments:
        - logo_path: Path to the logo image file
        - x_position: X-coordinate for logo placement
        - y_position: Y-coordinate for logo placement
        - logo_width: Width of the logo
        - logo_height: Height of the logo
        """
        logo = ImageReader(logo_path)
        self.pdf.drawImage(logo, x_position, y_position, width=logo_width, height=logo_height)

    def add_header(self, text, font="Helvetica-Bold", font_size=18, y_position=None):
        """
        Method to add a centered header to the PDF.
        Arguments:
        - text: Text to be added as the header
        - font: Font style (default is Helvetica-Bold)
        - font_size: Font size for the header (default is 18)
        - y_position: Y-coordinate for the header position
        """
        if y_position is None:
            y_position = self.page_height - 80  # Default header position from top

        # Set the font and size
        self.pdf.setFont(font, font_size)

        # Calculate the width of the text to center it
        text_width = self.pdf.stringWidth(text, font, font_size)

        # Set the text color to black
        self.pdf.setFillColorRGB(0, 0, 0)

        # Draw the header text centered at the given position
        self.pdf.drawString((self.page_width - text_width) / 2, y_position, text)

        # Draw a horizontal line below the header
        line_y_position = y_position - 20  # Adjust the spacing
        self.pdf.line(30, line_y_position, self.page_width - 30, line_y_position)  # Horizontal line

    def add_site_details(self, site_name, site_id, report_date, line_y_position):
        """
        Method to add site details to the PDF.
        Arguments:
        - site_name: Site Name text
        - site_id: Site ID text
        - report_date: Report Date text
        - line_y_position: The Y-coordinate to position the text
        """
        # Set font for site details
        self.pdf.setFont("Helvetica", 12)

        # Add site details (left side)
        self.pdf.drawString(30, line_y_position - 20, f" Site Name  :  {site_name}" )  # Positioned below the line

        # Add site ID (right side)
        site_id_width = self.pdf.stringWidth(site_id, "Helvetica", 12)
        self.pdf.drawString(self.page_width - 80 - site_id_width, line_y_position - 20, f"Site ID :  {site_id}")  # Right aligned

        # Add report date (left side)
        self.pdf.drawString(34, line_y_position - 47, f"Report Date : {report_date}" )  # Positioned below the line

        # Draw a horizontal line below the site details
        line_y_position2 = line_y_position - 60  # Adjust the spacing for next section
        self.pdf.line(30, line_y_position2, self.page_width - 30, line_y_position2)  # Horizontal line


    def add_cafeteria_name(self, cafeteria_name, line_y_position):
        """
        Method to add cafeteria name section with a dark red background.
        Arguments:
        - cafeteria_name: Cafeteria Name text
        - line_y_position: The Y-coordinate to position the section
        """
        # Set background color (Dark Red)
        self.pdf.setFillColorRGB(0.5, 0, 0)  # Dark Red RGB value (adjust as needed)
        self.pdf.rect(30, line_y_position - 92, self.page_width - 60, 23, fill=1)  # Draw a filled rectangle

        # Set text color to white for contrast
        self.pdf.setFillColorRGB(1, 1, 1)  # White color

        # Add Cafeteria Name text
        self.pdf.setFont("Helvetica", 16)
        self.pdf.drawString(32, line_y_position - 90 + 5, cafeteria_name)  # Positioned within the rectangle

    def add_section_header(self, header_text, y_position):
        """
        Method to add a section header such as 'Receiving & Stores'
        Arguments:
        - header_text: Header text to be centered
        - y_position: Y-coordinate for the header position
        """
        # Set font for the section header
        self.pdf.setFont("Helvetica-Bold", 14)  # Arial alternative in ReportLab

        # Calculate the width of the text to center it
        text_width = self.pdf.stringWidth(header_text, "Helvetica-Bold", 14)

        # Set the text color to black
        self.pdf.setFillColorRGB(139/255, 69/255, 19/255)

        # Draw the header text centered at the given position
        self.pdf.drawString((self.page_width - text_width) / 2, y_position, header_text)

    def new_page(self):
        """Adds a new page to the PDF."""
        self.pdf.showPage()  # Finish the current page and start a new one
    
    def add_pest_sighting_text(self, y_position, text):
        """
        Method to add 'Pest Sighting' text after each cafe, centered horizontally.
        Arguments:
        - y_position: Y-coordinate for the positioning of the Pest Sighting text
        - text: Custom text to add (default is 'Pest Sighting')
        """
        # Set font for the "Pest Sighting" text
        self.pdf.setFont("Helvetica-Bold", 14)

        # Set the text color to black
        self.pdf.setFillColorRGB(139/255, 69/255, 19/255)

        # Calculate the width of the text to center it
        text_width = self.pdf.stringWidth(text, "Helvetica-Bold", 14)

        # Calculate the X position to center the text on the page
        x_position = (self.page_width - text_width) / 2

        # Draw the text at the calculated position
        self.pdf.drawString(x_position, y_position, text)
        # Set the text color to black
        self.pdf.setFillColorRGB(0, 0, 0)

        # You can add additional formatting here if required, like lines or spacing
    def draw_footer_text(self, current_y_position,Verified_By):
        
        self.pdf.setFont("Helvetica", 14)
        self.pdf.setFillColorRGB(0, 0, 0)
        # Left side: Report Downloaded On
        self.pdf.drawString(30, current_y_position - 10, "Report Downloaded On:")
        
        # Right side: Verified By
        self.pdf.drawString(self.page_width - 200, current_y_position - 10, "Verified By")
        
        # Left side: Timestamp below "Report Downloaded On"
        current_time = datetime.now().strftime("%d-%b-%Y %I:%M:%S%p")
        self.pdf.drawString(30, current_y_position - 40, current_time)
        
        # Right side: Verified By
        self.pdf.drawString(self.page_width - 180, current_y_position - 30, Verified_By)
        
        
    def add_footer(self):
        footer_y = 10  # Position for footer

        # Left-aligned copyright text
        self.pdf.setFont("Helvetica", 9)
        self.pdf.setFillColorRGB(0.5, 0.5, 0.5)  # Light gray color
        self.pdf.drawString(30, footer_y, "Copyright © 2023 Compass India Food Service Pvt. Ltd")
        self.pdf.setFillColorRGB(0, 0, 0)  # Reset to black for other text

        # Right-aligned system-generated message
        self.pdf.drawString(self.page_width - 280, footer_y, "This is a system-generated report hence signature not required")
        
    def save_pdf(self):
        """
        Method to save the generated PDF to a file.
        """
        self.pdf.save()