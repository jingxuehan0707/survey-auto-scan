import os
import uuid
from PIL import Image
from pdf2image import convert_from_path

# Define folder paths
SCAN_FOLDER = "scan"
SURVEY_FOLDER = "survey"

def get_pdf_files(scan_folder):
    """Get a list of all PDF files in the scan folder."""
    return [file for file in os.listdir(scan_folder) if file.endswith('.pdf')]

def convert_pdf_to_images(pdf_file, scan_folder):
    """Convert a PDF file to a list of images."""
    input_path = os.path.join(scan_folder, pdf_file)
    return convert_from_path(input_path)

def process_image(image, page_index):
    """Rotate the image based on the page index and return the suffix."""
    if page_index % 2 == 0:  # Odd page
        image = image.rotate(90, expand=True)
        suffix = "p1"
    else:  # Even page
        image = image.rotate(-90, expand=True)
        suffix = "p2"
    return image, suffix

def save_image(image, survey_uuid, suffix, survey_folder, pdf_file, page_index):
    """Save the image with a UUID and suffix."""
    survey_output_path = os.path.join(
        survey_folder, f"{survey_uuid}_{suffix}.jpeg"
    )
    image.save(survey_output_path, "JPEG")
    print(f"Exported page {page_index + 1} of {pdf_file} as JPEG to '{survey_output_path}'")

def process_pdf_files(pdf_files, scan_folder, survey_folder):
    """Process each PDF file and save its pages as images."""
    for pdf_file in pdf_files:
        images = convert_pdf_to_images(pdf_file, scan_folder)
        for i, image in enumerate(images):
            if i % 2 == 0:  # Start of a new survey response
                survey_uuid = uuid.uuid4()
            image, suffix = process_image(image, i)
            save_image(image, survey_uuid, suffix, survey_folder, pdf_file, i)

def process_pdf_files(pdf_files, scan_folder, survey_folder):
    """Process each PDF file and save its pages as images."""
    for pdf_file in pdf_files:
        images = convert_pdf_to_images(pdf_file, scan_folder)
        for i, image in enumerate(images):
            if i % 2 == 0:  # Start of a new survey response
                survey_uuid = uuid.uuid4()
            image, suffix = process_image(image, i)
            save_image(image, survey_uuid, suffix, survey_folder, pdf_file, i)

def main():
    """Main function to process PDF files."""
    pdf_files = get_pdf_files(SCAN_FOLDER)
    print(pdf_files)
    process_pdf_files(pdf_files, SCAN_FOLDER, SURVEY_FOLDER)

if __name__ == "__main__":
    main()
