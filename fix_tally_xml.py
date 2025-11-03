"""
Fix existing Tally XML file to work with any Financial Year
This script modifies the XML to add extended date range
"""

import os
import re
from datetime import datetime

print("="*80)
print("🔧 TALLY XML FIXER - Auto FY Range")
print("="*80)

# Find the most recent Tally XML file in Downloads or current directory
possible_paths = [
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Desktop"),
    "."
]

xml_files = []
for path in possible_paths:
    if os.path.exists(path):
        for file in os.listdir(path):
            if file.endswith('.xml') and 'tally' in file.lower():
                full_path = os.path.join(path, file)
                xml_files.append((full_path, os.path.getmtime(full_path)))

if not xml_files:
    print("❌ No Tally XML files found!")
    print("\n📝 Please enter the full path to your Tally XML file:")
    xml_path = input("> ").strip().strip('"')
else:
    # Sort by modification time (most recent first)
    xml_files.sort(key=lambda x: x[1], reverse=True)
    xml_path = xml_files[0][0]
    print(f"\n✅ Found XML file: {xml_path}")
    print(f"   Modified: {datetime.fromtimestamp(xml_files[0][1]).strftime('%Y-%m-%d %H:%M:%S')}")

if not os.path.exists(xml_path):
    print(f"❌ File not found: {xml_path}")
    exit(1)

# Read the XML file
print(f"\n📖 Reading XML file...")
with open(xml_path, 'r', encoding='utf-8') as f:
    xml_content = f.read()

# Extract all dates from vouchers to calculate range
date_pattern = r'<DATE>(\d{8})</DATE>'
dates = re.findall(date_pattern, xml_content)

if dates:
    # Convert YYYYMMDD to datetime objects
    date_objects = []
    for date_str in dates:
        try:
            year = int(date_str[0:4])
            month = int(date_str[4:6])
            day = int(date_str[6:8])
            date_objects.append(datetime(year, month, day))
        except:
            pass
    
    if date_objects:
        earliest = min(date_objects)
        latest = max(date_objects)
        
        print(f"\n📅 Invoice Date Range:")
        print(f"   Earliest: {earliest.strftime('%Y-%m-%d')}")
        print(f"   Latest: {latest.strftime('%Y-%m-%d')}")
        
        # Set FY to cover all dates (1 year before earliest to 2 years after latest)
        fy_start_year = earliest.year - 1
        fy_end_year = latest.year + 2
        
        fy_start = f"{fy_start_year:04d}0401"  # 1st April
        fy_end = f"{fy_end_year:04d}0331"      # 31st March
        
        print(f"\n✅ Setting Financial Year:")
        print(f"   From: {fy_start_year}-04-01")
        print(f"   To: {fy_end_year}-03-31")
    else:
        # Fallback: 2020 to 2030
        fy_start = "20200401"
        fy_end = "20300331"
        print(f"\n⚠️  Could not detect dates, using wide range: 2020-2030")
else:
    # Fallback: 2020 to 2030
    fy_start = "20200401"
    fy_end = "20300331"
    print(f"\n⚠️  No dates found in XML, using wide range: 2020-2030")

# Fix the STATICVARIABLES section
if '<STATICVARIABLES>' in xml_content:
    # Find the STATICVARIABLES block
    pattern = r'(<STATICVARIABLES>)(.*?)(</STATICVARIABLES>)'
    
    def replace_static_vars(match):
        opening = match.group(1)
        content = match.group(2)
        closing = match.group(3)
        
        # Remove existing PERIOD tags if present
        content = re.sub(r'\s*<PERIODSTARTDATE>.*?</PERIODSTARTDATE>', '', content)
        content = re.sub(r'\s*<PERIODENDDATE>.*?</PERIODENDDATE>', '', content)
        
        # Add new PERIOD tags
        new_content = content + f'\n          <PERIODSTARTDATE>{fy_start}</PERIODSTARTDATE>\n          <PERIODENDDATE>{fy_end}</PERIODENDDATE>'
        
        return opening + new_content + '\n        ' + closing
    
    xml_content = re.sub(pattern, replace_static_vars, xml_content, flags=re.DOTALL)
    print(f"   ✅ Added PERIOD tags to STATICVARIABLES")
else:
    print(f"   ⚠️  Could not find STATICVARIABLES section")

# Fix any blank vendor names (Master name is missing error)
blank_ledger_pattern = r'<LEDGERNAME>\s*</LEDGERNAME>'
blank_count = len(re.findall(blank_ledger_pattern, xml_content))
if blank_count > 0:
    xml_content = re.sub(blank_ledger_pattern, '<LEDGERNAME>Unknown Vendor</LEDGERNAME>', xml_content)
    print(f"   ✅ Fixed {blank_count} blank vendor names")

# Fix any blank party ledger names
blank_party_pattern = r'<PARTYLEDGERNAME>\s*</PARTYLEDGERNAME>'
blank_party_count = len(re.findall(blank_party_pattern, xml_content))
if blank_party_count > 0:
    xml_content = re.sub(blank_party_pattern, '<PARTYLEDGERNAME>Unknown Vendor</PARTYLEDGERNAME>', xml_content)
    print(f"   ✅ Fixed {blank_party_count} blank party ledger names")

# Save the fixed XML
output_path = xml_path.replace('.xml', '_FIXED.xml')
print(f"\n💾 Saving fixed XML...")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(xml_content)

print(f"   ✅ Saved to: {output_path}")

print("\n" + "="*80)
print("✅ XML FILE FIXED SUCCESSFULLY!")
print("="*80)
print("\n📋 NEXT STEPS:")
print("1. In Tally Prime:")
print("   - Press O (Import)")
print("   - Click 'Transactions'")
print(f"   - Select file: {os.path.basename(output_path)}")
print("   - Press Enter")
print("\n2. All invoices should import WITHOUT errors now!")
print("="*80)

# Open the folder containing the file
import subprocess
folder_path = os.path.dirname(output_path)
print(f"\n📂 Opening folder: {folder_path}")
try:
    subprocess.run(['explorer', folder_path], shell=True)
except:
    pass
