"""
Invoices API - Retrieve and manage invoices
Compatible with existing Supabase invoices table
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import FileResponse
from typing import List, Dict, Any
import os
import logging
from app.services.supabase_helper import supabase

# Set up logger
logger = logging.getLogger(__name__)
from app.services.excel_exporter import ExcelExporter
from app.services.professional_excel_exporter import ProfessionalInvoiceExporter
from app.services.html_professional_pdf_exporter import HTMLProfessionalPDFExporter
from app.services.accountant_excel_exporter import AccountantExcelExporter
from app.services.csv_exporter import CSVExporter
from app.config.plans import check_feature_access
from app.services.usage_tracker import UsageTracker
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth import get_current_user
# 🚀 NEW BULLETPROOF EXPORTERS - GEMINI COMPATIBLE (temporarily disabled)
# from app.services.bulletproof_excel_exporter import BulletproofExcelExporter
# from app.services.bulletproof_pdf_exporter import BulletproofPDFExporter
# from app.services.bulletproof_csv_exporter import BulletproofCSVExporter

router = APIRouter()


async def check_export_permission(user_id: str, db: Session = Depends(get_db)):
    """
    Check if user has permission to export invoices
    """
    tracker = UsageTracker(db)
    user_tier = await tracker.get_current_tier(user_id)
    
    if not check_feature_access(user_tier, "excel_csv_export"):
        raise HTTPException(
            status_code=403,
            detail="Export functionality requires a subscription. Please upgrade your plan."
        )
    
    return True
@router.get("/", response_model=List[Dict[Any, Any]])
async def get_invoices(user_id: str = None, limit: int = 100):
    """
    Get all invoices (optionally filtered by user)
    """
    try:
        query = supabase.table("invoices").select("*").limit(limit)
        if user_id:
            query = query.eq("user_id", user_id)
        invoices_response = query.execute()
        invoices = invoices_response.data
        
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
            invoices_response = supabase.table("invoices").select("*").eq("id", numeric_id).execute()
            invoices = invoices_response.data
            if invoices:
                print(f"  ✅ Found with numeric ID! Vendor: {invoices[0].get('vendor_name', 'Unknown')}")
                return invoices[0]
        except (ValueError, TypeError):
            print(f"  ℹ️ Not a numeric ID, trying as string/UUID")
        
        # Try as string/UUID
        invoices_response = supabase.table("invoices").select("*").eq("id", invoice_id).execute()
        invoices = invoices_response.data
        print(f"  📊 Query result: {len(invoices) if invoices else 0} rows")
        
        if not invoices:
            print(f"  ❌ Invoice not found with ID: {invoice_id}")
            # Debug: Get all invoice IDs to help diagnose
            try:
                all_invoices_response = supabase.table("invoices").select("id,vendor_name,user_id").execute()
                all_invoices = all_invoices_response.data
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
        supabase.table("invoices").delete().eq("id", invoice_id).execute()
        
        return {"success": True, "message": "Invoice deleted"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ 🚀 BULLETPROOF 10/10 EXPORT ENDPOINTS (temporarily disabled) ============
# Will enable after fixing line continuation issues in the export files
# These endpoints will provide 10/10 quality exports using ALL Gemini extracted data


# ============ ORIGINAL EXPORT ENDPOINTS (LEGACY) ============

@router.get("/{invoice_id}/export-pdf")
async def export_invoice_pdf(
    invoice_id: str,
    authorization: str = Header(None)
):
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
    print(f"📄 PDF Export endpoint called")
    print(f"   Invoice ID: {invoice_id}")
    print(f"   Authorization header: {authorization[:50] if authorization else 'MISSING'}...")
    
    # Manual auth validation
    if not authorization:
        print("   ❌ No authorization header")
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            print(f"   ❌ Invalid auth format: {len(parts)} parts")
            raise HTTPException(status_code=401, detail="Invalid authorization format")
        
        token = parts[1]
        print(f"   🔐 Token received, length: {len(token)}")
        
        # Validate token with Supabase
        response = supabase.auth.get_user(token)
        user_id = response.user.id if hasattr(response, 'user') and response.user else None
        if not user_id:
            print(f"   ❌ Token validation failed")
            raise HTTPException(status_code=401, detail="Invalid token")
        print(f"   ✅ User authenticated: {user_id}")
        
        # Get invoice
        invoices_response = supabase.table("invoices").select("*").eq("id", invoice_id).execute()
        invoices = invoices_response.data
        
        if not invoices:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        invoice_data = invoices[0]
        
        # Parse line_items if string
        if isinstance(invoice_data.get('line_items'), str):
            try:
                import json
                invoice_data['line_items'] = json.loads(invoice_data['line_items'])
            except Exception as e:
                logger.warning(f"Failed to parse line_items JSON for PDF export: {e}")
                invoice_data['line_items'] = []
        
        print(f"📊 Export-PDF: Processing invoice {invoice_id}")
        print(f"   Vendor: {invoice_data.get('vendor_name')}")
        print(f"   Invoice #: {invoice_data.get('invoice_number')}")
        
        # Export to PDF using HTML-based professional exporter
        exporter = HTMLProfessionalPDFExporter()
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
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Export-PDF Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{invoice_id}/export-excel")
async def export_invoice_excel(
    invoice_id: str,
    authorization: str = Header(None)
):
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
    print(f"📊 Excel Export endpoint called")
    print(f"   Invoice ID: {invoice_id}")
    print(f"   Authorization header: {authorization[:50] if authorization else 'MISSING'}...")
    
    # Manual auth validation
    if not authorization:
        print("   ❌ No authorization header")
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            print(f"   ❌ Invalid auth format: {len(parts)} parts")
            raise HTTPException(status_code=401, detail="Invalid authorization format")
        
        token = parts[1]
        print(f"   🔐 Token received, length: {len(token)}")
        
        # Validate token with Supabase
        response = supabase.auth.get_user(token)
        user_id = response.user.id if hasattr(response, 'user') and response.user else None
        if not user_id:
            print(f"   ❌ Token validation failed")
            raise HTTPException(status_code=401, detail="Invalid token")
        print(f"   ✅ User authenticated: {user_id}")
        
        # Get invoice
        invoices_response = supabase.table("invoices").select("*").eq("id", invoice_id).execute()
        invoices = invoices_response.data

        if not invoices:
            raise HTTPException(status_code=404, detail="Invoice not found")

        invoice_data = invoices[0]
        
        # Parse line_items if string
        if isinstance(invoice_data.get('line_items'), str):
            try:
                import json
                invoice_data['line_items'] = json.loads(invoice_data['line_items'])
            except Exception as e:
                logger.warning(f"Failed to parse line_items JSON for Excel export: {e}")
                invoice_data['line_items'] = []

        print(f"📊 Export-Excel: Processing invoice {invoice_id}")
        print(f"   Vendor: {invoice_data.get('vendor_name')}")
        print(f"   Invoice #: {invoice_data.get('invoice_number')}")
        print(f"   Total: {invoice_data.get('total_amount')}")

        # Get user's template preference
        try:
            users_response = supabase.table("users").select("export_template").eq("id", user_id).execute()
            user_template = "accountant"  # Default template
            if users_response.data and len(users_response.data) > 0:
                user_template = users_response.data[0].get('export_template', 'accountant')
            print(f"   📋 Using template: {user_template}")
        except Exception as e:
            print(f"   ⚠️ Could not fetch template preference, using default 'accountant': {e}")
            user_template = "accountant"

        # Export to Excel with user's preferred template
        exporter = AccountantExcelExporter()
        excel_filename = exporter.export_invoices_bulk([invoice_data], template=user_template)

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
        print(f"❌ Export-Excel Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{invoice_id}/export-csv")
async def export_invoice_csv(
    invoice_id: str,
    authorization: str = Header(None)
):
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
    print(f"📋 CSV Export endpoint called")
    print(f"   Invoice ID: {invoice_id}")
    print(f"   Authorization header: {authorization[:50] if authorization else 'MISSING'}...")
    
    # Manual auth validation
    if not authorization:
        print("   ❌ No authorization header")
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            print(f"   ❌ Invalid auth format: {len(parts)} parts")
            raise HTTPException(status_code=401, detail="Invalid authorization format")
        
        token = parts[1]
        print(f"   🔐 Token received, length: {len(token)}")
        
        # Validate token with Supabase
        response = supabase.auth.get_user(token)
        user_id = response.user.id if hasattr(response, 'user') and response.user else None
        if not user_id:
            print(f"   ❌ Token validation failed")
            raise HTTPException(status_code=401, detail="Invalid token")
        print(f"   ✅ User authenticated: {user_id}")
        
        # Get invoice
        invoices_response = supabase.table("invoices").select("*").eq("id", invoice_id).execute()
        invoices = invoices_response.data
        
        if not invoices:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        invoice_data = invoices[0]
        
        # Parse line_items if string
        if isinstance(invoice_data.get('line_items'), str):
            try:
                import json
                invoice_data['line_items'] = json.loads(invoice_data['line_items'])
            except Exception as e:
                logger.warning(f"Failed to parse line_items JSON for CSV export: {e}")
                invoice_data['line_items'] = []
        
        print(f"📊 Export-CSV: Processing invoice {invoice_id}")
        print(f"   Vendor: {invoice_data.get('vendor_name')}")
        print(f"   Invoice #: {invoice_data.get('invoice_number')}")
        
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
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Export-CSV Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ============ ORIGINAL BULK EXPORT (LEGACY) ============

@router.get("/export/excel")
async def export_invoices_excel(
    user_id: str = None,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
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
    # Check export permissions
    await check_export_permission(current_user_id, db)

    try:
        # Get invoices
        query = supabase.table("invoices").select("*")
        if user_id:
            query = query.eq("user_id", user_id)
        invoices_response = query.execute()
        invoices = invoices_response.data
        
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
