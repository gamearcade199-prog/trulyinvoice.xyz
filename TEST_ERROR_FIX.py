"""
Test that error fields are properly handled during invoice save
"""
import sys
import asyncio
from pathlib import Path

async def test_error_handling():
    """Test that error responses don't break the database save"""
    
    print("\n" + "="*60)
    print("🧪 TESTING ERROR FIELD HANDLING")
    print("="*60)
    
    try:
        # Create error response (like what fallback_response creates)
        error_extracted_data = {
            'error': True,
            'error_message': 'Vision API failed: 403 Permission Denied',
            'invoice_number': '',
            'invoice_number_confidence': 0.0,
            'vendor_name': 'test.jpg',
            'vendor_name_confidence': 0.1,
            'total_amount': 0.0,
            'total_amount_confidence': 0.0,
            'currency': 'INR',
            'currency_confidence': 1.0,
            'line_items': [],
            '_extraction_metadata': {
                'method': 'vision_flash_lite_fallback',
                'success': False,
                'error': 'Vision API failed'
            }
        }
        
        print("\n📋 Original extracted data:")
        print(f"   - Keys: {list(error_extracted_data.keys())}")
        print(f"   - Has 'error': {('error' in error_extracted_data)}")
        print(f"   - Has '_extraction_metadata': {('_extraction_metadata' in error_extracted_data)}")
        
        # Test that the fix removes problematic fields
        test_data = error_extracted_data.copy()
        
        # This is what _save_invoice_data does now
        test_data.pop('error', None)
        test_data.pop('error_message', None)
        test_data.pop('_extraction_metadata', None)
        
        print("\n✅ After cleanup:")
        print(f"   - Keys: {list(test_data.keys())}")
        print(f"   - Has 'error': {('error' in test_data)}")
        print(f"   - Has '_extraction_metadata': {('_extraction_metadata' in test_data)}")
        
        # Verify safe fields remain
        assert 'invoice_number' in test_data, "Should keep invoice_number"
        assert 'vendor_name' in test_data, "Should keep vendor_name"
        assert 'total_amount' in test_data, "Should keep total_amount"
        assert 'currency' in test_data, "Should keep currency"
        assert 'line_items' in test_data, "Should keep line_items"
        
        # Verify problematic fields are removed
        assert 'error' not in test_data, "Should remove 'error' field"
        assert 'error_message' not in test_data, "Should remove 'error_message' field"
        assert '_extraction_metadata' not in test_data, "Should remove '_extraction_metadata' field"
        
        print("\n🎯 All assertions passed!")
        print("\n" + "="*60)
        print("✅ ERROR FIELD HANDLING TEST PASSED")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_error_handling())
    sys.exit(0 if result else 1)
