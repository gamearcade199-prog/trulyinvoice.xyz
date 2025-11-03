"""
Complete Tally Removal Script
Removes all Tally references from the codebase
"""

import os
import re

print("="*80)
print("🧹 REMOVING ALL TALLY REFERENCES")
print("="*80)

files_to_clean = [
    # Main invoice page
    "frontend/src/app/invoices/page.tsx",
    
    # Utility functions
    "frontend/src/lib/invoiceUtils.ts",
    
    # SEO config files  
    "frontend/src/config/seo.config.ts",
    "frontend/src/config/seo.advanced.ts",
    
    # Homepage
    "frontend/src/components/HomePage.tsx",
    
    # Export success modal
    "frontend/src/components/ExportSuccessModal.tsx",
]

base_path = "c:\\Users\\akib\\Desktop\\trulyinvoice.xyz"

replacements = [
    # Remove Tally from function signatures
    (r"'excel' \| 'csv' \| 'tally' \| 'quickbooks'", "'excel' | 'csv' | 'quickbooks'"),
    (r"'tally' \| ", ""),
    (r" \| 'tally'", ""),
    
    # Remove Tally case statements
    (r"\s*case 'tally':[\s\S]*?break\n", ""),
    
    # Remove Tally export function calls
    (r"exportInvoicesToTallyXML", "// REMOVED: exportInvoicesToTallyXML"),
    
    # Remove Tally from titles and descriptions (case insensitive)
    (r", Tally,?", ","),
    (r"Tally,? ", ""),
    (r",? Tally", ""),
    (r"Tally XML,? ", ""),
    (r", Tally XML", ""),
    (r"Tally ERP 9,? ", ""),
    (r", Tally ERP 9", ""),
    (r"Tally Prime,? ", ""),
    (r", Tally Prime", ""),
    
    # Remove tally keywords
    (r"'invoice to tally[^']*',?\n", ""),
    (r"'[^']*tally[^']*',?\n", ""),
    (r"'[^']*Tally[^']*',?\n", ""),
    
    # Remove tally export type
    (r"exportType: 'tally',", ""),
    
    # Clean up double commas and spaces
    (r", ,", ","),
    (r",  ", ", "),
]

total_changes = 0

for file_path in files_to_clean:
    full_path = os.path.join(base_path, file_path.replace("/", "\\"))
    
    if not os.path.exists(full_path):
        print(f"⚠️  Skipping {file_path} (not found)")
        continue
    
    print(f"\n📝 Processing: {file_path}")
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    file_changes = 0
    
    for pattern, replacement in replacements:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            file_changes += len(matches)
    
    if content != original_content:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✅ Made {file_changes} changes")
        total_changes += file_changes
    else:
        print(f"   ℹ️  No changes needed")

print("\n" + "="*80)
print(f"✅ CLEANUP COMPLETE: {total_changes} changes across {len(files_to_clean)} files")
print("="*80)
print("\n📋 MANUAL CLEANUP NEEDED:")
print("1. Delete file: frontend/src/app/export/tally/page.tsx")
print("2. Remove tally section from: frontend/src/config/seo.config.ts (lines 483-487)")
print("3. Update homepage tagline to remove Tally mentions")
print("="*80)
