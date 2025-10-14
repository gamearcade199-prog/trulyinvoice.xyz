"""
ROBUST PAYMENT STATUS DETECTOR
Advanced detection of payment status from invoice images and text
Looks for multiple indicators: stamps, watermarks, text, signatures, etc.
"""
import re
from typing import Dict, List, Optional, Tuple

class PaymentStatusDetector:
    """Advanced payment status detection with multiple indicators"""
    
    def __init__(self):
        # Comprehensive payment indicators
        self.paid_indicators = {
            'stamps': [
                'PAID', 'paid', 'Paid', 'PAYMENT RECEIVED', 'PAYMENT MADE',
                'SETTLEMENT DONE', 'CLEARED', 'cleared', 'Cleared'
            ],
            'watermarks': [
                'PAID IN FULL', 'FULLY PAID', 'AMOUNT RECEIVED', 'PAYMENT COMPLETE',
                'SETTLED', 'settled', 'Settled', 'PAYMENT CONFIRMED'
            ],
            'text_patterns': [
                'payment received', 'amount paid', 'paid on', 'paid by',
                'payment made', 'settlement', 'transaction completed',
                'payment confirmed', 'amount received', 'credited',
                'deposit received', 'cash received', 'cheque cleared',
                'online payment', 'upi payment received', 'neft received',
                'rtgs received', 'fund transfer received'
            ],
            'transaction_refs': [
                'transaction id', 'txn id', 'ref no', 'reference number',
                'utr number', 'payment ref', 'receipt no', 'rrn',
                'transaction reference', 'payment reference'
            ],
            'signatures': [
                'received by', 'authorized signatory', 'signature',
                'signed', 'acknowledged', 'confirmed by'
            ],
            'dates': [
                'payment date', 'paid date', 'settlement date',
                'transaction date', 'receipt date'
            ]
        }
        
        # Partial payment indicators
        self.partial_indicators = [
            'partial payment', 'advance paid', 'part payment',
            'installment', 'down payment', 'token amount',
            'advance received', 'partial settlement'
        ]
        
        # Pending/unpaid indicators
        self.unpaid_indicators = [
            'due', 'pending', 'outstanding', 'unpaid',
            'amount due', 'balance', 'overdue', 'payable'
        ]
    
    def detect_payment_status(self, text: str) -> Tuple[str, float, List[str]]:
        """
        Detect payment status from text with confidence score
        
        Returns:
            Tuple of (status, confidence_score, evidence_found)
        """
        text_lower = text.lower()
        evidence = []
        confidence = 0.0
        
        # Check for PAID indicators
        paid_score, paid_evidence = self._check_paid_indicators(text, text_lower)
        
        # Check for PARTIAL indicators  
        partial_score, partial_evidence = self._check_partial_indicators(text_lower)
        
        # Check for UNPAID indicators
        unpaid_score, unpaid_evidence = self._check_unpaid_indicators(text_lower)
        
        # Determine final status with improved logic
        if partial_score > 0.5:  # Check partial first (more specific)
            return "partial", partial_score, partial_evidence
        elif paid_score > 0.7:
            return "paid", paid_score, paid_evidence
        elif unpaid_score > 0.3:
            return "unpaid", unpaid_score, unpaid_evidence
        else:
            # Default based on highest score
            scores = [
                ("paid", paid_score, paid_evidence),
                ("partial", partial_score, partial_evidence), 
                ("unpaid", unpaid_score, unpaid_evidence)
            ]
            best = max(scores, key=lambda x: x[1])
            return best[0], best[1], best[2]
    
    def _check_paid_indicators(self, text: str, text_lower: str) -> Tuple[float, List[str]]:
        """Check for PAID status indicators"""
        evidence = []
        score = 0.0
        
        # Check stamps (highest confidence)
        for stamp in self.paid_indicators['stamps']:
            if stamp.lower() in text_lower:
                evidence.append(f"STAMP: {stamp}")
                score += 0.4
        
        # Check watermarks
        for watermark in self.paid_indicators['watermarks']:
            if watermark.lower() in text_lower:
                evidence.append(f"WATERMARK: {watermark}")
                score += 0.3
        
        # Check text patterns
        for pattern in self.paid_indicators['text_patterns']:
            if pattern in text_lower:
                evidence.append(f"TEXT: {pattern}")
                score += 0.2
        
        # Check transaction references
        for ref_pattern in self.paid_indicators['transaction_refs']:
            if ref_pattern in text_lower:
                evidence.append(f"TRANSACTION_REF: {ref_pattern}")
                score += 0.25
        
        # Check signatures
        for sig_pattern in self.paid_indicators['signatures']:
            if sig_pattern in text_lower:
                evidence.append(f"SIGNATURE: {sig_pattern}")
                score += 0.15
        
        # Check for specific payment methods with amounts
        payment_methods = [
            'upi:', 'neft:', 'rtgs:', 'imps:', 'cheque no', 'cash:',
            'card payment', 'net banking', 'online payment'
        ]
        for method in payment_methods:
            if method in text_lower:
                evidence.append(f"PAYMENT_METHOD: {method}")
                score += 0.2
        
        # Check for numerical transaction IDs
        txn_patterns = [
            r'txn\s*id\s*:?\s*\d{8,}',
            r'transaction\s*id\s*:?\s*\d{8,}',
            r'ref\s*no\s*:?\s*\d{8,}',
            r'utr\s*:?\s*\d{8,}'
        ]
        for pattern in txn_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                evidence.append(f"TXN_ID: {matches[0]}")
                score += 0.3
        
        return min(score, 1.0), evidence
    
    def _check_partial_indicators(self, text_lower: str) -> Tuple[float, List[str]]:
        """Check for PARTIAL payment indicators"""
        evidence = []
        score = 0.0
        
        for indicator in self.partial_indicators:
            if indicator in text_lower:
                evidence.append(f"PARTIAL: {indicator}")
                score += 0.4  # Higher score for partial indicators
        
        # Check for advance/token amounts
        advance_patterns = [
            r'advance\s*paid\s*:?\s*₹?\s*\d+',
            r'token\s*amount\s*:?\s*₹?\s*\d+',
            r'part\s*payment\s*:?\s*₹?\s*\d+',
            r'balance\s*due\s*:?\s*₹?\s*\d+'  # Strong indicator of partial payment
        ]
        for pattern in advance_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                evidence.append(f"ADVANCE: {matches[0]}")
                score += 0.5  # Strong indicator of partial payment
        
        return min(score, 1.0), evidence
    
    def _check_unpaid_indicators(self, text_lower: str) -> Tuple[float, List[str]]:
        """Check for UNPAID status indicators"""
        evidence = []
        score = 0.0
        
        for indicator in self.unpaid_indicators:
            if indicator in text_lower:
                evidence.append(f"UNPAID: {indicator}")
                score += 0.2
        
        # Check for due dates in future (indicates unpaid)
        due_patterns = [
            r'due\s*date\s*:?\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
            r'payment\s*due\s*:?\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
        ]
        for pattern in due_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                evidence.append(f"DUE_DATE: {matches[0]}")
                score += 0.3
        
        return min(score, 1.0), evidence
    
    def generate_robust_prompt(self) -> str:
        """Generate enhanced prompt for AI with robust payment detection"""
        
        return """Extract invoice data as JSON. CRITICAL: Robust payment status detection required.

REQUIRED: invoice_number, invoice_date (YYYY-MM-DD), vendor_name, total_amount (number), currency

PAYMENT STATUS DETECTION (CRITICAL - Look carefully):

PAID indicators (set status="paid"):
- STAMPS: "PAID", "PAYMENT RECEIVED", "CLEARED", "SETTLED"
- WATERMARKS: "PAID IN FULL", "FULLY PAID", "PAYMENT COMPLETE"
- TEXT: "payment received", "amount paid", "payment made", "credited", "settlement done"
- TRANSACTION IDs: Any UPI/NEFT/RTGS/transaction reference numbers
- SIGNATURES: "received by", "authorized signatory", payment acknowledgment
- PAYMENT METHODS: "UPI paid", "Cash received", "Cheque cleared", "Online payment made"

PARTIAL indicators (set status="partial"):
- "partial payment", "advance paid", "token amount", "down payment", "installment"
- Any mention of advance amounts or part payments

UNPAID indicators (set status="unpaid"):
- "due", "pending", "outstanding", "amount due", "balance payable", "overdue"
- Future due dates without payment confirmation

DEFAULT: If no clear indicators found, set status="unpaid"

OPTIONAL (only if visible): vendor_gstin, vendor_email, vendor_phone, vendor_address, due_date, po_number, subtotal, cgst, sgst, igst, cess, discount, shipping_charges, hsn_code, sac_code, place_of_supply, payment_method, line_items

Return ONLY JSON, no explanation."""

# Test the detector
if __name__ == "__main__":
    detector = PaymentStatusDetector()
    
    # Test cases
    test_cases = [
        ("Invoice with PAID stamp", "INVOICE #123\nTotal: ₹5000\nPAID\nReceived by: John"),
        ("UPI payment", "Invoice #456\nAmount: ₹3000\nUPI ID: merchant@paytm\nTxn ID: 123456789"),
        ("Partial payment", "Invoice #789\nTotal: ₹10000\nAdvance paid: ₹2000\nBalance due: ₹8000"),
        ("Unpaid invoice", "Invoice #999\nAmount: ₹7500\nDue date: 15/02/2025\nPayment pending")
    ]
    
    print("🔍 ROBUST PAYMENT STATUS DETECTION TEST")
    print("="*50)
    
    for description, text in test_cases:
        status, confidence, evidence = detector.detect_payment_status(text)
        print(f"\n📄 {description}")
        print(f"   Status: {status.upper()}")
        print(f"   Confidence: {confidence:.2f}")
        print(f"   Evidence: {evidence}")
    
    print(f"\n✅ Enhanced payment detection ready for integration!")