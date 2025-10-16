"""
Bulk Export API Router - Multiple invoice exports
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from app.services.supabase_helper import SupabaseClient
from app.services.accountant_excel_exporter import AccountantExcelExporter
from app.services.professional_pdf_exporter import ProfessionalPDFExporter
from app.services.csv_exporter import CSVExporter

router = APIRouter()

# Initialize Supabase client
supabase = SupabaseClient()

class BulkExportRequest(BaseModel):
    invoice_ids: List[str]

@router.post("/export-excel")
async def bulk_export_excel(request: BulkExportRequest):
    """Bulk export multiple invoices to Excel"""
    try:
        # Get invoices
        invoices = []
        for invoice_id in request.invoice_ids:
            invoice_data = supabase.query("invoices", filters={"id": f"eq.{invoice_id}"})
            if invoice_data and 'data' in invoice_data:
                invoices.extend(invoice_data['data'])
        
        if not invoices:
            raise HTTPException(status_code=404, detail="No invoices found")
        
        # Export to Excel
        exporter = AccountantExcelExporter()
        excel_filename = exporter.export_invoices_bulk(invoices)
        
        return FileResponse(
            path=excel_filename,
            filename=f"invoices_bulk_{len(invoices)}.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export-pdf")
async def bulk_export_pdf(request: BulkExportRequest):
    """Bulk export multiple invoices to PDF"""
    try:
        # Get invoices
        invoices = []
        for invoice_id in request.invoice_ids:
            invoice_data = supabase.query("invoices", filters={"id": f"eq.{invoice_id}"})
            if invoice_data and 'data' in invoice_data:
                invoices.extend(invoice_data['data'])
        
        if not invoices:
            raise HTTPException(status_code=404, detail="No invoices found")
        
        # Export to PDF
        exporter = ProfessionalPDFExporter()
        pdf_filename = exporter.export_invoices_bulk(invoices)
        
        return FileResponse(
            path=pdf_filename,
            filename=f"invoices_bulk_{len(invoices)}.pdf",
            media_type="application/pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export-csv")
async def bulk_export_csv(request: BulkExportRequest):
    """Bulk export multiple invoices to CSV"""
    try:
        # Get invoices
        invoices = []
        for invoice_id in request.invoice_ids:
            invoice_data = supabase.query("invoices", filters={"id": f"eq.{invoice_id}"})
            if invoice_data and 'data' in invoice_data:
                invoices.extend(invoice_data['data'])
        
        if not invoices:
            raise HTTPException(status_code=404, detail="No invoices found")
        
        # Export to CSV
        exporter = CSVExporter()
        csv_filename = exporter.export_bulk_invoices(invoices)
        
        return FileResponse(
            path=csv_filename,
            filename=f"invoices_bulk_{len(invoices)}.csv",
            media_type="text/csv"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))