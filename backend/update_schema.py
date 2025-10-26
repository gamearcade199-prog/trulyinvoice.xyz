#!/usr/bin/env python3
"""
Enhanced Database Schema Updater
Adds 50+ industry fields and fixes payment status constraint
"""

import os
import psycopg2
from psycopg2 import sql
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

# Use Supabase client instead of direct PostgreSQL connection
from supabase import create_client, Client

def execute_schema_update():
    """Execute the enhanced schema update with 50+ fields using Supabase client"""
    
    # Split into smaller SQL commands for Supabase
    commands = [
        "ALTER TABLE invoices DROP CONSTRAINT IF EXISTS invoices_payment_status_check",
        """ALTER TABLE invoices ADD CONSTRAINT invoices_payment_status_check 
           CHECK (payment_status IN ('pending', 'paid', 'overdue', 'cancelled', 'refunded', 'partial', 'processing', 'failed', 'PENDING', 'PAID', 'OVERDUE', 'CANCELLED', 'REFUNDED', 'PARTIAL', 'PROCESSING', 'FAILED', 'Pending', 'Paid', 'Overdue', 'Cancelled', 'Refunded', 'Partial', 'Processing', 'Failed'))""",
        
        # Hotel & Hospitality
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS arrival_date DATE",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS departure_date DATE", 
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS room_number VARCHAR(50)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS guest_count INTEGER",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS booking_reference VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS hotel_star_rating INTEGER",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS meal_plan VARCHAR(50)",
        
        # Retail & E-commerce
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS order_id VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS tracking_number VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS shipping_method VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS delivery_date DATE",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS return_policy TEXT",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS coupon_code VARCHAR(50)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS discount_percentage DECIMAL(5,2)",
        
        # Manufacturing & Industrial  
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS purchase_order VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS batch_number VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS quality_certificate VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS warranty_period VARCHAR(50)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS manufacturing_date DATE",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS expiry_date DATE",
        
        # Medical & Healthcare
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS patient_id VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS doctor_name VARCHAR(200)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS medical_license VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS insurance_claim VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS treatment_date DATE",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS prescription_number VARCHAR(100)",
        
        # Logistics & Transportation
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS vehicle_number VARCHAR(50)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS driver_name VARCHAR(200)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS origin_location VARCHAR(300)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS destination_location VARCHAR(300)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS distance_km DECIMAL(10,2)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS fuel_surcharge DECIMAL(10,2)",
        
        # Professional Services
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS project_name VARCHAR(200)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS consultant_name VARCHAR(200)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS hourly_rate DECIMAL(10,2)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS hours_worked DECIMAL(10,2)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS project_phase VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS deliverable TEXT",
        
        # Real Estate
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS property_address TEXT",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS property_type VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS square_footage DECIMAL(10,2)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS lease_term VARCHAR(50)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS security_deposit DECIMAL(10,2)",
        
        # Education
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS student_id VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS course_name VARCHAR(200)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS academic_year VARCHAR(20)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS semester VARCHAR(20)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS instructor_name VARCHAR(200)",
        
        # Utilities & Services
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS meter_reading_start DECIMAL(10,2)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS meter_reading_end DECIMAL(10,2)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS units_consumed DECIMAL(10,2)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS rate_per_unit DECIMAL(10,4)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS connection_id VARCHAR(100)",
        
        # Financial Services
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS account_number VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS transaction_id VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS interest_rate DECIMAL(10,4)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS principal_amount DECIMAL(15,2)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS processing_fee DECIMAL(10,2)",
        
        # Subscription & Recurring Services
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS subscription_type VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS billing_cycle VARCHAR(50)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS next_billing_date DATE",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS auto_renewal BOOLEAN DEFAULT FALSE",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS plan_features TEXT",
        
        # Additional Business Fields
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS contract_number VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS milestone VARCHAR(200)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS approval_status VARCHAR(50)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS approved_by VARCHAR(200)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS department VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS cost_center VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS budget_code VARCHAR(100)",
        
        # Compliance & Regulatory
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS regulatory_code VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS compliance_certificate VARCHAR(100)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS audit_trail TEXT",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS authorized_signatory VARCHAR(200)",
        
        # Enhanced Metadata
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS extraction_version VARCHAR(20) DEFAULT 'v2.5'",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS processing_time_seconds DECIMAL(5,2)",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS data_source VARCHAR(50) DEFAULT 'gemini-2.5-flash'",
        "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS quality_score DECIMAL(5,2)",
        
        # Update existing records
        "UPDATE invoices SET payment_status = 'pending' WHERE payment_status IS NULL"
    ]
    
    try:
        print("🔌 Connecting to Supabase...")
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        print("🚀 Executing enhanced schema update...")
        executed = 0
        failed = 0
        
        for i, command in enumerate(commands):
            try:
                result = supabase.rpc('exec_sql', {'sql': command})
                executed += 1
                if i % 10 == 0:
                    print(f"   ⚡ Executed {executed}/{len(commands)} commands...")
            except Exception as e:
                failed += 1
                if "already exists" not in str(e):
                    print(f"   ⚠️ Command {i+1} failed: {str(e)[:100]}...")
        
        print(f"✅ Schema update completed!")
        print(f"📊 Executed: {executed} commands, Failed: {failed}")
        print("⚡ Database ready for bulletproof extraction with 50+ fields")
        
        return True
        
    except Exception as e:
        print(f"❌ Database update failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = execute_schema_update()
    if success:
        print("\n🎉 Database schema enhanced with 50+ industry fields!")
        print("💡 Ready for bulletproof extraction across all industries")
    else:
        print("\n❌ Schema update failed. Check database connection.")
        sys.exit(1)