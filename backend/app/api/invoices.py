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
    try:
        invoices = supabase.select("invoices", filters={"id": invoice_id})
        
        if not invoices:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        return invoices[0]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{invoice_id}")
async def delete_invoice(invoice_id: str):
    """Delete an invoice"""
    try:
        supabase.delete("invoices", filters={"id": invoice_id})
        
        return {"success": True, "message": "Invoice deleted"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
