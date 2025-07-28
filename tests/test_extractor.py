import pytest
import os
import json
from src.core import PDFOutlineExtractor
from src.utils import load_settings # To ensure settings load correctly

# Define paths relative to the test file
TEST_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
EXPECTED_OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'expected_outputs') # Create this folder

# Create an 'expected_outputs' folder in the project root and place your reference JSONs there
# e.g., expected_outputs/file01.json, expected_outputs/file02.json etc.

@pytest.fixture(scope="module")
def extractor():
    """Provides a fresh extractor instance for tests."""
    # Ensure settings are loaded before tests run
    _ = load_settings() 
    return PDFOutlineExtractor()

def load_expected_json(filename):
    """Loads an expected JSON output file."""
    path = os.path.join(EXPECTED_OUTPUT_DIR, filename)
    if not os.path.exists(path):
        pytest.skip(f"Expected output file not found: {path}. Skipping test.")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# List of PDFs to test with their corresponding expected JSONs
# You need to ensure these PDFs are in the 'data' folder and their JSONs in 'expected_outputs'
test_cases = [
    ("file01.pdf", "file01.json"),
    ("file02.pdf", "file02.json"),
    ("file03.pdf", "file03.json"),
    ("file04.pdf", "file04.json"),
    ("file05.pdf", "file05.json")
]

@pytest.mark.parametrize("pdf_file, expected_json_file", test_cases)
def test_pdf_outline_extraction(extractor, pdf_file, expected_json_file):
    pdf_path = os.path.join(DATA_DIR, pdf_file)
    if not os.path.exists(pdf_path):
        pytest.fail(f"Test PDF file not found: {pdf_path}")

    extracted_outline = extractor.extract_outline(pdf_path)
    expected_outline = load_expected_json(expected_json_file)

    # Basic comparison: Check title
    assert extracted_outline.get("title") == expected_outline.get("title"), \
        f"Title mismatch for {pdf_file}"

    # Compare outlines: This is more complex due to potential order/level differences
    # For a robust comparison, you might need to sort lists or compare sets of dicts
    # For now, a simple direct comparison of the list of dictionaries
    # NOTE: Floating point differences in coordinates from PyMuPDF might slightly alter order
    # if heuristics rely on precise positions. This basic comparison might fail if order differs.
    
    # A more robust comparison:
    # 1. Sort both lists by page then text to handle potential order variations
    extracted_outline_sorted = sorted(extracted_outline.get("outline", []), key=lambda x: (x.get('page',0), x.get('text','')))
    expected_outline_sorted = sorted(expected_outline.get("outline", []), key=lambda x: (x.get('page',0), x.get('text','')))

    assert len(extracted_outline_sorted) == len(expected_outline_sorted), \
        f"Outline length mismatch for {pdf_file}. Expected {len(expected_outline_sorted)}, Got {len(extracted_outline_sorted)}"
    
    # Compare each item
    for i in range(len(extracted_outline_sorted)):
        # Allow some flexibility in H-level assignment for the general model,
        # but ensure text and page are correct.
        # You might adjust this assertion based on how strict you want the level comparison.
        assert extracted_outline_sorted[i].get("text") == expected_outline_sorted[i].get("text"), \
            f"Text mismatch at index {i} for {pdf_file}. Expected '{expected_outline_sorted[i].get('text')}', Got '{extracted_outline_sorted[i].get('text')}'"
        assert extracted_outline_sorted[i].get("page") == expected_outline_sorted[i].get("page"), \
            f"Page mismatch at index {i} for {pdf_file} for text '{expected_outline_sorted[i].get('text')}'"
        
        # If the level is 'H_UNKNOWN' from the general model, it implies an imperfect match
        if extracted_outline_sorted[i].get("level") == "H_UNKNOWN":
            print(f"Warning: H_UNKNOWN level for '{extracted_outline_sorted[i].get('text')}' in {pdf_file}")
            # Consider this a soft fail or a warning in a real project, but for now it will fail the assertion
            # unless you specifically allow H_UNKNOWN to match any H-level from expected.
        
        # For stricter level comparison:
        assert extracted_outline_sorted[i].get("level") == expected_outline_sorted[i].get("level"), \
            f"Level mismatch at index {i} for {pdf_file} for text '{expected_outline_sorted[i].get('text')}'." \
            f" Expected '{expected_outline_sorted[i].get('level')}', Got '{extracted_outline_sorted[i].get('level')}'"