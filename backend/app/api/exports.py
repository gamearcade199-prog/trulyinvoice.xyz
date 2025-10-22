"""
Bulk Export API Router - Multiple invoice exports
"""
import json
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from app.services.supabase_helper import supabase
from app.services.accountant_excel_exporter import AccountantExcelExporter
from app.services.professional_pdf_exporter import ProfessionalPDFExporter
from app.services.csv_exporter import CSVExporter
from app.auth import get_current_user

router = APIRouter()

class BulkExportRequest(BaseModel):
    invoice_ids: List[str]
    template: str = "simple"  # Default to simple template

@router.post("/export-excel")
async def bulk_export_excel(request: BulkExportRequest, current_user_id: str = Depends(get_current_user)):
    """Bulk export multiple invoices to Excel"""
    try:
        # Get invoices
        invoice_ids = [str(inv_id) for inv_id in request.invoice_ids]
        invoices_response = supabase.table("invoices").select("*").in_("id", invoice_ids).execute()
        invoices = invoices_response.data
        
        if not invoices:
            raise HTTPException(status_code=404, detail="No invoices found")
        
        print(f"📊 Bulk Export-Excel: Processing {len(invoices)} invoices")
        
        # Manually parse line_items from JSON string to list
        for idx, invoice in enumerate(invoices):
            if isinstance(invoice.get('line_items'), str):
                try:
                    invoice['line_items'] = json.loads(invoice['line_items'])
                except json.JSONDecodeError:
                    invoice['line_items'] = []
            print(f"   Invoice {idx+1}: {invoice.get('vendor_name', 'Unknown')}")
        
        # Export to Excel
        exporter = AccountantExcelExporter()
        excel_filename = exporter.export_invoices_bulk(invoices, template=request.template)
        
        print(f"✅ Bulk Excel export successful: {excel_filename}")
        
        return FileResponse(
            path=excel_filename,
            filename=f"invoices_bulk_{len(invoices)}.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        print(f"❌ Bulk Export-Excel Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export-pdf")
async def bulk_export_pdf(request: BulkExportRequest, current_user_id: str = Depends(get_current_user)):
    """Bulk export multiple invoices to PDF"""
    try:
        # Get invoices
        invoice_ids = [str(inv_id) for inv_id in request.invoice_ids]
        invoices_response = supabase.table("invoices").select("*").in_("id", invoice_ids).execute()
        invoices = invoices_response.data
        
        if not invoices:
            raise HTTPException(status_code=404, detail="No invoices found")
        
        print(f"📊 Bulk Export-PDF: Processing {len(invoices)} invoices")
        
        # Manually parse line_items from JSON string to list
        for idx, invoice in enumerate(invoices):
            if isinstance(invoice.get('line_items'), str):
                try:
                    invoice['line_items'] = json.loads(invoice['line_items'])
                except json.JSONDecodeError:
                    invoice['line_items'] = []
            print(f"   Invoice {idx+1}: {invoice.get('vendor_name', 'Unknown')}")
        
        # Export to PDF
        from app.services.professional_pdf_exporter import ProfessionalPDFExporter
        exporter = ProfessionalPDFExporter()
        pdf_filename = exporter.export_invoices_bulk(invoices)
        
        print(f"✅ Bulk PDF export successful: {pdf_filename}")
        
        return FileResponse(
            path=pdf_filename,
            filename=f"invoices_bulk_{len(invoices)}.pdf",
            media_type="application/pdf"
        )
        
    except Exception as e:
        print(f"❌ Bulk Export-PDF Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export-csv")
async def bulk_export_csv(request: BulkExportRequest, current_user_id: str = Depends(get_current_user)):
    """Bulk export multiple invoices to CSV"""
    try:
        # Get invoices
        invoice_ids = [str(inv_id) for inv_id in request.invoice_ids]
        invoices_response = supabase.table("invoices").select("*").in_("id", invoice_ids).execute()
        invoices = invoices_response.data
        
        if not invoices:
            raise HTTPException(status_code=404, detail="No invoices found")
        
        print(f"📊 Bulk Export-CSV: Processing {len(invoices)} invoices")
        
        # Manually parse line_items from JSON string to list
        for idx, invoice in enumerate(invoices):
            if isinstance(invoice.get('line_items'), str):
                try:
                    invoice['line_items'] = json.loads(invoice['line_items'])
                except json.JSONDecodeError:
                    invoice['line_items'] = []
            print(f"   Invoice {idx+1}: {invoice.get('vendor_name', 'Unknown')}")
        
        # Export to CSV
        exporter = CSVExporter()
        csv_filename = exporter.export_bulk_invoices(invoices)
        
        print(f"✅ Bulk CSV export successful: {csv_filename}")
        
        return FileResponse(
            path=csv_filename,
            filename=f"invoices_bulk_{len(invoices)}.csv",
            media_type="text/csv"
        )
        
    except Exception as e:
        print(f"❌ Bulk Export-CSV Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))