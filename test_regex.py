"""Test invoice number extraction from filenames"""
import re

filenames = [
    "2025-09-01T10-20 Tax invoice #24347159344967481-24160039583679457.pdf",
    "2025-09-01T16-57 Tax invoice #24105611812455566-24105611835788897.pdf",
    "WhatsApp Image 2025-10-12 at 11.55.50_85ce5a7a.jpg"
]

print("=" * 70)
print(" TESTING INVOICE NUMBER EXTRACTION")
print("=" * 70)
print()

for filename in filenames:
    print(f"File: {filename}")
    print("-" * 70)
    
    # Current regex (WRONG - matches dates too!)
    current_match = re.search(r'#?([\d-]+)', filename)
    print(f"  Current regex '#?([\d-]+)': {current_match.group(1) if current_match else 'Not found'}")
    
    # Better regex - only after # symbol
    invoice_match = re.search(r'#(\d+)', filename)
    print(f"  Better regex '#(\d+)': {invoice_match.group(1) if invoice_match else 'Not found'}")
    
    # Extract first number after #
    invoice_full = re.search(r'#([\d-]+)', filename)
    print(f"  Full after # '#([\d-]+)': {invoice_full.group(1) if invoice_full else 'Not found'}")
    
    # Date extraction
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    print(f"  Date: {date_match.group(1) if date_match else 'Not found'}")
    
    print()

print("\n" + "=" * 70)
print(" RECOMMENDATION: Use '#(\d+)' to get first number after #")
print("=" * 70)
