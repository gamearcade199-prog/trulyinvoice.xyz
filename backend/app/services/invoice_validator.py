"""
🛡️ CENTRALIZED INVOICE DATA VALIDATION LAYER
Prevents all data quality issues before they reach database or exports
"""

from typing import Dict, Any, Tuple, List, Optional
from decimal import Decimal
from datetime import datetime
import re


class InvoiceValidationError(Exception):
    """Raised when invoice data fails validation"""
    pass


class InvoiceValidator:
    """Comprehensive validation for all invoice fields"""
    
    # ============ FIELD CONSTRAINTS ============
    MIN_VENDOR_NAME_LENGTH = 2
    MAX_VENDOR_NAME_LENGTH = 200
    MIN_INVOICE_NUMBER_LENGTH = 1
    MAX_INVOICE_NUMBER_LENGTH = 50
    MIN_TOTAL_AMOUNT = 0.01  # Must be positive if present
    MAX_TOTAL_AMOUNT = 999999999.99
    MAX_STRING_FIELD_LENGTH = 1000
    
    # Valid payment statuses (must match DB constraint)
    VALID_PAYMENT_STATUSES = {
        'pending', 'paid', 'overdue', 'cancelled', 
        'refunded', 'partial', 'processing', 'failed'
    }
    
    # Payment status mapping for common variations
    PAYMENT_STATUS_MAPPING = {
        'unpaid': 'pending',
        'outstanding': 'pending',
        'draft': 'pending',
        'unknown': 'pending',
        'na': 'pending',
        'n/a': 'pending',
        'complete': 'paid',
        'completed': 'paid',
        'success': 'paid',
        'successful': 'paid',
        'late': 'overdue',
        'past_due': 'overdue',
        'void': 'cancelled',
        'canceled': 'cancelled',
        'refund': 'refunded',
        'returned': 'refunded',
        'partially_paid': 'partial',
    }
    
    # Confidence score constraints
    MIN_CONFIDENCE = 0.0
    MAX_CONFIDENCE = 1.0
    
    @classmethod
    def validate_invoice_data(cls, invoice_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Comprehensive validation of invoice data
        
        Returns:
            (is_valid: bool, error_message: str, cleaned_data: dict)
        """
        errors = []
        warnings = []
        cleaned_data = invoice_data.copy()
        
        try:
            # ============ REQUIRED FIELDS ============
            # user_id is required (for RLS security)
            if not cleaned_data.get('user_id'):
                errors.append("CRITICAL: Missing user_id (required for data access control)")
            
            # document_id is required (for audit trail)
            if not cleaned_data.get('document_id'):
                errors.append("CRITICAL: Missing document_id (required for audit trail)")
            
            # ============ INVOICE NUMBER VALIDATION ============
            invoice_num = cleaned_data.get('invoice_number', '').strip() if cleaned_data.get('invoice_number') else ''
            
            if not invoice_num:
                errors.append("CRITICAL: invoice_number cannot be empty. Must provide a valid invoice number.")
            elif len(invoice_num) < cls.MIN_INVOICE_NUMBER_LENGTH:
                errors.append(f"invoice_number too short (min {cls.MIN_INVOICE_NUMBER_LENGTH} chars)")
            elif len(invoice_num) > cls.MAX_INVOICE_NUMBER_LENGTH:
                errors.append(f"invoice_number too long (max {cls.MAX_INVOICE_NUMBER_LENGTH} chars)")
            else:
                cleaned_data['invoice_number'] = invoice_num
            
            # ============ VENDOR NAME VALIDATION ============
            vendor_name = str(cleaned_data.get('vendor_name', '')).strip() if cleaned_data.get('vendor_name') else ''
            
            if not vendor_name:
                # Allow missing vendor_name if it's a consolidated invoice or if we have sub-vendors
                is_consolidated = cleaned_data.get('is_consolidated', False)
                line_items = cleaned_data.get('line_items', [])
                has_sub_vendors = False
                if isinstance(line_items, list):
                    has_sub_vendors = any(item.get('sub_vendor') for item in line_items if isinstance(item, dict))
                
                if is_consolidated or has_sub_vendors:
                    warnings.append("vendor_name empty but consolidated invoice detected - will auto-generate")
                else:
                    errors.append("CRITICAL: vendor_name cannot be empty")
            elif len(vendor_name) < cls.MIN_VENDOR_NAME_LENGTH:
                warnings.append(f"vendor_name very short ({len(vendor_name)} chars) - might be incomplete")
            elif len(vendor_name) > cls.MAX_VENDOR_NAME_LENGTH:
                errors.append(f"vendor_name too long (max {cls.MAX_VENDOR_NAME_LENGTH} chars)")
            else:
                cleaned_data['vendor_name'] = vendor_name
            
            # ============ TOTAL AMOUNT VALIDATION ============
            total_amount = cleaned_data.get('total_amount')
            
            if total_amount is not None:
                try:
                    total_amount = float(total_amount)
                    if total_amount < 0:
                        errors.append(f"total_amount cannot be negative: {total_amount}")
                    elif total_amount > cls.MAX_TOTAL_AMOUNT:
                        errors.append(f"total_amount exceeds maximum: {total_amount} > {cls.MAX_TOTAL_AMOUNT}")
                    cleaned_data['total_amount'] = total_amount
                except (ValueError, TypeError):
                    errors.append(f"total_amount must be a number, got: {total_amount}")
            else:
                warnings.append("total_amount is missing (should be populated if invoice has financial data)")
                cleaned_data['total_amount'] = 0.0
            
            # ============ PAYMENT STATUS VALIDATION ============
            payment_status = str(cleaned_data.get('payment_status', 'pending')).strip().lower()
            
            # Try mapping first
            if payment_status in cls.PAYMENT_STATUS_MAPPING:
                payment_status = cls.PAYMENT_STATUS_MAPPING[payment_status]
                warnings.append(f"payment_status normalized: {cleaned_data.get('payment_status')} → {payment_status}")
            
            # Validate it's in allowed list
            if payment_status not in cls.VALID_PAYMENT_STATUSES:
                errors.append(f"payment_status invalid: '{payment_status}'. Must be one of: {cls.VALID_PAYMENT_STATUSES}")
            else:
                cleaned_data['payment_status'] = payment_status
            
            # ============ DATE VALIDATION ============
            date_fields = ['invoice_date', 'due_date', 'created_at', 'updated_at']
            for date_field in date_fields:
                if date_field in cleaned_data and cleaned_data[date_field]:
                    date_value = cleaned_data[date_field]
                    try:
                        # Try to parse date
                        if isinstance(date_value, str):
                            # Try YYYY-MM-DD format
                            datetime.strptime(date_value, '%Y-%m-%d')
                        elif isinstance(date_value, datetime):
                            pass  # Already a datetime
                        else:
                            warnings.append(f"{date_field} has unexpected type: {type(date_value)}")
                    except ValueError:
                        errors.append(f"{date_field} invalid format: '{date_value}' (expected YYYY-MM-DD)")
            
            # ============ DATE LOGIC VALIDATION ============
            # Check that due_date is not before invoice_date
            if 'invoice_date' in cleaned_data and 'due_date' in cleaned_data:
                inv_date_val = cleaned_data.get('invoice_date')
                due_date_val = cleaned_data.get('due_date')
                
                if inv_date_val and due_date_val:
                    try:
                        # Parse to datetime objects for comparison
                        inv_dt = datetime.strptime(inv_date_val, '%Y-%m-%d') if isinstance(inv_date_val, str) else inv_date_val
                        due_dt = datetime.strptime(due_date_val, '%Y-%m-%d') if isinstance(due_date_val, str) else due_date_val
                        
                        if due_dt < inv_dt:
                            errors.append(f"due_date ({due_date_val}) cannot be before invoice_date ({inv_date_val})")
                    except (ValueError, TypeError):
                        pass  # Already caught by individual field validation
            
            # ============ CONFIDENCE SCORE VALIDATION ============
            confidence_fields = [
                'confidence_score', 'vendor_confidence', 'amount_confidence',
                'date_confidence', 'invoice_number_confidence'
            ]
            for conf_field in confidence_fields:
                if conf_field in cleaned_data and cleaned_data[conf_field] is not None:
                    conf_value = cleaned_data[conf_field]
                    try:
                        conf_value = float(conf_value)
                        if conf_value < cls.MIN_CONFIDENCE or conf_value > cls.MAX_CONFIDENCE:
                            errors.append(
                                f"{conf_field} out of range: {conf_value} "
                                f"(must be between {cls.MIN_CONFIDENCE} and {cls.MAX_CONFIDENCE})"
                            )
                        else:
                            cleaned_data[conf_field] = conf_value
                    except (ValueError, TypeError):
                        errors.append(f"{conf_field} must be a number, got: {conf_value}")
            
            # ============ STRING FIELD TRIMMING & VALIDATION ============
            string_fields = [
                'customer_name', 'vendor_address', 'customer_address',
                'vendor_phone', 'vendor_email', 'vendor_gstin',
                'customer_gstin', 'notes'
            ]
            for string_field in string_fields:
                if string_field in cleaned_data and cleaned_data[string_field]:
                    str_value = str(cleaned_data[string_field]).strip()
                    if len(str_value) > cls.MAX_STRING_FIELD_LENGTH:
                        errors.append(
                            f"{string_field} too long ({len(str_value)} chars, "
                            f"max {cls.MAX_STRING_FIELD_LENGTH})"
                        )
                    else:
                        cleaned_data[string_field] = str_value
            
            # ============ NUMERIC FIELD VALIDATION ============
            numeric_fields = [
                'subtotal', 'cgst', 'sgst', 'igst', 'paid_amount', 
                'discount', 'shipping_charges', 'tax_amount'
            ]
            for numeric_field in numeric_fields:
                if numeric_field in cleaned_data and cleaned_data[numeric_field] is not None:
                    try:
                        num_value = float(cleaned_data[numeric_field])
                        if num_value < 0:
                            warnings.append(f"{numeric_field} is negative: {num_value}")
                        cleaned_data[numeric_field] = num_value
                    except (ValueError, TypeError):
                        errors.append(f"{numeric_field} must be a number, got: {cleaned_data[numeric_field]}")
            
            # ============ REMOVE UI-ONLY FIELDS FROM EXPORT ============
            # These should never be saved to database
            ui_only_fields = ['uploaded_at', 'processing_status']
            for ui_field in ui_only_fields:
                if ui_field in cleaned_data:
                    del cleaned_data[ui_field]
            
            # ============ FINAL DECISION ============
            if errors:
                error_message = "Invoice validation FAILED:\n" + "\n".join(f"  ❌ {e}" for e in errors)
                if warnings:
                    error_message += "\n" + "\n".join(f"  ⚠️  {w}" for w in warnings)
                return False, error_message, {}
            
            # Validation passed
            success_message = "✅ Invoice validation passed"
            if warnings:
                success_message += f" ({len(warnings)} warnings)"
            
            return True, success_message, cleaned_data
            
        except Exception as e:
            return False, f"UNEXPECTED ERROR in validation: {str(e)}", {}
    
    @classmethod
    def quick_validate(cls, invoice_data: Dict[str, Any]) -> bool:
        """Quick validation - returns True if valid, False otherwise"""
        is_valid, _, _ = cls.validate_invoice_data(invoice_data)
        return is_valid
    
    @classmethod
    def validate_and_clean(cls, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and return cleaned data, raise exception if invalid
        
        Usage:
            try:
                cleaned = InvoiceValidator.validate_and_clean(data)
            except InvoiceValidationError as e:
                # Handle error
        """
        is_valid, message, cleaned_data = cls.validate_invoice_data(invoice_data)
        if not is_valid:
            raise InvoiceValidationError(message)
        return cleaned_data


# ============ CONVENIENCE FUNCTIONS ============

def validate_invoice_before_save(invoice_data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate invoice before saving to database
    Returns: (is_valid, message)
    """
    is_valid, message, _ = InvoiceValidator.validate_invoice_data(invoice_data)
    return is_valid, message


def validate_invoice_before_export(invoice_data: Dict[str, Any]) -> List[str]:
    """
    Validate invoice before exporting (less strict than save validation)
    Returns: list of warning/error messages
    """
    issues = []
    
    # Check critical fields for export
    if not invoice_data.get('invoice_number'):
        issues.append("⚠️  invoice_number is empty")
    
    if not invoice_data.get('vendor_name'):
        issues.append("⚠️  vendor_name is empty")
    
    if invoice_data.get('total_amount') == 0:
        issues.append("⚠️  total_amount is 0 (may indicate incomplete data)")
    
    if not invoice_data.get('invoice_date'):
        issues.append("⚠️  invoice_date is missing")
    
    return issues
