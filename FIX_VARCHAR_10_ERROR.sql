-- Fix for "value too long for type character varying(10)" Error
-- This fixes columns that are too short for the data being inserted

-- CRITICAL FIX: Extend columns that might receive long values

-- 1. Currency field (might receive "Indian Rupee" instead of "INR")
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'currency'
    ) THEN
        ALTER TABLE invoices ALTER COLUMN currency TYPE VARCHAR(50);
        RAISE NOTICE '✅ Extended currency column to VARCHAR(50)';
    END IF;
END $$;

-- 2. Vendor PAN (PAN can be alphanumeric, sometimes with formatting)
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_pan'
    ) THEN
        ALTER TABLE invoices ALTER COLUMN vendor_pan TYPE VARCHAR(50);
        RAISE NOTICE '✅ Extended vendor_pan column to VARCHAR(50)';
    END IF;
END $$;

-- 3. Vendor TAN (TAN can have formatting)
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_tan'
    ) THEN
        ALTER TABLE invoices ALTER COLUMN vendor_tan TYPE VARCHAR(50);
        RAISE NOTICE '✅ Extended vendor_tan column to VARCHAR(50)';
    END IF;
END $$;

-- 4. Vendor Pincode (Indian pincodes are 6 digits, but might have formatting)
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'vendor_pincode'
    ) THEN
        ALTER TABLE invoices ALTER COLUMN vendor_pincode TYPE VARCHAR(20);
        RAISE NOTICE '✅ Extended vendor_pincode column to VARCHAR(20)';
    END IF;
END $$;

-- 5. Place of Supply (Indian state names can be long, e.g., "Arunachal Pradesh")
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'place_of_supply'
    ) THEN
        ALTER TABLE invoices ALTER COLUMN place_of_supply TYPE VARCHAR(100);
        RAISE NOTICE '✅ Extended place_of_supply column to VARCHAR(100)';
    END IF;
END $$;

-- 6. Payment Status (might have values like "Partially Paid", "Overdue", etc.)
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'payment_status'
    ) THEN
        ALTER TABLE invoices ALTER COLUMN payment_status TYPE VARCHAR(50);
        RAISE NOTICE '✅ Extended payment_status column to VARCHAR(50)';
    END IF;
END $$;

-- 7. Payment Method (might have values like "Net Banking", "Credit Card", etc.)
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'invoices' AND column_name = 'payment_method'
    ) THEN
        ALTER TABLE invoices ALTER COLUMN payment_method TYPE VARCHAR(50);
        RAISE NOTICE '✅ Extended payment_method column to VARCHAR(50)';
    END IF;
END $$;

-- Verify the changes
SELECT 
    column_name,
    data_type,
    character_maximum_length
FROM information_schema.columns
WHERE table_name = 'invoices'
    AND column_name IN (
        'currency', 'vendor_pan', 'vendor_tan', 'vendor_pincode', 
        'place_of_supply', 'payment_status', 'payment_method'
    )
ORDER BY column_name;

-- Success message
DO $$ 
BEGIN
    RAISE NOTICE '🎉 All column sizes fixed! Your invoices should now upload without errors.';
END $$;
