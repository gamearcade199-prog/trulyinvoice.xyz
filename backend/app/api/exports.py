"""
Bulk Export API Router - Multiple invoice exports with Professional Exporters
PDF Export has been disabled
"""
import json
import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from app.services.supabase_helper import supabase
from app.services.accountant_excel_exporter import AccountantExcelExporter
from app.services.excel_exporter import export_invoices
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
        excel_filename = exporter.export_invoices_bulk(invoices)
        
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
    """PDF Export feature has been disabled"""
    raise HTTPException(
        status_code=503, 
        detail="PDF export feature is currently disabled. Please use Excel or CSV export."
    )

@router.post("/export-csv")
async def bulk_export_csv(request: BulkExportRequest, current_user_id: str = Depends(get_current_user)):
    """Export invoices to Excel with dynamic column widths"""
    try:
        # Get invoices
        invoice_ids = [str(inv_id) for inv_id in request.invoice_ids]
        invoices_response = supabase.table("invoices").select("*").in_("id", invoice_ids).execute()
        invoices = invoices_response.data
        
        if not invoices:
            raise HTTPException(status_code=404, detail="No invoices found")
        
        # Parse line_items JSON
        for invoice in invoices:
            if isinstance(invoice.get('line_items'), str):
                try:
                    invoice['line_items'] = json.loads(invoice['line_items'])
                except:
                    invoice['line_items'] = []
        
        # Export to Excel with dynamic columns
        excel_path = export_invoices(invoices)
        
        return FileResponse(
            path=excel_path,
            filename=f"invoices_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        print(f"❌ Export Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


# Note: /export-pdf now uses the new HTMLPDFExporter by default
# The old ProfessionalPDFExporterV2 is deprecated
# If you need the old version, use ProfessionalPDFExporterV2 directly
