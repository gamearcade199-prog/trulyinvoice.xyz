"""Health Check Router"""
from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "TrulyInvoice Backend v2.0 - Operational",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "features": [
            "Document Upload",
            "Invoice Processing",
            "Supabase Integration"
        ]
    }
