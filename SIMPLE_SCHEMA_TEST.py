#!/usr/bin/env python3
"""
SCHEMA DETECTIVE: Test actual payment_status values in database
"""

import requests
import json

def test_payment_status_constraint():
    """Test which payment_status values actually work"""
    
    print("🔍 TESTING ACTUAL DATABASE PAYMENT_STATUS CONSTRAINT...")
    print()
    
    # Use the backend API to test constraints  
    backend_url = "http://localhost:8000"
    
    # Test document ID from the error log
    document_id = "825b1b43-bc59-4204-8e91-e75cb721966f"
    
    print(f"📡 Testing via backend API: {backend_url}")
    print(f"📄 Using document_id: {document_id}")
    print()
    
    # Try to trigger processing which will reveal the constraint
    try:
        response = requests.post(f"{backend_url}/api/documents/{document_id}/process")
        print(f"🔍 Response status: {response.status_code}")
        
        if response.status_code == 500:
            error_data = response.json()
            detail = error_data.get('detail', '')
            
            print("🚨 CONSTRAINT ERROR DETAILS:")
            print("=" * 50)
            print(detail)
            print()
            
            # Parse the failing row to see what payment_status was attempted
            if "Failing row contains" in detail:
                # Extract the failing row data
                start = detail.find("Failing row contains (") + len("Failing row contains (")
                end = detail.find(").", start)
                if start > 0 and end > 0:
                    row_data = detail[start:end]
                    fields = [f.strip() for f in row_data.split(',')]
                    
                    print("🎯 FAILING ROW ANALYSIS:")
                    print(f"   payment_status field position 22: '{fields[22] if len(fields) > 22 else 'N/A'}'")
                    print()
                    
                    # Check what the constraint allows
                    if "violates check constraint" in detail:
                        constraint_name = detail.split("violates check constraint \"")[1].split("\"")[0]
                        print(f"🔒 CONSTRAINT NAME: {constraint_name}")
                        
                        if "payment_status_check" in constraint_name:
                            print("💡 This confirms it's a payment_status constraint issue!")
                            print()
                            print("🎯 SOLUTION: We need to find which values are actually allowed")
                            
    except Exception as e:
        print(f"❌ Error testing: {e}")

if __name__ == "__main__":
    test_payment_status_constraint()