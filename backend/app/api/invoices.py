"""
Invoices API - Retrieve and manage invoices
Compatible with existing Supabase invoices table
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import List, Dict, Any
import os
from app.services.supabase_helper import supabase
from app.services.excel_exporter import ExcelExporter
from app.services.professional_excel_exporter import ProfessionalInvoiceExporter
from app.services.professional_pdf_exporter import ProfessionalPDFExporter
from app.services.accountant_excel_exporter import AccountantExcelExporter
from app.services.csv_exporter import CSVExporter
# 🚀 NEW BULLETPROOF EXPORTERS - GEMINI COMPATIBLE (temporarily disabled)
# from app.services.bulletproof_excel_exporter import BulletproofExcelExporter
# from app.services.bulletproof_pdf_exporter import BulletproofPDFExporter
# from app.services.bulletproof_csv_exporter import BulletproofCSVExporter

router = APIRouter()


@router.get("/", response_model=List[Dict[Any, Any]])
async def get_invoices(user_id: str = None, limit: int = 100):
    """
    Get all invoices (optionally filtered by user)
    """
    try:
        filters = {"user_id": user_id} if user_id else None
        invoices = supabase.select("invoices", columns="*", filters=filters)
        
        return invoices or []
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{invoice_id}")
async def get_invoice(invoice_id: str):
    """Get single invoice by ID"""
    print(f"🔍 GET /api/invoices/{invoice_id}")
    print(f"  📋 Invoice ID type: {type(invoice_id)} | Value: '{invoice_id}'")
    
    try:
        print(f"  📊 Querying Supabase for invoice...")
        
        # Try to convert to int if possible (for numeric IDs)
        try:
            numeric_id = int(invoice_id)
            print(f"  🔢 Trying numeric ID: {numeric_id}")
            invoices = supabase.select("invoices", filters={"id": numeric_id})
            if invoices:
                print(f"  ✅ Found with numeric ID! Vendor: {invoices[0].get('vendor_name', 'Unknown')}")
                return invoices[0]
        except (ValueError, TypeError):
            print(f"  ℹ️ Not a numeric ID, trying as string/UUID")
        
        # Try as string/UUID
        invoices = supabase.select("invoices", filters={"id": invoice_id})
        print(f"  📊 Query result: {len(invoices) if invoices else 0} rows")
        
        if not invoices:
            print(f"  ❌ Invoice not found with ID: {invoice_id}")
            # Debug: Get all invoice IDs to help diagnose
            try:
                all_invoices = supabase.select("invoices", columns="id,vendor_name,user_id")
                print(f"  📊 Database contains {len(all_invoices)} total invoices")
                print(f"  📋 Sample IDs in DB: {[inv['id'] for inv in all_invoices[:3]]}")
            except Exception as debug_error:
                print(f"  ⚠️ Could not list invoice IDs: {debug_error}")
            
            raise HTTPException(status_code=404, detail=f"Invoice {invoice_id} not found")
        
        print(f"  ✅ Invoice found: {invoices[0].get('vendor_name', 'Unknown')}")
        return invoices[0]
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{invoice_id}")
async def delete_invoice(invoice_id: str):
    """Delete an invoice"""
    try:
        supabase.delete("invoices", filters={"id": invoice_id})
        
        return {"success": True, "message": "Invoice deleted"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ 🚀 BULLETPROOF 10/10 EXPORT ENDPOINTS (temporarily disabled) ============
# Will enable after fixing line continuation issues in the export files
# These endpoints will provide 10/10 quality exports using ALL Gemini extracted data


# ============ ORIGINAL EXPORT ENDPOINTS (LEGACY) ============

@router.get("/{invoice_id}/export-pdf")
async def export_invoice_pdf(invoice_id: str):
    """
    🎯 STYLIZED PDF EXPORT (for clients, business owners)
    
    Export single invoice as professional PDF
    - Beautiful formatting with colors
    - Proper ₹ symbols
    - Company branding
    - Print-ready format
    - Perfect for sending to customers
    
    Target Users: Clients, Business Owners, Anyone who needs to VIEW
    """
    try:
        # Get invoice
        invoices = supabase.select("invoices", filters={"id": invoice_id})
        
        if not invoices:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        invoice_data = invoices[0]
        
        # Export to PDF
        exporter = ProfessionalPDFExporter()
        pdf_filename = exporter.export_invoice(invoice_data)
        
        # Return file
        return FileResponse(
            path=pdf_filename,
            filename=pdf_filename,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{pdf_filename}"'
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{invoice_id}/export-excel")
async def export_invoice_excel(invoice_id: str):
    """
    📊 LIGHT-STYLED EXCEL EXPORT (for accountants, SMEs)
    
    Export single invoice as accountant-friendly Excel
    - Light styling (minimal colors, just for readability)
    - Formulas for calculations (tax = rate × qty)
    - Consistent column structure
    - Import-ready for Tally/Zoho/QuickBooks
    - Perfect for accounting/analysis
    
    Target Users: Accountants, SMEs, Bookkeepers, Anyone who needs to EDIT/IMPORT
    """
    try:
        # Get invoice
        invoices = supabase.select("invoices", filters={"id": invoice_id})
        
        if not invoices:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        invoice_data = invoices[0]
        
        # Export to Excel (accountant-friendly version)
        exporter = AccountantExcelExporter()
        excel_filename = exporter.export_invoice(invoice_data)
        
        # Return file
        return FileResponse(
            path=excel_filename,
            filename=excel_filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="{excel_filename}"'
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{invoice_id}/export-csv")
async def export_invoice_csv(invoice_id: str):
    """
    📄 RAW CSV EXPORT (for developers, ERP/CRM systems)
    
    Export single invoice as plain CSV
    - No formatting whatsoever
    - Plain text, comma-separated
    - Consistent column order (same as Excel)
    - UTF-8 encoding for ₹ symbols
    - Perfect for automation and bulk processing
    
    Target Users: Developers, ERP Systems, Automation Scripts
    """
    try:
        # Get invoice
        invoices = supabase.select("invoices", filters={"id": invoice_id})
        
        if not invoices:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        invoice_data = invoices[0]
        
        # Export to CSV
        exporter = CSVExporter()
        csv_filename = exporter.export_invoice(invoice_data)
        
        # Return file
        return FileResponse(
            path=csv_filename,
            filename=csv_filename,
            media_type="text/csv",
            headers={
                "Content-Disposition": f'attachment; filename="{csv_filename}"'
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ ORIGINAL BULK EXPORT (LEGACY) ============

@router.get("/export/excel")
async def export_invoices_excel(user_id: str = None):
    """
    Export invoices to formatted Excel file (.xlsx)
    Features:
    - Formatted headers (bold, colored)
    - Currency formatting (₹ symbol)
    - Borders around cells
    - Auto-width columns
    - Multiple sheets (Summary + Details)
    - Formulas for totals
    - Vendor analysis
    """
    try:
        # Get invoices
        filters = {"user_id": user_id} if user_id else None
        invoices = supabase.select("invoices", columns="*", filters=filters)
        
        if not invoices:
            raise HTTPException(status_code=404, detail="No invoices found")
        
        # Export to Excel
        exporter = ExcelExporter()
        filename = exporter.export_invoices(invoices)
        
        # Return file
        return FileResponse(
            path=filename,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
