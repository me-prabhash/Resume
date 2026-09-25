"""
HTML to ATS-friendly PDF converter.

Uses Playwright (headless Chromium) to render the HTML and produce a PDF
with real embedded text that ATS systems can parse.

Usage:
    python convert_to_pdf.py
    python convert_to_pdf.py path/to/resume.html path/to/output.pdf
"""

import sys
import os
import logging
from playwright.sync_api import sync_playwright

logging.getLogger('pdfminer').setLevel(logging.ERROR)

# Defaults
DEFAULT_HTML = os.path.join(
    os.path.dirname(__file__), 'Resume', 'Prabhash_Thakur_Resume.html'
)
DEFAULT_PDF = os.path.join(
    os.path.dirname(__file__), 'Resume', 'Prabhash Thakur Resume.pdf'
)


def convert_html_to_pdf(html_path, pdf_path):
    html_path = os.path.abspath(html_path)
    pdf_path = os.path.abspath(pdf_path)

    if not os.path.exists(html_path):
        print(f"ERROR: HTML file not found: {html_path}")
        return False

    file_url = 'file:///' + html_path.replace('\\', '/')

    print(f"Converting: {html_path}")
    print(f"Output:     {pdf_path}")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Load the HTML file
        page.goto(file_url, wait_until='networkidle')

        # Wait for fonts to load
        page.wait_for_timeout(2000)

        # Generate PDF with proper margins and footer
        page.pdf(
            path=pdf_path,
            format='A4',
            margin={
                'top': '20mm',
                'right': '15mm',
                'bottom': '20mm',
                'left': '15mm',
            },
            print_background=True,
        )

        browser.close()

    # Verify the PDF has extractable text
    file_size = os.path.getsize(pdf_path)
    print(f"PDF created: {file_size:,} bytes")

    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            total_chars = 0
            for pg in pdf.pages:
                text = pg.extract_text()
                if text:
                    total_chars += len(text)
            if total_chars > 100:
                print(f"Text check: PASS ({total_chars:,} characters extracted)")
                print("This PDF is ATS-readable.")
            else:
                print(f"Text check: WARNING (only {total_chars} characters found)")
                print("ATS systems may not be able to read this PDF.")
    except ImportError:
        print("(Install pdfplumber to verify text extraction)")

    return True


if __name__ == '__main__':
    html_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HTML
    pdf_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PDF

    success = convert_html_to_pdf(html_path, pdf_path)
    if success:
        print("\nDone! You can now submit this PDF to ATS systems.")
    else:
        sys.exit(1)
