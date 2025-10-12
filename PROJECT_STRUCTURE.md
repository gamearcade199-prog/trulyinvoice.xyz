# TrulyInvoice - Complete Project Structure

```
trulyinvoice.in/
│
├── 📄 README.md                      # Main project documentation
├── 📄 SETUP.md                       # Detailed setup instructions  
├── 📄 QUICKSTART.md                  # Quick 10-minute setup guide
├── 📄 PROJECT_STATUS.md              # Current implementation status
├── 📄 .gitignore                     # Git ignore rules
│
├── 📁 backend/                       # FastAPI Backend Application
│   │
│   ├── 📄 requirements.txt           # Python dependencies
│   ├── 📄 .env.example               # Environment variables template
│   │
│   └── 📁 app/                       # Main application package
│       │
│       ├── 📄 __init__.py
│       ├── 📄 main.py                # FastAPI app entry point
│       │
│       ├── 📁 core/                  # Core configuration & utilities
│       │   ├── 📄 __init__.py
│       │   ├── 📄 config.py          # Settings & environment variables
│       │   ├── 📄 database.py        # Database connection & session
│       │   └── 📄 security.py        # JWT auth & password hashing
│       │
│       ├── 📁 models/                # Data models & schemas
│       │   ├── 📄 __init__.py
│       │   ├── 📄 models.py          # SQLAlchemy database models
│       │   └── 📄 schemas.py         # Pydantic validation schemas
│       │
│       ├── 📁 api/                   # API route handlers
│       │   ├── 📄 __init__.py
│       │   ├── 📄 auth.py            # Authentication endpoints
│       │   ├── 📄 documents.py       # Document upload & management
│       │   ├── 📄 invoices.py        # Invoice CRUD operations
│       │   ├── 📄 categories.py      # Category management
│       │   └── 📄 subscriptions.py   # Subscription & usage APIs
│       │
│       └── 📁 services/              # Business logic layer
│           ├── 📄 __init__.py
│           ├── 📄 ai_service.py      # AI extraction pipeline
│           └── 📄 subscription_service.py  # Subscription limits
│
└── 📁 frontend/                      # Next.js Frontend Application
    │
    ├── 📄 package.json               # Node dependencies
    ├── 📄 .env.example               # Frontend environment variables
    ├── 📄 next.config.js             # Next.js configuration
    ├── 📄 tsconfig.json              # TypeScript configuration
    ├── 📄 tailwind.config.js         # Tailwind CSS configuration
    ├── 📄 postcss.config.js          # PostCSS configuration
    │
    └── 📁 src/                       # Source code
        │
        └── 📁 app/                   # Next.js 14 App Router
            ├── 📄 layout.tsx         # Root layout
            ├── 📄 page.tsx           # Landing page
            └── 📄 globals.css        # Global styles


PLANNED (To be added):

frontend/src/
├── 📁 app/
│   ├── 📁 (auth)/                   # Authentication pages
│   │   ├── login/
│   │   │   └── page.tsx             # Login page
│   │   └── register/
│   │       └── page.tsx             # Registration page
│   │
│   └── 📁 (dashboard)/              # Protected dashboard
│       ├── layout.tsx               # Dashboard layout
│       ├── page.tsx                 # Main dashboard
│       └── invoices/
│           └── [id]/
│               └── page.tsx         # Invoice detail page
│
├── 📁 components/                   # React components
│   ├── ui/                          # Base UI components
│   ├── forms/                       # Form components
│   ├── upload/                      # Upload components
│   └── invoice/                     # Invoice-specific components
│
└── 📁 lib/                          # Utilities
    ├── api.ts                       # API client
    ├── auth.ts                      # Auth helpers
    └── utils.ts                     # Utility functions
```

---

## 📊 File Count Summary

### ✅ Created Files (30+)

**Backend** (15 files):
- Core configuration: 3
- Database models: 2
- API routes: 5
- Services: 2
- Config files: 3

**Frontend** (10 files):
- Pages: 2
- Configuration: 5
- Styles: 1
- Package config: 2

**Documentation** (4 files):
- README.md
- SETUP.md
- QUICKSTART.md
- PROJECT_STATUS.md

**Root** (1 file):
- .gitignore

---

## 🎯 Key Files Explained

### Backend

**`app/main.py`**
- FastAPI application entry point
- CORS middleware
- Router registration
- Health check endpoints

**`app/core/config.py`**
- Environment variable management
- Subscription tier limits
- AI model configuration
- Security settings

**`app/models/models.py`**
- SQLAlchemy database models
- User, Subscription, Document, Invoice, Category tables
- Relationships and constraints

**`app/services/ai_service.py`**
- Google Cloud Vision OCR
- Anthropic Claude extraction
- Automatic fallback logic
- Confidence scoring

**`app/api/documents.py`**
- Document upload endpoint
- File validation
- AI processing pipeline
- Usage limit enforcement

### Frontend

**`src/app/page.tsx`**
- Landing page component
- Hero section
- Pricing table
- Feature showcase

**`tailwind.config.js`**
- Custom color scheme
- Blue accent color (#3B82F6)
- Responsive breakpoints

**`next.config.js`**
- API proxy configuration
- Image optimization
- Production settings

---

## 🔌 API Endpoints

### Authentication
```
POST   /api/auth/register      # Create new account
POST   /api/auth/login         # Login and get token
GET    /api/auth/me            # Get current user
PUT    /api/auth/me            # Update user profile
```

### Documents
```
POST   /api/documents/upload   # Upload invoice
GET    /api/documents/         # List all documents
GET    /api/documents/{id}     # Get specific document
DELETE /api/documents/{id}     # Delete document
```

### Invoices
```
GET    /api/invoices/          # List invoices (with filters)
GET    /api/invoices/{id}      # Get invoice details
PUT    /api/invoices/{id}      # Update invoice
GET    /api/invoices/stats/summary  # Get statistics
```

### Categories
```
GET    /api/categories/        # List all categories
POST   /api/categories/        # Create category
GET    /api/categories/{id}    # Get category
PUT    /api/categories/{id}    # Update category
DELETE /api/categories/{id}    # Delete category
```

### Subscriptions
```
GET    /api/subscriptions/current  # Get subscription
GET    /api/subscriptions/usage    # Get usage limits
POST   /api/subscriptions/upgrade  # Upgrade plan
```

---

## 🗄️ Database Schema

### Users Table
```sql
- id: INTEGER (PK)
- email: VARCHAR(255) UNIQUE
- hashed_password: VARCHAR(255)
- full_name: VARCHAR(255)
- phone: VARCHAR(20)
- is_active: BOOLEAN
- is_verified: BOOLEAN
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

### Subscriptions Table
```sql
- id: INTEGER (PK)
- user_id: INTEGER (FK)
- tier: ENUM (starter/pro/business)
- status: VARCHAR(50)
- scans_used_this_period: INTEGER
- razorpay_subscription_id: VARCHAR(255)
- current_period_start: TIMESTAMP
- current_period_end: TIMESTAMP
- created_at: TIMESTAMP
```

### Documents Table
```sql
- id: INTEGER (PK)
- user_id: INTEGER (FK)
- filename: VARCHAR(255)
- file_type: VARCHAR(50)
- file_size: INTEGER
- file_url: VARCHAR(500)
- status: VARCHAR(50)
- confidence_score: FLOAT
- used_fallback_model: BOOLEAN
- uploaded_at: TIMESTAMP
- processed_at: TIMESTAMP
```

### Invoices Table
```sql
- id: INTEGER (PK)
- user_id: INTEGER (FK)
- document_id: INTEGER (FK)
- category_id: INTEGER (FK)
- vendor_name: VARCHAR(255)
- invoice_number: VARCHAR(255)
- invoice_date: TIMESTAMP
- subtotal: FLOAT
- gst_amount: FLOAT
- cgst/sgst/igst: FLOAT
- total_amount: FLOAT
- line_items: JSON
- raw_extracted_data: JSON
- created_at: TIMESTAMP
```

---

## 🔐 Environment Variables

### Backend (.env)
```
DATABASE_URL                    # PostgreSQL connection
SECRET_KEY                      # JWT secret
GOOGLE_CLOUD_VISION_API_KEY    # OCR API
ANTHROPIC_API_KEY              # AI extraction
SUPABASE_URL                   # File storage
SUPABASE_KEY                   # Storage key
RAZORPAY_KEY_ID                # Payments
RAZORPAY_KEY_SECRET            # Payments
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL            # Backend URL
NEXT_PUBLIC_RAZORPAY_KEY       # Razorpay public key
```

---

## 📦 Dependencies

### Backend (Python)
- **Framework**: FastAPI, Uvicorn
- **Database**: SQLAlchemy, PostgreSQL
- **Auth**: python-jose, passlib
- **AI**: anthropic, google-cloud-vision
- **Storage**: supabase
- **Payments**: razorpay
- **Utils**: pydantic, python-dotenv

### Frontend (Node.js)
- **Framework**: Next.js 14, React 18
- **Styling**: Tailwind CSS
- **State**: React Query
- **HTTP**: Axios
- **Forms**: react-hook-form, zod
- **UI**: lucide-react, sonner

---

## 🚀 Deployment Structure (Future)

```
Production:
├── Backend → Railway/Render
│   └── PostgreSQL → Supabase
├── Frontend → Vercel
└── Storage → Supabase Storage
```

---

**Last Updated**: October 2025  
**Status**: Phase 1 Foundation Complete ✅
