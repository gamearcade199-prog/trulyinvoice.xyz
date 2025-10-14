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
# Allow frontend to make API calls from different domains
allowed_origins = [
    "http://localhost:3000",  # Local development
    "http://localhost:3004",  # Alternative local port
    "https://trulyinvoice.xyz",  # Production domain
    "https://www.trulyinvoice.xyz",  # Production with www
    "https://trulyinvoice-xyz.vercel.app",  # Vercel deployment
]

# Add any preview deployments from environment
if os.getenv("VERCEL_URL"):
    allowed_origins.append(f"https://{os.getenv('VERCEL_URL')}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
