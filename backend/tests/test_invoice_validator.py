"""
🧪 AUTOMATED TEST SUITE FOR INVOICE VALIDATION
Catches data quality bugs before they reach production
"""

import pytest
from app.services.invoice_validator import InvoiceValidator, InvoiceValidationError


class TestInvoiceValidator:
    """Comprehensive test suite for invoice validation"""
    
    def test_valid_invoice_passes(self):
        """Valid invoice should pass all checks"""
        invoice = {
            'user_id': 'user-123',
            'document_id': 'doc-456',
            'invoice_number': 'INV-001',
            'vendor_name': 'Acme Corp',
            'total_amount': 1000.00,
            'invoice_date': '2025-10-22',
            'payment_status': 'pending'
        }
        
        is_valid, message, cleaned = InvoiceValidator.validate_invoice_data(invoice)
        assert is_valid, f"Valid invoice failed: {message}"
        assert cleaned['invoice_number'] == 'INV-001'
    
    def test_missing_invoice_number_fails(self):
        """Missing invoice_number should fail"""
        invoice = {
            'user_id': 'user-123',
            'document_id': 'doc-456',
            'invoice_number': '',  # Empty!
            'vendor_name': 'Acme Corp',
            'total_amount': 1000.00
        }
        
        is_valid, message, _ = InvoiceValidator.validate_invoice_data(invoice)
        assert not is_valid
        assert 'invoice_number' in message.lower()
    
    def test_missing_vendor_name_fails(self):
        """Missing vendor_name should fail"""
        invoice = {
            'user_id': 'user-123',
            'document_id': 'doc-456',
            'invoice_number': 'INV-001',
            'vendor_name': '',  # Empty!
            'total_amount': 1000.00
        }
        
        is_valid, message, _ = InvoiceValidator.validate_invoice_data(invoice)
        assert not is_valid
        assert 'vendor_name' in message.lower()
    
    def test_missing_user_id_fails(self):
        """Missing user_id should fail (RLS security)"""
        invoice = {
            'document_id': 'doc-456',
            'invoice_number': 'INV-001',
            'vendor_name': 'Acme Corp',
            'total_amount': 1000.00
        }
        
        is_valid, message, _ = InvoiceValidator.validate_invoice_data(invoice)
        assert not is_valid
        assert 'user_id' in message.lower()
    
    def test_negative_total_fails(self):
        """Negative total_amount should fail"""
        invoice = {
            'user_id': 'user-123',
            'document_id': 'doc-456',
            'invoice_number': 'INV-001',
            'vendor_name': 'Acme Corp',
            'total_amount': -100.00  # Negative!
        }
        
        is_valid, message, _ = InvoiceValidator.validate_invoice_data(invoice)
        assert not is_valid
        assert 'negative' in message.lower() or 'total' in message.lower()
    
    def test_invalid_payment_status_normalized(self):
        """Invalid payment_status should be normalized"""
        invoice = {
            'user_id': 'user-123',
            'document_id': 'doc-456',
            'invoice_number': 'INV-001',
            'vendor_name': 'Acme Corp',
            'total_amount': 1000.00,
            'payment_status': 'unpaid'  # Maps to 'pending'
        }
        
        is_valid, message, cleaned = InvoiceValidator.validate_invoice_data(invoice)
        assert is_valid
        assert cleaned['payment_status'] == 'pending'
    
    def test_whitespace_trimmed(self):
        """Whitespace should be trimmed from strings"""
        invoice = {
            'user_id': 'user-123',
            'document_id': 'doc-456',
            'invoice_number': '  INV-001  ',
            'vendor_name': '  Acme Corp  ',
            'total_amount': 1000.00
        }
        
        is_valid, message, cleaned = InvoiceValidator.validate_invoice_data(invoice)
        assert is_valid
        assert cleaned['invoice_number'] == 'INV-001'
        assert cleaned['vendor_name'] == 'Acme Corp'
    
    def test_confidence_score_validation(self):
        """Confidence scores must be between 0-1"""
        # Valid confidence
        invoice = {
            'user_id': 'user-123',
            'document_id': 'doc-456',
            'invoice_number': 'INV-001',
            'vendor_name': 'Acme Corp',
            'total_amount': 1000.00,
            'confidence_score': 0.85
        }
        
        is_valid, message, _ = InvoiceValidator.validate_invoice_data(invoice)
        assert is_valid
        
        # Invalid confidence (too high)
        invoice['confidence_score'] = 1.5
        is_valid, message, _ = InvoiceValidator.validate_invoice_data(invoice)
        assert not is_valid
    
    def test_invoice_number_too_long_fails(self):
        """Very long invoice_number should fail"""
        invoice = {
            'user_id': 'user-123',
            'document_id': 'doc-456',
            'invoice_number': 'INV-' + 'X' * 100,  # Too long
            'vendor_name': 'Acme Corp',
            'total_amount': 1000.00
        }
        
        is_valid, message, _ = InvoiceValidator.validate_invoice_data(invoice)
        assert not is_valid
    
    def test_due_date_before_invoice_date_warning(self):
        """If due_date before invoice_date, it's a warning"""
        invoice = {
            'user_id': 'user-123',
            'document_id': 'doc-456',
            'invoice_number': 'INV-001',
            'vendor_name': 'Acme Corp',
            'total_amount': 1000.00,
            'invoice_date': '2025-10-22',
            'due_date': '2025-10-20'  # Before invoice_date
        }
        
        is_valid, message, _ = InvoiceValidator.validate_invoice_data(invoice)
        # Should fail because due_date before invoice_date
        assert not is_valid
    
    def test_validate_and_clean_raises_on_error(self):
        """validate_and_clean should raise exception on error"""
        invoice = {
            'document_id': 'doc-456',  # Missing user_id
            'invoice_number': 'INV-001',
            'vendor_name': 'Acme Corp'
        }
        
        with pytest.raises(InvoiceValidationError):
            InvoiceValidator.validate_and_clean(invoice)
    
    def test_zero_total_amount_warning(self):
        """Zero total_amount should generate warning"""
        invoice = {
            'user_id': 'user-123',
            'document_id': 'doc-456',
            'invoice_number': 'INV-001',
            'vendor_name': 'Acme Corp',
            'total_amount': 0.0
        }
        
        # Should pass but with warning
        is_valid, message, _ = InvoiceValidator.validate_invoice_data(invoice)
        assert is_valid  # Still valid (might be incomplete data)
    
    def test_multiple_errors_all_reported(self):
        """Multiple errors should all be reported"""
        invoice = {
            'document_id': 'doc-456',  # Missing user_id
            'invoice_number': '',      # Missing invoice_number
            'vendor_name': '',         # Missing vendor_name
            'total_amount': -100,      # Negative
            'payment_status': 'invalid'  # Invalid status
        }
        
        is_valid, message, _ = InvoiceValidator.validate_invoice_data(invoice)
        assert not is_valid
        # Should report multiple issues
        assert message.count('❌') >= 3  # At least 3 errors


class TestInvoiceDataQuality:
    """Test suite for data quality scenarios"""
    
    def test_ai_extraction_with_empty_fields(self):
        """Simulate AI extraction with some empty fields"""
        invoice = {
            'user_id': 'user-123',
            'document_id': 'doc-456',
            'invoice_number': '',  # AI didn't extract
            'vendor_name': 'Company Name',
            'total_amount': 0,  # AI couldn't parse
            'invoice_date': None,
            'payment_status': ''
        }
        
        is_valid, message, cleaned = InvoiceValidator.validate_invoice_data(invoice)
        assert not is_valid  # Should fail due to empty invoice_number
    
    def test_fallback_invoice_number_generation(self):
        """Test with fallback invoice_number (mimics fix_missing_invoice_numbers)"""
        invoice = {
            'user_id': 'user-123',
            'document_id': '1913ba3c-c274-48b7',
            'invoice_number': 'INV-1913BA3C',  # Generated fallback
            'vendor_name': 'Travel Agency',
            'total_amount': 800.0
        }
        
        is_valid, message, cleaned = InvoiceValidator.validate_invoice_data(invoice)
        assert is_valid
        assert cleaned['invoice_number'] == 'INV-1913BA3C'


if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])
