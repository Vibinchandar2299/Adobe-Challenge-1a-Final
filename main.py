import os
import json
from src.core import PDFOutlineExtractor

def process_single_pdf(pdf_path):
    """Processes a single PDF file and returns its extracted outline."""
    extractor = PDFOutlineExtractor()
    outline = extractor.extract_outline(pdf_path)
    return outline

def process_directory(input_dir, output_dir):
    """Processes all PDF files in an input directory and saves outlines to an output directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir}.")
        return

    print(f"Found {len(pdf_files)} PDF files in {input_dir}. Starting extraction...")

    for pdf_file_name in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file_name)
        print(f"Processing: {pdf_file_name}")
        
        outline = process_single_pdf(pdf_path)
        
        output_file_name = os.path.splitext(pdf_file_name)[0] + '.json'
        output_path = os.path.join(output_dir, output_file_name)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(outline, f, indent=4, ensure_ascii=False)
            print(f"Extracted outline saved to: {output_file_name}")
        except Exception as e:
            print(f"Error saving outline for {pdf_file_name}: {e}")
    
    print("Extraction complete.")

if __name__ == "__main__":
    # Example Usage:
    # Place your PDF files in the 'data' folder
    # The JSON outputs will be saved in the 'output' folder

    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_pdf_dir = os.path.join(current_dir, 'data')
    output_json_dir = os.path.join(current_dir, 'output')

    # Create 'data' directory if it doesn't exist
    if not os.path.exists(input_pdf_dir):
        os.makedirs(input_pdf_dir)
        print(f"Created input directory: {input_pdf_dir}")
        print("Please place your PDF files into the 'data' folder and run the script again.")
        exit()

    process_directory(input_pdf_dir, output_json_dir)

    # To process a specific file (uncomment and modify as needed):
    # single_pdf_path = os.path.join(input_pdf_dir, "file03.pdf")
    # if os.path.exists(single_pdf_path):
    #     outline = process_single_pdf(single_pdf_path)
    #     print("\n--- Extracted Outline for Single PDF ---")
    #     print(json.dumps(outline, indent=4, ensure_ascii=False))
    # else:
    #     print(f"Single PDF not found at {single_pdf_path}")