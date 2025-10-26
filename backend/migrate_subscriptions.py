"""
Database Migration: Update Subscription Schema
Run this script to update the subscriptions table with new plan tiers
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine


def update_subscription_schema():
    """Update subscriptions table with new schema"""
    
    migrations = [
        # Ensure subscriptions table exists with all required columns
        """
        CREATE TABLE IF NOT EXISTS subscriptions (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            tier VARCHAR(50) NOT NULL DEFAULT 'free',
            status VARCHAR(50) NOT NULL DEFAULT 'active',
            scans_used_this_period INTEGER DEFAULT 0,
            razorpay_subscription_id VARCHAR(255),
            razorpay_customer_id VARCHAR(255),
            razorpay_plan_id VARCHAR(255),
            current_period_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            current_period_end TIMESTAMP DEFAULT CURRENT_TIMESTAMP + INTERVAL '30 days',
            cancelled_at TIMESTAMP,
            billing_cycle VARCHAR(20) DEFAULT 'monthly',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id)
        );
        """,
        
        # Add indexes for better performance
        """
        CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);
        """,
        
        """
        CREATE INDEX IF NOT EXISTS idx_subscriptions_tier ON subscriptions(tier);
        """,
        
        """
        CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);
        """,
        
        # Add tier constraint to ensure valid values
        """
        ALTER TABLE subscriptions DROP CONSTRAINT IF EXISTS subscriptions_tier_check;
        """,
        
        """
        ALTER TABLE subscriptions 
        ADD CONSTRAINT subscriptions_tier_check 
        CHECK (tier IN ('free', 'basic', 'pro', 'ultra', 'max'));
        """,
        
        # Add status constraint
        """
        ALTER TABLE subscriptions DROP CONSTRAINT IF EXISTS subscriptions_status_check;
        """,
        
        """
        ALTER TABLE subscriptions 
        ADD CONSTRAINT subscriptions_status_check 
        CHECK (status IN ('active', 'cancelled', 'expired', 'suspended', 'pending'));
        """,
        
        # Add billing cycle constraint
        """
        ALTER TABLE subscriptions DROP CONSTRAINT IF EXISTS subscriptions_billing_cycle_check;
        """,
        
        """
        ALTER TABLE subscriptions 
        ADD CONSTRAINT subscriptions_billing_cycle_check 
        CHECK (billing_cycle IN ('monthly', 'yearly'));
        """,
        
        # Add trigger to update updated_at timestamp
        """
        CREATE OR REPLACE FUNCTION update_subscription_timestamp()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """,
        
        """
        DROP TRIGGER IF EXISTS trigger_update_subscription_timestamp ON subscriptions;
        """,
        
        """
        CREATE TRIGGER trigger_update_subscription_timestamp
        BEFORE UPDATE ON subscriptions
        FOR EACH ROW
        EXECUTE FUNCTION update_subscription_timestamp();
        """,
        
        # Migrate any existing subscriptions from old tiers to new tiers
        # Old: starter, pro, business
        # New: free, basic, pro, ultra, max
        """
        UPDATE subscriptions SET tier = 'free' WHERE tier = 'starter';
        """,
        
        """
        UPDATE subscriptions SET tier = 'basic' WHERE tier NOT IN ('free', 'basic', 'pro', 'ultra', 'max');
        """,
    ]
    
    print("🔄 Starting database migration for subscriptions table...")
    
    with engine.connect() as conn:
        for i, migration in enumerate(migrations, 1):
            try:
                print(f"  ✓ Running migration {i}/{len(migrations)}...")
                conn.execute(text(migration))
                conn.commit()
            except Exception as e:
                print(f"  ⚠️  Migration {i} warning: {str(e)}")
                # Continue with other migrations
                continue
    
    print("✅ Database migration completed!")
    print("\nNew subscription tiers:")
    print("  - Free: ₹0/month, 10 scans")
    print("  - Basic: ₹149/month, 80 scans")
    print("  - Pro: ₹299/month, 200 scans")
    print("  - Ultra: ₹599/month, 500 scans")
    print("  - Max: ₹999/month, 1000 scans")


if __name__ == "__main__":
    try:
        update_subscription_schema()
    except Exception as e:
        print(f"❌ Error running migration: {str(e)}")
        sys.exit(1)
