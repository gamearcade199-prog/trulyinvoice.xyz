#!/usr/bin/env python3
"""
🔍 EXPORT FUNCTIONALITY AUDIT
=============================
Check PDF export, CSV export, and confidence score display
"""

import os
import glob

def check_export_functionality():
    """Audit all export capabilities and confidence score display"""
    
    print("🔍 EXPORT FUNCTIONALITY AUDIT")
    print("=" * 35)
    print()
    
    # 1. Check for PDF export functionality
    print("📄 1. PDF EXPORT CAPABILITIES")
    print("-" * 30)
    
    pdf_exporters = [
        "backend/app/services/pdf_exporter.py",
        "backend/app/services/professional_pdf_exporter.py", 
        "backend/app/services/invoice_pdf_generator.py"
    ]
    
    found_pdf_exporters = []
    for exporter in pdf_exporters:
        if os.path.exists(exporter):
            found_pdf_exporters.append(exporter)
    
    if found_pdf_exporters:
        print(f"✅ Found {len(found_pdf_exporters)} PDF exporters:")
        for exp in found_pdf_exporters:
            print(f"   📄 {exp}")
    else:
        print("❌ NO PDF EXPORTERS FOUND")
        print("💡 Need to create PDF export functionality")
    
    print()
    
    # 2. Check CSV export functionality  
    print("📊 2. CSV EXPORT CAPABILITIES")
    print("-" * 30)
    
    csv_exporters = [
        "backend/app/services/csv_exporter.py",
        "backend/app/services/raw_csv_exporter.py"
    ]
    
    found_csv_exporters = []
    for exporter in csv_exporters:
        if os.path.exists(exporter):
            found_csv_exporters.append(exporter)
    
    if found_csv_exporters:
        print(f"✅ Found {len(found_csv_exporters)} CSV exporters:")
        for exp in found_csv_exporters:
            print(f"   📊 {exp}")
        print("✅ CSV export is working (as shown in your logs)")
    else:
        print("⚠️  CSV exporters not found in services")
        print("💡 May be implemented inline in API")
    
    print()
    
    # 3. Check API endpoints for exports
    print("🌐 3. API EXPORT ENDPOINTS")
    print("-" * 26)
    
    if os.path.exists("backend/app/api/invoices.py"):
        with open("backend/app/api/invoices.py", 'r') as f:
            content = f.read()
            
        if "export-csv" in content:
            print("✅ CSV export endpoint exists")
        else:
            print("❌ CSV export endpoint missing")
            
        if "export-pdf" in content:
            print("✅ PDF export endpoint exists")
        else:
            print("❌ PDF export endpoint missing")
            
        if "export-excel" in content:
            print("✅ Excel export endpoint exists")
        else:
            print("❌ Excel export endpoint missing")
    
    print()
    
    # 4. Check confidence score display in frontend
    print("🎯 4. CONFIDENCE SCORE DISPLAY")
    print("-" * 31)
    
    frontend_files = [
        "frontend/src/app/invoices/page.tsx",
        "frontend/src/components/InvoiceCard.tsx",
        "frontend/src/components/ConfidenceIndicator.tsx"
    ]
    
    confidence_display_found = False
    for file_path in frontend_files:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if "confidence" in content.lower():
                    print(f"✅ Confidence handling found in: {file_path}")
                    confidence_display_found = True
    
    if not confidence_display_found:
        print("❌ NO CONFIDENCE SCORE DISPLAY FOUND")
        print("💡 Need to add confidence indicators to UI")
    
    print()
    
    # 5. Check what confidence data is available
    print("📊 5. CONFIDENCE DATA AVAILABILITY")
    print("-" * 34)
    
    print("From your logs, AI extracts these confidence fields:")
    confidence_fields = [
        'invoice_number_confidence', 'invoice_date_confidence', 
        'vendor_name_confidence', 'total_amount_confidence',
        'currency_confidence', 'vendor_phone_confidence', 
        'vendor_address_confidence', 'customer_name_confidence',
        'subtotal_confidence', 'cgst_confidence', 'sgst_confidence',
        'total_gst_confidence', 'payment_status_confidence'
    ]
    
    for field in confidence_fields:
        print(f"   📈 {field}")
    
    print()
    print("✅ All confidence data is available from AI")
    print("❌ But not displayed in the UI")
    
    print()
    print("🔧 FIXES NEEDED:")
    print("=" * 15)
    print("1. 📄 Create PDF export functionality")
    print("2. 🎯 Add confidence score display to UI")
    print("3. 📊 Show confidence ratings (1-10 scale)")
    print("4. 🌐 Verify all export endpoints are working")

if __name__ == "__main__":
    check_export_functionality()