"""
Quick script to extract text from the uploaded tax.pdf
"""
import PyPDF2
import sys

pdf_path = r"c:\Users\akib\Downloads\tax.pdf"

try:
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        print("=" * 80)
        print(f" PDF TEXT EXTRACTION - {pdf_path}")
        print("=" * 80)
        print(f"Number of pages: {len(pdf_reader.pages)}\n")
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            
            print(f"\n--- PAGE {page_num + 1} ---")
            print(text)
            print("\n" + "-" * 80)
            
except Exception as e:
    print(f"Error: {e}")
    print("\nTrying to install PyPDF2...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "PyPDF2"])
    print("\nPlease run this script again after installation.")
