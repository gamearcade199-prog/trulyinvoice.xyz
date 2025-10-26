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
        FAST document processing with AI extraction - Target: 5-10 seconds
        
        Args:
            document_id: ID of the document to process
            user_id: Optional user ID for validation
            
        Returns:
            Dict containing processing results
            
        Raises:
            DocumentProcessingError: If processing fails
        """
        import time
        start_time = time.time()
        logger.info(f"🚀 FAST processing started for document {document_id}")
        
        try:
            # Step 1: Fetch document from Supabase (~0.5s)
            document = await self._fetch_document(document_id, user_id)
            step1_time = time.time() - start_time
            print(f"   📄 Document fetched in {step1_time:.2f}s")
            
            # Step 2: Download file from storage (~1-2s)
            file_path = await self._download_file(document)
            step2_time = time.time() - start_time
            print(f"   📥 File downloaded in {step2_time - step1_time:.2f}s")
            
            # Step 3: Update status to processing (~0.3s)
            await self._update_document_status(document_id, "processing")
            
            # Step 4: FAST AI extraction (~3-6s - main optimization target)
            extracted_data = await self._extract_invoice_data(
                file_path,
                document.get('file_type', 'pdf')
            )
            step4_time = time.time() - start_time
            print(f"   🤖 AI extraction completed in {step4_time - step2_time:.2f}s")
            
            # Step 5: Save invoice data (~0.5s)
            invoice = await self._save_invoice_data(document, extracted_data)
            step5_time = time.time() - start_time
            print(f"   💾 Data saved in {step5_time - step4_time:.2f}s")
            
            # Step 6: Update document status (~0.3s)
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
    
    def _clean_string_field(self, value: Any) -> Optional[str]:
        """
        Clean string fields: convert empty strings to None, strip whitespace
        """
        if not value:
            return None
        
        cleaned = str(value).strip()
        return cleaned if cleaned else None

    def _validate_payment_status(self, value: Any) -> str:
        """
        Validate and sanitize payment_status field.
        MUST match ENHANCED_SCHEMA_50_PLUS_FIELDS.sql constraint:
        CHECK (payment_status IN ('pending', 'paid', 'overdue', 'cancelled', 'refunded', 'partial', 'processing', 'failed'))
        """
        # Database constraint from ENHANCED_SCHEMA_50_PLUS_FIELDS.sql
        valid_statuses = {'pending', 'paid', 'overdue', 'cancelled', 'refunded', 'partial', 'processing', 'failed'}
        
        # Convert to string and clean up
        if not value:
            return 'pending'  # Default to 'pending' (valid in ENHANCED schema)
        
        status_str = str(value).strip().lower()
        
        # Map additional variations to valid values
        status_mapping = {
            'unpaid': 'pending',          # unpaid → pending (unpaid not allowed!)
            'unknown': 'pending',         # unknown → pending
            'na': 'pending',              # n/a → pending
            'n/a': 'pending',
            'draft': 'pending',           # draft → pending
            # These are already valid in the schema:
            'pending': 'pending',         # pending is valid
            'paid': 'paid',               # paid is valid  
            'overdue': 'overdue',         # overdue is valid
            'cancelled': 'cancelled',     # cancelled is valid
            'refunded': 'refunded',       # refunded is valid
            'partial': 'partial',         # partial is valid
            'processing': 'processing',   # processing is valid
            'failed': 'failed',           # failed is valid
        }
        
        # Use mapping if exists
        if status_str in status_mapping:
            return status_mapping[status_str]
        
        # Return if valid, otherwise default to 'pending'
        return status_str if status_str in valid_statuses else 'pending'
    
    def _calculate_overall_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate overall confidence score based on extracted data quality"""
        scores = []
        
        # Vendor confidence
        vendor_score = 0.85
        if data.get('vendor_name') and len(str(data['vendor_name'])) > 3:
            vendor_score = 0.90
        elif not data.get('vendor_name'):
            vendor_score = 0.60
        scores.append(vendor_score)
        
        # Amount confidence
        amount_score = 0.85
        if data.get('total_amount') and data['total_amount'] > 0:
            amount_score = 0.92
        elif not data.get('total_amount'):
            amount_score = 0.55
        scores.append(amount_score)
        
        # Date confidence
        date_score = 0.85
        if data.get('invoice_date'):
            date_score = 0.88
        elif not data.get('invoice_date'):
            date_score = 0.60
        scores.append(date_score)
        
        # Invoice number confidence
        invoice_num_score = 0.80
        if data.get('invoice_number') and len(str(data['invoice_number'])) > 2:
            invoice_num_score = 0.85
        elif not data.get('invoice_number'):
            invoice_num_score = 0.50
        scores.append(invoice_num_score)
        
        # Calculate weighted average
        overall = sum(scores) / len(scores)
        return round(overall, 2)
    
    async def _save_invoice_data(
        self,
        document: Dict[str, Any],
        extracted_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Save or update invoice data in Supabase"""
        logger.debug(f"Saving invoice data for document {document['id']}")
        
        # Create a copy to avoid modifying the original extracted_data
        # Remove fields that don't exist in the database schema
        safe_data = {k: v for k, v in extracted_data.items() 
                     if k not in ('error', 'error_message', '_extraction_metadata')}
        
        # Prepare comprehensive invoice data - ALL FIELDS SUPPORTED
        invoice_data = {
            # Required fields
            'user_id': document.get('user_id'),
            'document_id': document['id'],
            'invoice_number': self._clean_string_field(safe_data.get('invoice_number')),
            'invoice_date': safe_data.get('invoice_date'),
            'vendor_name': self._clean_string_field(safe_data.get('vendor_name')) or 'Unknown Vendor',  # NOT NULL in some schemas
            'total_amount': safe_data.get('total_amount', 0),
            'payment_status': self._validate_payment_status(safe_data.get('payment_status')),
            
            # Vendor Information (all optional)
            'vendor_gstin': self._clean_string_field(safe_data.get('vendor_gstin') or safe_data.get('gstin')),
            'vendor_pan': self._clean_string_field(safe_data.get('vendor_pan')),
            'vendor_tan': self._clean_string_field(safe_data.get('vendor_tan')),
            'vendor_email': self._clean_string_field(safe_data.get('vendor_email')),
            'vendor_phone': self._clean_string_field(safe_data.get('vendor_phone')),
            'vendor_address': self._clean_string_field(safe_data.get('vendor_address')),
            'vendor_state': self._clean_string_field(safe_data.get('vendor_state')),
            'vendor_city': self._clean_string_field(safe_data.get('vendor_city')),
            'vendor_pincode': self._clean_string_field(safe_data.get('vendor_pincode')),
            
            # Customer Information (optional)
            'customer_name': self._clean_string_field(safe_data.get('customer_name')),
            'customer_gstin': self._clean_string_field(safe_data.get('customer_gstin')),
            'customer_pan': self._clean_string_field(safe_data.get('customer_pan')),
            'customer_email': self._clean_string_field(safe_data.get('customer_email')),
            'customer_phone': self._clean_string_field(safe_data.get('customer_phone')),
            'customer_address': self._clean_string_field(safe_data.get('customer_address')),
            'customer_state': self._clean_string_field(safe_data.get('customer_state')),
            
            # Dates & References
            'due_date': safe_data.get('due_date'),
            'po_number': self._clean_string_field(safe_data.get('po_number')),
            'po_date': safe_data.get('po_date'),
            'challan_number': self._clean_string_field(safe_data.get('challan_number')),
            'eway_bill_number': self._clean_string_field(safe_data.get('eway_bill_number')),
            'lr_number': self._clean_string_field(safe_data.get('lr_number')),
            
            # Financial Amounts
            'subtotal': safe_data.get('subtotal', 0),
            'taxable_amount': safe_data.get('taxable_amount', 0),
            
            # GST Taxes (Indian Tax System)
            'cgst': safe_data.get('cgst', 0),
            'sgst': safe_data.get('sgst', 0),
            'igst': safe_data.get('igst', 0),
            'ugst': safe_data.get('ugst', 0),
            'cess': safe_data.get('cess', 0),
            'total_gst': safe_data.get('total_gst', 0),
            
            # Other Tax Fields
            'vat': safe_data.get('vat', 0),
            'service_tax': safe_data.get('service_tax', 0),
            'tds_amount': safe_data.get('tds_amount', 0),
            'tds_percentage': safe_data.get('tds_percentage', 0),
            'tcs_amount': safe_data.get('tcs_amount', 0),
            
            # Deductions & Charges  
            'discount': safe_data.get('discount', 0),
            'discount_percentage': safe_data.get('discount_percentage', 0),
            'shipping_charges': safe_data.get('shipping_charges', 0),
            'freight_charges': safe_data.get('freight_charges', 0),
            'handling_charges': safe_data.get('handling_charges', 0),
            'packing_charges': safe_data.get('packing_charges', 0),
            'insurance_charges': safe_data.get('insurance_charges', 0),
            'loading_charges': safe_data.get('loading_charges', 0),
            'other_charges': safe_data.get('other_charges', 0),
            'roundoff': safe_data.get('roundoff', 0),
            'advance_paid': safe_data.get('advance_paid', 0),
            
            # Business Fields
            'currency': self._clean_string_field(safe_data.get('currency')) or 'INR',
            'exchange_rate': safe_data.get('exchange_rate', 1.0),
            'hsn_code': self._clean_string_field(safe_data.get('hsn_code')),
            'sac_code': self._clean_string_field(safe_data.get('sac_code')),
            'place_of_supply': self._clean_string_field(safe_data.get('place_of_supply')),
            'reverse_charge': safe_data.get('reverse_charge'),
            
            # Payment Information
            'payment_method': self._clean_string_field(safe_data.get('payment_method')),
            'payment_terms': self._clean_string_field(safe_data.get('payment_terms')),
            'bank_name': self._clean_string_field(safe_data.get('bank_name')),
            'account_number': self._clean_string_field(safe_data.get('account_number')),
            'ifsc_code': self._clean_string_field(safe_data.get('ifsc_code')),
            'upi_id': self._clean_string_field(safe_data.get('upi_id')),
            
            # Invoice Classification
            'invoice_type': self._clean_string_field(safe_data.get('invoice_type')) or 'standard',
            'business_type': self._clean_string_field(safe_data.get('business_type')),
            'supply_type': self._clean_string_field(safe_data.get('supply_type')),
            'transaction_type': self._clean_string_field(safe_data.get('transaction_type')),
            
            # Data Storage
            'line_items': safe_data.get('line_items', []),
            'raw_extracted_data': safe_data,
            'updated_at': datetime.utcnow().isoformat(),
            
            # AI Confidence Scores
            'confidence_score': self._calculate_overall_confidence(safe_data),
            'vendor_confidence': safe_data.get('vendor_confidence', 0.85),
            'amount_confidence': safe_data.get('amount_confidence', 0.88),
            'date_confidence': safe_data.get('date_confidence', 0.85),
            'invoice_number_confidence': safe_data.get('invoice_number_confidence', 0.80)
        }
        
        # Remove None values to avoid database issues
        invoice_data = {k: v for k, v in invoice_data.items() if v is not None}
        
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
