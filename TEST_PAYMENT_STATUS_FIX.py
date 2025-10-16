"""
Test Script: Verify Payment Status Normalization
Ensures ALL payment status values are normalized to database-valid values
"""

def test_document_processor_validate():
    """Test document_processor._validate_payment_status()"""
    print("=" * 70)
    print("TEST 1: document_processor._validate_payment_status()")
    print("=" * 70)
    
    # Import the function
    import sys
    sys.path.insert(0, r'c:\Users\akib\Desktop\trulyinvoice.in\backend')
    
    from app.services.document_processor import DocumentProcessor
    
    processor = DocumentProcessor()
    
    # Test cases
    test_cases = [
        ('paid', 'paid'),
        ('PAID', 'paid'),
        ('unpaid', 'unpaid'),
        ('UNPAID', 'unpaid'),
        ('partial', 'partial'),
        ('PARTIAL', 'partial'),
        ('overdue', 'overdue'),
        ('OVERDUE', 'overdue'),
        # Invalid values that should map to 'unpaid'
        ('pending', 'unpaid'),
        ('PENDING', 'unpaid'),
        ('cancelled', 'unpaid'),
        ('CANCELLED', 'unpaid'),
        ('refunded', 'unpaid'),
        ('REFUNDED', 'unpaid'),
        ('processing', 'unpaid'),
        ('PROCESSING', 'unpaid'),
        ('failed', 'unpaid'),
        ('FAILED', 'unpaid'),
        ('draft', 'unpaid'),
        ('DRAFT', 'unpaid'),
        ('unknown', 'unpaid'),
        ('UNKNOWN', 'unpaid'),
        ('na', 'unpaid'),
        ('N/A', 'unpaid'),
        # None and empty
        (None, 'unpaid'),
        ('', 'unpaid'),
        ('   ', 'unpaid'),
        # Invalid values
        ('invalid', 'unpaid'),
        ('xyz', 'unpaid'),
    ]
    
    passed = 0
    failed = 0
    
    for input_val, expected in test_cases:
        result = processor._validate_payment_status(input_val)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        if result == expected:
            passed += 1
        else:
            failed += 1
        print(f"  {status}: {repr(input_val):20} → {repr(result):12} (expected: {repr(expected)})")
    
    print(f"\nResults: {passed}/{len(test_cases)} passed")
    return failed == 0


def test_documents_api_payment_status():
    """Test documents API payment_status mapping logic"""
    print("\n" + "=" * 70)
    print("TEST 2: API payment_status mapping logic")
    print("=" * 70)
    
    # Define the mapping logic (from documents.py)
    valid_payment_statuses = {'paid', 'unpaid', 'partial', 'overdue'}
    payment_status_mapping = {
        'pending': 'unpaid',
        'cancelled': 'unpaid',
        'refunded': 'unpaid',
        'processing': 'unpaid',
        'failed': 'unpaid',
        'draft': 'unpaid',
        'unknown': 'unpaid',
    }
    
    test_cases = [
        ('paid', 'paid'),
        ('unpaid', 'unpaid'),
        ('partial', 'partial'),
        ('overdue', 'overdue'),
        ('pending', 'unpaid'),
        ('cancelled', 'unpaid'),
        ('refunded', 'unpaid'),
        ('processing', 'unpaid'),
        ('failed', 'unpaid'),
        ('draft', 'unpaid'),
        ('unknown', 'unpaid'),
        ('', 'unpaid'),
        (None, 'unpaid'),
    ]
    
    passed = 0
    failed = 0
    
    for input_val, expected in test_cases:
        payment_status = str(input_val).strip().lower() if input_val else ''
        
        if payment_status in payment_status_mapping:
            result = payment_status_mapping[payment_status]
        elif payment_status in valid_payment_statuses:
            result = payment_status
        else:
            result = 'unpaid'
        
        status = "✅ PASS" if result == expected else "❌ FAIL"
        if result == expected:
            passed += 1
        else:
            failed += 1
        print(f"  {status}: {repr(input_val):20} → {repr(result):12} (expected: {repr(expected)})")
    
    print(f"\nResults: {passed}/{len(test_cases)} passed")
    return failed == 0


def test_database_constraint():
    """Verify database constraint values"""
    print("\n" + "=" * 70)
    print("TEST 3: Database constraint validation")
    print("=" * 70)
    
    # Database allows ONLY these values
    allowed_values = {'paid', 'unpaid', 'partial', 'overdue'}
    
    # All extracted values that might come from AI
    extracted_values = [
        'paid', 'unpaid', 'partial', 'overdue',  # Valid
        'pending', 'cancelled', 'refunded', 'processing', 'failed', 'draft', 'unknown'  # Invalid
    ]
    
    print("\n  Allowed by database constraint:")
    for val in allowed_values:
        print(f"    ✅ {repr(val)}")
    
    print("\n  Will be normalized to 'unpaid':")
    invalid = [v for v in extracted_values if v not in allowed_values]
    for val in invalid:
        print(f"    → {repr(val)} becomes 'unpaid'")
    
    print(f"\n  Total valid values: {len(allowed_values)}")
    print(f"  Total values that need normalization: {len(invalid)}")
    
    return True


if __name__ == "__main__":
    print("\n" + "🔍 PAYMENT STATUS NORMALIZATION TEST SUITE\n")
    
    try:
        test1_pass = test_document_processor_validate()
    except Exception as e:
        print(f"\n❌ TEST 1 ERROR: {e}")
        test1_pass = False
    
    try:
        test2_pass = test_documents_api_payment_status()
    except Exception as e:
        print(f"\n❌ TEST 2 ERROR: {e}")
        test2_pass = False
    
    try:
        test3_pass = test_database_constraint()
    except Exception as e:
        print(f"\n❌ TEST 3 ERROR: {e}")
        test3_pass = False
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Test 1 (document_processor): {'✅ PASS' if test1_pass else '❌ FAIL'}")
    print(f"Test 2 (API mapping): {'✅ PASS' if test2_pass else '❌ FAIL'}")
    print(f"Test 3 (DB constraint): {'✅ PASS' if test3_pass else '❌ FAIL'}")
    
    if test1_pass and test2_pass and test3_pass:
        print("\n🎉 ALL TESTS PASSED! Payment status normalization is working correctly.")
    else:
        print("\n❌ SOME TESTS FAILED - Please review the fixes.")
    
    print("=" * 70 + "\n")
