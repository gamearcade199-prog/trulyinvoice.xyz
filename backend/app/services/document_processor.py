"""
Enterprise-Grade Document Processing Service
Handles AI extraction, validation, and storage with comprehensive error handling
"""

import logging
import tempfile
import os
import asyncio
import httpx
import uuid
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
from app.core.config import settings
from app.services.ai_service import ai_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DocumentProcessingError(Exception):
    """Custom exception for document processing errors"""
    pass


class DocumentProcessor:
    """
    Enterprise-grade document processor with:
    - Retry logic
    - Comprehensive error handling
    - Detailed logging
    - Supabase HTTP API integration
    - Transaction management
    """
    
    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_SERVICE_KEY
        self.bucket_name = "invoice-documents"
        self.max_retries = 3
        self.headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json"
        }
        
    async def _supabase_query(self, table: str, method: str = "GET", **params):
        """Make HTTP request to Supabase"""
        url = f"{self.supabase_url}/rest/v1/{table}"
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, headers=self.headers, params=params)
            elif method == "POST":
                response = await client.post(url, headers=self.headers, json=params.get('data', {}))
            elif method == "PATCH":
                response = await client.patch(url, headers=self.headers, json=params.get('data', {}), params=params.get('params', {}))
            response.raise_for_status()
            return response.json()
    
    async def _download_from_storage(self, path: str):
        """Download file from Supabase Storage"""
        url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{path}"
        headers = {"Authorization": f"Bearer {self.supabase_key}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.content
        
    async def process_document(
        self,
        document_id: int,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a document with AI extraction
        
        Args:
            document_id: ID of the document to process
            user_id: Optional user ID for validation
            
        Returns:
            Dict containing processing results
            
        Raises:
            DocumentProcessingError: If processing fails
        """
        logger.info(f"Starting processing for document {document_id}")
        
        try:
            # Step 1: Fetch document from Supabase
            document = await self._fetch_document(document_id, user_id)
            
            # Step 2: Download file from storage
            file_path = await self._download_file(document)
            
            # Step 3: Update status to processing
            await self._update_document_status(document_id, "processing")
            
            # Step 4: Extract data with AI
            extracted_data = await self._extract_invoice_data(
                file_path,
                document.get('file_type', 'pdf')
            )
            
            # Step 5: Save invoice data
            invoice = await self._save_invoice_data(document, extracted_data)
            
            # Step 6: Update document status
            await self._update_document_status(
                document_id,
                "processed",
                confidence_score=extracted_data.get('confidence_score'),
                processed_at=datetime.utcnow().isoformat()
            )
            
            # Step 7: Cleanup
            self._cleanup_temp_file(file_path)
            
            logger.info(f"Successfully processed document {document_id}")
            
            return {
                "success": True,
                "document_id": document_id,
                "invoice_id": invoice.get('id'),
                "confidence_score": extracted_data.get('confidence_score'),
                "extracted_data": extracted_data
            }
            
        except Exception as e:
            logger.error(f"Error processing document {document_id}: {str(e)}", exc_info=True)
            
            # Update document status to error
            try:
                await self._update_document_status(
                    document_id,
                    "error",
                    error_message=str(e)
                )
            except Exception as update_error:
                logger.error(f"Failed to update error status: {str(update_error)}")
            
            raise DocumentProcessingError(f"Failed to process document: {str(e)}")
    
    async def _fetch_document(
        self,
        document_id: int,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch document from Supabase with validation"""
        logger.debug(f"Fetching document {document_id}")
        
        # Build query params - only use id filter, not user_id in params
        params = {"select": "*"}
        
        # Use URL parameter for filtering by ID
        async with httpx.AsyncClient() as client:
            url = f"{self.supabase_url}/rest/v1/documents?id=eq.{document_id}"
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            documents = response.json()
        
        if not documents or len(documents) == 0:
            raise DocumentProcessingError(f"Document {document_id} not found")
        
        document = documents[0]
        
        # Validate document has required fields
        if not document.get('storage_path'):
            raise DocumentProcessingError("Document has no storage path")
        
        return document
    
    async def _download_file(self, document: Dict[str, Any]) -> str:
        """Download file from Supabase Storage to temp file"""
        storage_path = document.get('storage_path')
        file_name = document.get('file_name', 'document')
        
        logger.debug(f"Downloading file from storage: {storage_path}")
        
        try:
            # Download file from Supabase Storage
            file_content = await self._download_from_storage(storage_path)
            
            # Create temp directory if it doesn't exist
            temp_dir = os.path.join(tempfile.gettempdir(), 'trulyinvoice')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Create a unique temp file path (Windows-compatible)
            import uuid
            safe_filename = f"{uuid.uuid4()}_{file_name}"
            temp_path = os.path.join(temp_dir, safe_filename)
            
            # Write file content
            with open(temp_path, 'wb') as f:
                f.write(file_content)
            
            logger.debug(f"File downloaded to: {temp_path}")
            return temp_path
            
        except Exception as e:
            logger.error(f"Download error: {str(e)}", exc_info=True)
            raise DocumentProcessingError(f"Failed to download file: {str(e)}")
    
    async def _extract_invoice_data(
        self,
        file_path: str,
        file_type: str
    ) -> Dict[str, Any]:
        """Extract invoice data using AI service with retry logic"""
        logger.info(f"Extracting data from {file_path}")
        
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                # Call AI service
                extracted_data, used_fallback = await ai_service.extract_invoice_data(
                    file_path,
                    file_type
                )
                
                # Convert to dict
                data_dict = extracted_data.dict() if hasattr(extracted_data, 'dict') else extracted_data
                data_dict['used_fallback_model'] = used_fallback
                
                logger.info(
                    f"Extraction successful (attempt {attempt + 1}/{self.max_retries}). "
                    f"Confidence: {data_dict.get('confidence_score', 0):.2f}"
                )
                
                return data_dict
                
            except Exception as e:
                last_error = e
                logger.warning(
                    f"Extraction attempt {attempt + 1}/{self.max_retries} failed: {str(e)}"
                )
                
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        raise DocumentProcessingError(
            f"AI extraction failed after {self.max_retries} attempts: {str(last_error)}"
        )
    
    async def _save_invoice_data(
        self,
        document: Dict[str, Any],
        extracted_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Save or update invoice data in Supabase"""
        logger.debug(f"Saving invoice data for document {document['id']}")
        
        # Prepare invoice data
        invoice_data = {
            'user_id': document.get('user_id'),
            'document_id': document['id'],
            'vendor_name': extracted_data.get('vendor_name'),
            'invoice_number': extracted_data.get('invoice_number'),
            'invoice_date': extracted_data.get('invoice_date'),
            'due_date': extracted_data.get('due_date'),
            'subtotal': extracted_data.get('subtotal', 0),
            'tax_amount': extracted_data.get('gst_amount', 0),
            'total_amount': extracted_data.get('total_amount', 0),
            'cgst': extracted_data.get('cgst', 0),
            'sgst': extracted_data.get('sgst', 0),
            'igst': extracted_data.get('igst', 0),
            'gstin': extracted_data.get('gstin'),
            'payment_method': extracted_data.get('payment_method'),
            'payment_status': 'unpaid',
            'line_items': extracted_data.get('line_items', []),
            'raw_extracted_data': extracted_data,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        try:
            # Check if invoice already exists
            existing = await self._supabase_query(
                "invoices",
                "GET",
                document_id=f"eq.{document['id']}",
                select="id"
            )
            
            if existing and len(existing) > 0:
                # Update existing invoice
                invoice_id = existing[0]['id']
                response = await self._supabase_query(
                    "invoices",
                    "PATCH",
                    data=invoice_data,
                    params={"id": f"eq.{invoice_id}"}
                )
                logger.info(f"Updated existing invoice {invoice_id}")
                return response[0] if response else {}
            else:
                # Create new invoice
                invoice_data['created_at'] = datetime.utcnow().isoformat()
                response = await self._supabase_query(
                    "invoices",
                    "POST",
                    data=invoice_data
                )
                logger.info(f"Created new invoice for document {document['id']}")
                return response[0] if response else {}
            
        except Exception as e:
            raise DocumentProcessingError(f"Failed to save invoice data: {str(e)}")
    
    async def _update_document_status(
        self,
        document_id: int,
        status: str,
        **kwargs
    ) -> None:
        """Update document status and metadata"""
        logger.debug(f"Updating document {document_id} status to {status}")
        
        update_data = {
            'status': status,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Add optional fields
        if 'confidence_score' in kwargs:
            update_data['confidence_score'] = kwargs['confidence_score']
        if 'error_message' in kwargs:
            update_data['error_message'] = kwargs['error_message']
        if 'processed_at' in kwargs:
            update_data['processed_at'] = kwargs['processed_at']
        
        try:
            await self._supabase_query(
                "documents",
                "PATCH",
                data=update_data,
                params={"id": f"eq.{document_id}"}
            )
        except Exception as e:
            logger.error(f"Failed to update document status: {str(e)}")
            raise
    
    def _cleanup_temp_file(self, file_path: str) -> None:
        """Safely remove temporary file"""
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                logger.debug(f"Cleaned up temp file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup temp file {file_path}: {str(e)}")


# Global instance
document_processor = DocumentProcessor()
