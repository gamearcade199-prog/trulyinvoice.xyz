"""
CLEAN BACKEND - Main Application Entry Point
Industry-standard FastAPI backend with zero dependency conflicts
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title="TrulyInvoice API",
    description="Clean, production-ready invoice processing API",
    version="2.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3004"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from app.api import documents, invoices, health

# Register routes
app.include_router(health.router, tags=["Health"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["Invoices"])

@app.get("/")
def root():
    return {
        "message": "TrulyInvoice API v2.0 - Clean Architecture",
        "status": "operational",
        "docs": "/docs"
    }
