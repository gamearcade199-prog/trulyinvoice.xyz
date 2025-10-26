"""Health Check Router"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "TrulyInvoice Backend v2.0 - Operational",
        "features": [
            "Document Upload",
            "Invoice Processing",
            "Supabase Integration"
        ]
    }
