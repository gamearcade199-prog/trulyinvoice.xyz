# 📋 SUPABASE DATABASE SCHEMA REFERENCE

## Quick Navigation

- **4 Main Tables**
- **120+ Columns in invoices table**
- **50+ Extractable Fields**
- **Complete Field Definitions**
- **Data Types & Constraints**
- **Relationships & Foreign Keys**

---

## 📊 TABLE 1: Users

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    company_name VARCHAR(255),
    gstin VARCHAR(15),
    pan VARCHAR(10),
    tan VARCHAR(10),
    address TEXT,
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_gstin ON users(gstin);
```

**Purpose:** User authentication & account management  
**Primary Use:** Store user login credentials and company details  
**Relationships:** Referenced by invoices, documents, categories

**Fields:**
| Field | Type | Purpose |
|-------|------|---------|
| `id` | UUID | Unique user ID |
| `email` | VARCHAR | Login email (unique) |
| `hashed_password` | VARCHAR | Encrypted password |
| `full_name` | VARCHAR | User's name |
| `company_name` | VARCHAR | Company/business name |
| `gstin` | VARCHAR(15) | GST registration number |
| `pan` | VARCHAR(10) | PAN for income tax |
| `is_active` | BOOLEAN | Account status |
| `is_verified` | BOOLEAN | Email verified? |
| `created_at` | TIMESTAMP | Account creation date |
| `updated_at` | TIMESTAMP | Last update date |

---

## 📄 TABLE 2: Documents

```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    file_url TEXT,
    file_size INTEGER,
    mime_type VARCHAR(100),
    processing_status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_documents_status ON documents(processing_status);
```

**Purpose:** Track uploaded invoice files  
**Primary Use:** Store metadata about invoice documents before/during processing  
**Relationships:** References users; Referenced by invoices

**Fields:**
| Field | Type | Purpose |
|-------|------|---------|
| `id` | UUID | Unique document ID |
| `user_id` | UUID | Who uploaded this file |
| `file_name` | VARCHAR | Original filename (invoice_2025.pdf) |
| `storage_path` | VARCHAR | Path in Supabase Storage |
| `file_url` | TEXT | Public/private URL to access file |
| `file_size` | INTEGER | File size in bytes |
| `mime_type` | VARCHAR | File type (application/pdf, image/jpeg) |
| `processing_status` | VARCHAR | pending/processing/completed/failed |
| `created_at` | TIMESTAMP | Upload date |
| `updated_at` | TIMESTAMP | Last modification |

---

## 🧾 TABLE 3: Invoices (MAIN TABLE)

This is your primary table with 120+ columns for storing extracted invoice data.

### Section 3A: Core / Required Fields

```sql
-- PRIMARY KEY & RELATIONSHIPS
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
category_id UUID REFERENCES categories(id) ON DELETE SET NULL,

-- REQUIRED INVOICE INFORMATION (Must be present)
invoice_number VARCHAR(100) NOT NULL,
invoice_date DATE NOT NULL,
vendor_name VARCHAR(255) NOT NULL,
total_amount DECIMAL(15,2) NOT NULL,
payment_status VARCHAR(50) DEFAULT 'unpaid',

-- TIMESTAMPS
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

**Constraints:**
```sql
-- Payment status must be one of these values
CHECK (payment_status IN (
    'paid',
    'unpaid',
    'partial',
    'overdue',
    'pending',
    'cancelled',
    'refunded',
    'processing',
    'failed'
))
```

---

### Section 3B: Vendor Information (Optional)

```sql
-- VENDOR IDENTIFICATION
vendor_gstin VARCHAR(15),        -- GST registration number
vendor_pan VARCHAR(10),          -- PAN number
vendor_tan VARCHAR(10),          -- TAN number

-- VENDOR CONTACT DETAILS
vendor_email VARCHAR(255),
vendor_phone VARCHAR(20),

-- VENDOR ADDRESS
vendor_address TEXT,
vendor_state VARCHAR(100),
vendor_city VARCHAR(100),
vendor_pincode VARCHAR(10),

-- VENDOR TYPE
vendor_type VARCHAR(50),         -- Registered/Unregistered/Composition
vendor_cin VARCHAR(21),          -- Corporate Identification Number
```

**Example Data:**
```
vendor_name: "ACME Corporation Ltd."
vendor_gstin: "18AABCT1234Q1Z2"
vendor_pan: "AABCT1234P"
vendor_email: "sales@acme.com"
vendor_phone: "+91-9876543210"
vendor_address: "Plot 123, Tech Park, Mumbai"
vendor_state: "Maharashtra"
vendor_pincode: "400001"
vendor_type: "Registered"
```

---

### Section 3C: Customer/Buyer Information (Optional)

```sql
-- CUSTOMER IDENTIFICATION
customer_name VARCHAR(255),
customer_gstin VARCHAR(15),
customer_pan VARCHAR(10),

-- CUSTOMER CONTACT
customer_email VARCHAR(255),
customer_phone VARCHAR(20),

-- CUSTOMER ADDRESS
customer_address TEXT,
customer_state VARCHAR(100),
customer_city VARCHAR(100),
customer_pincode VARCHAR(10),
```

**When Used:** B2B invoices with buyer details

---

### Section 3D: Dates & References (Optional)

```sql
-- INVOICE DATES
invoice_date DATE,               -- Creation date
due_date DATE,                   -- Payment due date
delivery_date DATE,              -- Delivery date

-- REFERENCES
po_number VARCHAR(100),          -- Purchase Order #
po_date DATE,                    -- PO creation date
challan_number VARCHAR(100),     -- Delivery note #
eway_bill_number VARCHAR(50),    -- E-way bill #
lr_number VARCHAR(100),          -- Lorry receipt #
```

**Example:**
```
invoice_date: 2025-10-15
due_date: 2025-11-14 (Net 30)
po_number: "PO-2025-5678"
eway_bill_number: "402034567890"
```

---

### Section 3E: Financial Amounts (Optional, DECIMAL 15,2)

```sql
-- BASIC AMOUNTS
subtotal DECIMAL(15,2),          -- Before tax
taxable_amount DECIMAL(15,2),    -- Amount subject to tax
total_amount DECIMAL(15,2),      -- Final total (REQUIRED)

-- GST COMPONENTS (Indian GST System)
cgst DECIMAL(15,2),              -- Central GST (9%, 18%, etc.)
sgst DECIMAL(15,2),              -- State GST (9%, 18%, etc.)
igst DECIMAL(15,2),              -- Integrated GST (interstate)
ugst DECIMAL(15,2),              -- Union Territory GST
cess DECIMAL(15,2),              -- Additional cess
total_gst DECIMAL(15,2),         -- Total GST paid

-- OLD TAX SYSTEM (Pre-GST invoices)
vat DECIMAL(15,2),               -- Value Added Tax
service_tax DECIMAL(15,2),       -- Service tax

-- TAX DEDUCTIONS
tds_amount DECIMAL(15,2),        -- Tax Deducted at Source
tds_percentage DECIMAL(5,2),     -- TDS percentage
tcs_amount DECIMAL(15,2),        -- Tax Collected at Source

-- DISCOUNTS & CHARGES
discount DECIMAL(15,2),          -- Discount amount
discount_percentage DECIMAL(5,2), -- Discount %
shipping_charges DECIMAL(15,2),  -- Delivery cost
freight_charges DECIMAL(15,2),   -- Freight cost
packing_charges DECIMAL(15,2),   -- Packing cost
handling_charges DECIMAL(15,2),  -- Handling cost
insurance_charges DECIMAL(15,2), -- Insurance
other_charges DECIMAL(15,2),     -- Miscellaneous
advance_paid DECIMAL(15,2),      -- Advance payment
roundoff DECIMAL(15,2),          -- Rounding adjustment
```

**Example Invoice Calculation:**
```
Item Amount:           ₹10,000.00
Discount (10%):        -₹1,000.00
Subtotal:              ₹9,000.00
CGST (9%):             ₹810.00
SGST (9%):             ₹810.00
Total GST:             ₹1,620.00
Shipping:              ₹200.00
Total:                 ₹11,020.00
(Stored in total_amount)
```

---

### Section 3F: GST Classification Codes (Optional)

```sql
-- HSN/SAC CODES
hsn_code VARCHAR(20),            -- Harmonized System Number (for goods)
sac_code VARCHAR(20),            -- Service Accounting Code (for services)

-- GST SPECIFIC
place_of_supply VARCHAR(100),    -- State where supply happens
reverse_charge BOOLEAN DEFAULT false, -- RCM applicable?
invoice_type VARCHAR(50),        -- B2B, B2C, Export, SEZ, etc.
supply_type VARCHAR(50),         -- Goods, Services, or Both
```

**Examples:**
```
hsn_code: "6204" (Trousers, women's, of cotton)
sac_code: "9980" (B2B Consulting Services)
place_of_supply: "Maharashtra"
reverse_charge: true
invoice_type: "B2B"
supply_type: "Services"
```

---

### Section 3G: Import/Export Fields (Optional)

```sql
-- IMPORT DOCUMENTATION
bill_of_entry VARCHAR(100),      -- Import bill number
bill_of_entry_date DATE,         -- Bill date
port_code VARCHAR(20),           -- Port of import/export
country_of_origin VARCHAR(100),  -- Origin country

-- EXPORT DETAILS
shipping_bill_no VARCHAR(50),    -- Shipping bill number
shipping_bill_date DATE,
dest_country VARCHAR(100),       -- Destination country
```

---

### Section 3H: Line Items (JSONB Array)

```sql
-- ITEMS TABLE (stored as JSONB array in invoices table)
line_items JSONB,               -- Array of items

-- Line Item Structure:
[
  {
    "description": "Professional Consulting Services",
    "quantity": 2,
    "unit": "hours",
    "rate": 5000,
    "amount": 10000,
    "hsn_code": "9980",
    "tax_rate": 18,
    "tax_amount": 1800,
    "confidence": 0.95
  },
  {
    "description": "Software License",
    "quantity": 1,
    "unit": "subscription",
    "rate": 15000,
    "amount": 15000,
    "sac_code": "62019",
    "tax_rate": 18,
    "tax_amount": 2700,
    "confidence": 0.90
  }
]
```

---

### Section 3I: Bank & Payment Details (Optional)

```sql
-- BANK ACCOUNT (for payment)
bank_name VARCHAR(100),          -- Receiving bank name
bank_account_number VARCHAR(20), -- Account number
bank_ifsc_code VARCHAR(11),      -- IFSC code for transfers
account_holder_name VARCHAR(100),

-- PAYMENT TERMS
payment_terms VARCHAR(100),      -- e.g., "Net 30", "Due on receipt"
terms_of_payment TEXT,           -- Detailed payment terms
```

---

### Section 3J: Additional Business Fields (Optional)

```sql
-- VEHICLE/TRANSPORT
vehicle_number VARCHAR(20),      -- Registration number
vehicle_type VARCHAR(50),        -- Truck, Container, etc.
transporter_name VARCHAR(100),
transport_mode VARCHAR(50),      -- Road, Air, Rail, Sea

-- QUALITY CONTROL
batch_number VARCHAR(50),        -- Batch/Lot number
expiry_date DATE,                -- Expiry date (for goods)

-- ORDER TRACKING
order_number VARCHAR(100),       -- Internal order number
so_number VARCHAR(100),          -- Sales order number
```

---

### Section 3K: Data Quality & Metadata (Optional)

```sql
-- EXTRACTION METADATA
raw_extracted_data JSONB,        -- Complete extraction output (for debugging)
extraction_confidence DECIMAL(3,2),  -- Overall confidence (0.00-1.00)
extraction_method VARCHAR(100),  -- "vision_flash_lite", "manual_entry", etc.
last_updated_by VARCHAR(100),    -- User who last edited

-- DATA QUALITY FLAGS
requires_review BOOLEAN DEFAULT false,
is_verified BOOLEAN DEFAULT false,
verification_date TIMESTAMP,
verified_by VARCHAR(100),
```

**Example raw_extracted_data:**
```json
{
  "_extraction_metadata": {
    "method": "vision_flash_lite",
    "vision_api_cost_inr": 0.12,
    "flash_lite_cost_inr": 0.01,
    "total_cost_inr": 0.13,
    "processing_time_seconds": 4.2,
    "vision_confidence": 0.95,
    "text_length": 456,
    "filename": "invoice_2025-10-15.jpg",
    "success": true
  },
  "extracted_fields": {
    "invoice_number": {
      "value": "INV-2025-001",
      "confidence": 0.99
    },
    "vendor_name": {
      "value": "ACME Corp",
      "confidence": 0.98
    }
  }
}
```

---

## 📂 TABLE 4: Categories

```sql
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    color VARCHAR(10),             -- Hex color code (#FF5733)
    icon VARCHAR(50),              -- Icon name (folder, tag, briefcase)
    sort_order INTEGER,            -- Display order
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_categories_user_id ON categories(user_id);
```

**Purpose:** User-defined categories for organizing invoices  
**Primary Use:** Group invoices by vendor, project, type, etc.

**Fields:**
| Field | Type | Purpose |
|-------|------|---------|
| `id` | UUID | Unique category ID |
| `user_id` | UUID | Which user owns this |
| `name` | VARCHAR | Category name (e.g., "Vendors", "Projects") |
| `description` | TEXT | Optional description |
| `color` | VARCHAR | Color for UI (#FF5733) |
| `sort_order` | INTEGER | Display order |

**Example Categories:**
```
1. Vendors
2. Travel & Entertainment
3. Office Supplies
4. Utilities
5. Contractors
6. Government
```

---

## 🔗 Entity Relationship Diagram

```
┌─────────────┐
│   Users     │ (1 user)
└─────────────┘
      │
      ├─────────────────┬──────────────┐
      │                 │              │
      ↓                 ↓              ↓
┌──────────────┐  ┌─────────────┐  ┌────────────┐
│  Documents   │  │  Invoices   │  │ Categories │
│ (uploaded    │  │ (extracted  │  │ (user-     │
│  files)      │  │  data)      │  │  defined)  │
└──────────────┘  └─────────────┘  └────────────┘
      │                 │
      └─────────┬───────┘
                │
           (many-to-many)
```

**Relationships:**
- 1 User → Many Documents
- 1 User → Many Invoices
- 1 User → Many Categories
- 1 Document → 1 Invoice (optional)
- 1 Category → Many Invoices (optional)

---

## 🔐 Row-Level Security (RLS)

### Active RLS Policies

```sql
-- Users can only see their own invoices
CREATE POLICY "Users view own invoices"
ON invoices FOR SELECT
USING (auth.uid() = user_id);

-- Users can only create invoices for themselves
CREATE POLICY "Users create own invoices"
ON invoices FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can only update their own invoices
CREATE POLICY "Users update own invoices"
ON invoices FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Users can only delete their own invoices
CREATE POLICY "Users delete own invoices"
ON invoices FOR DELETE
USING (auth.uid() = user_id);

-- Similar policies for documents and categories
```

**Security Benefit:** Even if someone gets database access, they can only see/modify their own data.

---

## 📊 Data Types Reference

| Type | Range | Example | Usage |
|------|-------|---------|-------|
| UUID | 128-bit | 550e8400-e29b-41d4-a716-446655440001 | IDs |
| VARCHAR(n) | 1-n chars | "ACME Corp" | Text, limited |
| TEXT | Unlimited | Full addresses, descriptions | Long text |
| DATE | YYYY-MM-DD | 2025-10-15 | Dates only |
| TIMESTAMP | With time | 2025-10-15 14:30:45 | Date + time |
| DECIMAL(15,2) | ±999,999,999,999.99 | 11234.56 | Money |
| BOOLEAN | TRUE/FALSE | true | Yes/No |
| JSONB | JSON object | {"key": "value"} | Complex data |
| INTEGER | ±2,147,483,647 | 100 | Whole numbers |

---

## 📈 Sample Invoice Record

```sql
SELECT 
    id,
    user_id,
    invoice_number,
    invoice_date,
    vendor_name,
    vendor_gstin,
    total_amount,
    subtotal,
    cgst,
    sgst,
    total_gst,
    payment_status,
    line_items,
    created_at,
    updated_at
FROM invoices
WHERE id = '550e8400-e29b-41d4-a716-446655440001';

-- Result:
id:                 550e8400-e29b-41d4-a716-446655440001
user_id:            100e8400-e29b-41d4-a716-446655440001
invoice_number:     INV-2025-5678
invoice_date:       2025-10-15
vendor_name:        ACME Corporation
vendor_gstin:       18AABCT1234Q1Z2
total_amount:       11800.00
subtotal:           10000.00
cgst:               900.00
sgst:               900.00
total_gst:          1800.00
payment_status:     pending
line_items:         [{"description": "Consulting", "quantity": 1, "amount": 10000}]
created_at:         2025-10-15 14:30:45
updated_at:         2025-10-15 14:30:45
```

---

## 🔍 Useful SQL Queries

### Get All Invoices for a User

```sql
SELECT 
    invoice_number,
    vendor_name,
    total_amount,
    payment_status,
    invoice_date
FROM invoices
WHERE user_id = 'YOUR_USER_ID'
ORDER BY invoice_date DESC;
```

### Get Unpaid Invoices

```sql
SELECT 
    invoice_number,
    vendor_name,
    total_amount,
    invoice_date,
    due_date
FROM invoices
WHERE user_id = 'YOUR_USER_ID'
  AND payment_status = 'unpaid'
ORDER BY due_date ASC;
```

### Get Total GST by Month

```sql
SELECT 
    DATE_TRUNC('month', invoice_date) as month,
    SUM(cgst + sgst + igst) as total_gst,
    COUNT(*) as invoice_count
FROM invoices
WHERE user_id = 'YOUR_USER_ID'
GROUP BY DATE_TRUNC('month', invoice_date)
ORDER BY month DESC;
```

### Search Invoices by Vendor

```sql
SELECT 
    invoice_number,
    vendor_name,
    total_amount,
    invoice_date
FROM invoices
WHERE user_id = 'YOUR_USER_ID'
  AND vendor_name ILIKE '%ACME%'
ORDER BY invoice_date DESC;
```

### Get Invoices by Category

```sql
SELECT 
    i.invoice_number,
    i.vendor_name,
    i.total_amount,
    c.name as category
FROM invoices i
LEFT JOIN categories c ON i.category_id = c.id
WHERE i.user_id = 'YOUR_USER_ID'
  AND c.name = 'Vendors'
ORDER BY i.invoice_date DESC;
```

---

## ⚙️ Indexing Strategy

```sql
-- Already Created Indexes:
CREATE INDEX idx_invoices_user_id ON invoices(user_id);
CREATE INDEX idx_invoices_payment_status ON invoices(payment_status);
CREATE INDEX idx_invoices_invoice_date ON invoices(invoice_date);
CREATE INDEX idx_invoices_vendor_name ON invoices(vendor_name);
CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_categories_user_id ON categories(user_id);

-- For Search (Full-text search):
CREATE INDEX idx_invoices_vendor_gin ON invoices USING GIN(to_tsvector('english', vendor_name));
```

---

## 📝 Summary

- **4 Main Tables:** Users, Documents, Invoices, Categories
- **120+ Columns:** In invoices table alone
- **50+ Extractable Fields:** From invoices
- **Flexible Schema:** Optional fields for any invoice type
- **Secure:** RLS policies protect user data
- **Performant:** Strategic indexing on common queries
- **Extensible:** Easy to add new fields as needed

This schema supports invoices from any country/industry and can handle complex business scenarios! ✨
