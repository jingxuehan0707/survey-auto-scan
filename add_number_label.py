
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def create_grid(page_width, page_height, rows, cols, margin=0.05):
    """Create a grid with margins and return centroids of each cell."""
    grid = {}
    # Calculate margins
    left_margin = page_width * margin
    right_margin = page_width * margin
    usable_width = page_width - left_margin - right_margin
    cell_width = usable_width / cols
    cell_height = page_height / rows

    cell_id = 1  # Start numbering from 1
    for col in range(cols):  # Iterate over columns first
        for row in range(rows):  # Then iterate over rows
            centroid_x = left_margin + (col * cell_width) + (cell_width / 2)
            centroid_y = page_height - ((row * cell_height) + (cell_height / 2))  # Invert Y-axis for PDF
            grid[cell_id] = (centroid_x, centroid_y)
            cell_id += 1  # Increment the cell ID
    
    return grid

def get_page_orientation(page_width, page_height):
    """Determine the orientation of the page."""
    return "Landscape" if page_width > page_height else "Portrait"

def add_numbers_to_pdf(input_pdf, output_pdf, rows=3, cols=10):
    """Add numbers to the grid cell centroids on each page of the PDF."""
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_number, page in enumerate(reader.pages, start=1):
        # Get page size
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        orientation = get_page_orientation(page_width, page_height)
        print(f"Processing page {page_number}: {page_width} x {page_height} ({orientation})")

        # Create grid and get centroids
        grid = create_grid(page_width, page_height, rows, cols)

        # Create a new PDF with numbers added
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))

        # Add numbers to the centroids
        for cell_id, (x, y) in grid.items():
            # mirror the x coordinate
            if orientation == "Landscape":
                x = page_width - x
            # off set the y coordinate 10% of the page height
            y = y - (0.05 * page_height)
            # offset the x coordinate 10% of the page width
            x = x - (0.01 * page_width)
            # Calculate the number to display
            number = int(cell_id) + (page_number - 1) * (rows * cols) + 1000
            # draw text in format '001001' with two leading zeros
            can.setFont("Helvetica", 10)
            can.saveState()
            can.translate(x, y)
            can.rotate(-90)
            can.drawString(0, 0, f"{number:06}")
            can.restoreState()

        can.save()
        packet.seek(0)

        # Merge the new PDF with the original page
        overlay_pdf = PdfReader(packet)
        page.merge_page(overlay_pdf.pages[0])
        writer.add_page(page)

    # Write the final PDF
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

if __name__ == "__main__":
    input_pdf = "mail-address-label-20250430.pdf"
    output_pdf = "mail-address-label-20250430-numbered.pdf"
    add_numbers_to_pdf(input_pdf, output_pdf)