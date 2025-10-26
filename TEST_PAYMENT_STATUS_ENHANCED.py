#!/usr/bin/env python3
"""
🧪 TEST PAYMENT STATUS ENHANCEMENT
Verify improved payment status detection (80% → 90%+)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.flash_lite_formatter import FlashLiteFormatter


def test_payment_status_detection():
    """Test enhanced payment status detection"""
    
    print("\n" + "="*70)
    print("🧪 PAYMENT STATUS DETECTION ENHANCEMENT TESTS")
    print("="*70)
    
    formatter = FlashLiteFormatter()
    
    test_cases = [
        {
            "name": "Paid Invoice (Cheque)",
            "text": "Invoice: INV-001\nDate: 2024-01-15\nVendor: ABC Corp\nTotal: ₹1000\nStatus: Cheque attached - Payment cleared",
            "expected": "paid",
            "expected_conf_min": 0.90
        },
        {
            "name": "Paid Invoice (Direct Transfer)",
            "text": "Invoice: INV-002\nPayment received via bank transfer on 2024-01-15\nVendor: XYZ Ltd\nAmount: ₹5000",
            "expected": "paid",
            "expected_conf_min": 0.90
        },
        {
            "name": "Unpaid Invoice",
            "text": "Invoice: INV-003\nDate: 2024-01-15\nVendor: ABC Corp\nTotal: ₹2000\nStatus: Outstanding - Payment pending",
            "expected": "unpaid",
            "expected_conf_min": 0.85
        },
        {
            "name": "Not Paid Invoice",
            "text": "Invoice: INV-004\nVendor: Company A\nAmount: ₹3000\nPayment Status: Not paid\nPlease arrange payment",
            "expected": "unpaid",
            "expected_conf_min": 0.85
        },
        {
            "name": "Pending Invoice (Credit Terms)",
            "text": "Invoice: INV-005\nVendor: Supplier\nTotal: ₹7500\nPayment Terms: Net 30 days\nDue Date: 2024-02-15",
            "expected": "pending",
            "expected_conf_min": 0.75
        },
        {
            "name": "Pending Invoice (Credit)",
            "text": "Invoice: INV-006\nAmount: ₹4000\nCredit terms: 30 days credit extended\nVendor: Partner Co",
            "expected": "pending",
            "expected_conf_min": 0.75
        },
        {
            "name": "Overdue Invoice",
            "text": "Invoice: INV-007\nDue Date: 2023-12-15\nCurrent Date: 2024-01-15\nStatus: Overdue amount ₹5000 pending",
            "expected": "overdue",
            "expected_conf_min": 0.85
        },
        {
            "name": "Past Due Invoice",
            "text": "Invoice: INV-008\nVendor: ABC Ltd\nAmount: ₹8000\nStatus: Past due - 15 days overdue\nPlease pay immediately",
            "expected": "overdue",
            "expected_conf_min": 0.85
        },
        {
            "name": "Partially Paid",
            "text": "Invoice: INV-009\nTotal: ₹10000\nPayment received: ₹5000\nRemaining balance due: ₹5000",
            "expected": "partially_paid",
            "expected_conf_min": 0.65
        },
        {
            "name": "Unknown Status (Low Confidence)",
            "text": "Invoice: INV-010\nVendor: New Company\nTotal: ₹2000\nNo payment information provided",
            "expected": None,  # Can be anything, just needs confidence < 0.70
            "expected_conf_min": 0.0,
            "expected_conf_max": 0.70
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print(f"   Text: {test_case['text'][:60]}...")
        
        # Create a mock result dict to pass to enhancement
        mock_result = {
            "invoice_number": "INV-001",
            "vendor_name": "Test Vendor",
            "total_amount": 1000,
            "payment_status": "pending"  # Default before enhancement
        }
        
        # Run enhancement
        enhanced = formatter._enhance_payment_status(mock_result, test_case['text'])
        
        detected_status = enhanced.get('payment_status', 'unknown')
        detected_conf = enhanced.get('payment_status_confidence', 0)
        
        print(f"   Result: {detected_status}")
        print(f"   Confidence: {detected_conf:.0%}")
        
        # Check if correct
        if test_case['expected'] is None:
            # Just check confidence is in range
            if 'expected_conf_max' in test_case:
                if detected_conf <= test_case['expected_conf_max']:
                    print(f"   ✅ PASS (confidence in acceptable range)")
                    passed += 1
                else:
                    print(f"   ❌ FAIL (confidence too high: {detected_conf:.0%} > {test_case['expected_conf_max']:.0%})")
                    failed += 1
            else:
                print(f"   ✅ PASS")
                passed += 1
        else:
            # Check status and confidence
            status_match = detected_status == test_case['expected']
            conf_match = detected_conf >= test_case['expected_conf_min']
            
            if status_match and conf_match:
                print(f"   ✅ PASS (status={detected_status}, conf={detected_conf:.0%})")
                passed += 1
            else:
                reason = []
                if not status_match:
                    reason.append(f"status {detected_status} != {test_case['expected']}")
                if not conf_match:
                    reason.append(f"conf {detected_conf:.0%} < {test_case['expected_conf_min']:.0%}")
                print(f"   ❌ FAIL ({', '.join(reason)})")
                failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    print(f"✅ Passed: {passed}/{len(test_cases)}")
    print(f"❌ Failed: {failed}/{len(test_cases)}")
    
    accuracy_percent = (passed / len(test_cases)) * 100
    print(f"📈 Accuracy: {accuracy_percent:.1f}%")
    
    if accuracy_percent >= 90:
        print("\n🎉 EXCELLENT! Payment status detection improved to 90%+")
        print("   Improvement: 80% → 90%+ accuracy achieved!")
        return True
    elif accuracy_percent >= 80:
        print("\n✅ GOOD! Payment status detection at 80%+")
        print("   Improvement: Baseline 80% maintained")
        return True
    else:
        print(f"\n⚠️  NEEDS WORK! Accuracy only {accuracy_percent:.1f}%")
        return False


if __name__ == "__main__":
    try:
        success = test_payment_status_detection()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
