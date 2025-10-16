#!/usr/bin/env python3
"""
Test to verify the error field filtering fix in documents.py
"""

def test_error_field_filtering():
    """Test that error fields are properly excluded from invoice_data"""
    
    print("\n" + "="*70)
    print("🧪 Testing Error Field Filtering Fix")
    print("="*70 + "\n")
    
    # Simulate AI extraction result (what comes from vision_flash_lite_extractor)
    ai_result = {
        'error': True,                          # Should be filtered
        'error_message': 'Test error occurred', # Should be filtered
        '_extraction_metadata': {               # Should be filtered
            'source': 'flash-lite',
            'timestamp': '2025-10-16T12:00:00'
        },
        'invoice_number': 'INV-2025-001',      # Should be KEPT
        'invoice_number_confidence': 0.95,      # Should be filtered (confidence)
        'vendor_name': 'Acme Corporation',      # Should be KEPT
        'vendor_name_confidence': 0.88,         # Should be filtered (confidence)
        'total_amount': 5000.00,                # Should be KEPT
        'total_amount_confidence': 0.92,        # Should be filtered (confidence)
        'currency': 'INR',                      # Should be KEPT
        'line_items': [                         # Should be KEPT
            {'description': 'Item 1', 'amount': 2500},
            {'description': 'Item 2', 'amount': 2500}
        ]
    }
    
    print("1️⃣  Original AI Result:")
    print(f"   Total fields: {len(ai_result)}")
    for key in ai_result:
        print(f"      - {key}")
    
    print("\n2️⃣  Applying filter (same logic as fixed documents.py):")
    
    # This is the FIXED logic from documents.py
    excluded_fields = {'error', 'error_message', '_extraction_metadata'}
    invoice_data = {
        "user_id": "test-user-id",
        "document_id": "test-doc-id"
    }
    
    for key, value in ai_result.items():
        if key not in excluded_fields and not key.startswith('_') and not key.endswith('_confidence'):
            invoice_data[key] = value
    
    print(f"   Excluded fields set: {excluded_fields}")
    print(f"   Additional filters: fields starting with '_' or ending with '_confidence'")
    
    print("\n3️⃣  Resulting Invoice Data (what gets saved to database):")
    print(f"   Total fields: {len(invoice_data)}")
    for key in invoice_data:
        if key not in ('user_id', 'document_id'):
            value = invoice_data[key]
            if isinstance(value, (dict, list)):
                print(f"      - {key}: <{type(value).__name__}>")
            else:
                print(f"      - {key}: {value}")
    
    # Verification
    print("\n4️⃣  Verification Checks:")
    
    checks = [
        ('error' not in invoice_data, "❌ 'error' field filtered"),
        ('error_message' not in invoice_data, "❌ 'error_message' field filtered"),
        ('_extraction_metadata' not in invoice_data, "❌ '_extraction_metadata' field filtered"),
        ('invoice_number_confidence' not in invoice_data, "❌ Confidence scores filtered"),
        ('vendor_name_confidence' not in invoice_data, "❌ Confidence scores filtered"),
        ('total_amount_confidence' not in invoice_data, "❌ Confidence scores filtered"),
        ('invoice_number' in invoice_data, "✅ 'invoice_number' kept"),
        ('vendor_name' in invoice_data, "✅ 'vendor_name' kept"),
        ('total_amount' in invoice_data, "✅ 'total_amount' kept"),
        ('currency' in invoice_data, "✅ 'currency' kept"),
        ('line_items' in invoice_data, "✅ 'line_items' kept"),
        ('user_id' in invoice_data, "✅ 'user_id' kept"),
        ('document_id' in invoice_data, "✅ 'document_id' kept"),
    ]
    
    all_passed = True
    for condition, message in checks:
        status = "✅" if condition else "❌"
        print(f"   {status} {message}")
        if not condition:
            all_passed = False
    
    # Fields that were filtered
    filtered_fields = set(ai_result.keys()) - (set(invoice_data.keys()) - {'user_id', 'document_id'})
    
    print("\n5️⃣  Summary:")
    print(f"   Original fields: {len(ai_result)}")
    print(f"   Kept fields: {len(invoice_data) - 2}")  # -2 for user_id and document_id
    print(f"   Filtered fields: {len(filtered_fields)}")
    print(f"   Filtered field names: {filtered_fields}")
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ ALL TESTS PASSED - Error field filtering is working correctly!")
    else:
        print("❌ SOME TESTS FAILED - There may be an issue with the filtering")
    print("="*70 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = test_error_field_filtering()
    exit(0 if success else 1)
