# TrulyInvoice - AI-Powered Invoice Management Platform

## 🚀 Project Overview

TrulyInvoice is an AI-powered automation tool designed to eliminate manual data entry for Indian freelancers, small businesses, and e-commerce sellers. The platform processes, organizes, and analyzes invoices, receipts, and bills with a focus on speed, accuracy, and GST compliance.

**Target Market**: Indian Freelancers, Small Businesses, E-commerce Sellers  
**Project Start**: October 2025  
**MVP Launch Target**: Q1 2026

## 🏗️ Architecture

### Tech Stack

**Frontend**:
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Shadcn/ui components
- React Query for state management

**Backend**:
- FastAPI (Python 3.11+)
- PostgreSQL (via Supabase)
- SQLAlchemy ORM
- Pydantic for data validation

**AI & OCR**:
- Google Cloud Vision API (OCR)
- Anthropic Claude 3 Haiku (Primary extraction)
- Anthropic Claude 3 Sonnet (Fallback for low confidence)

**Storage & Services**:
- Supabase (Database + Storage)
- Razorpay (Payment Gateway)
- AWS S3 (Alternative storage option)

## 📁 Project Structure

```
trulyinvoice.in/
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/             # App router pages
│   │   ├── components/      # React components
│   │   ├── lib/             # Utilities and helpers
│   │   └── types/           # TypeScript definitions
│   └── public/              # Static assets
│
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/             # API routes
│   │   ├── core/            # Config, security, database
│   │   ├── models/          # Database models
│   │   ├── services/        # Business logic
│   │   └── main.py          # FastAPI app entry
│   ├── alembic/             # Database migrations
│   └── requirements.txt     # Python dependencies
│
└── docs/                    # Documentation
```

## 💰 Subscription Plans

| Feature | Starter (Free) | Pro | Business |
|---------|---------------|-----|----------|
| **Price** | ₹0 | ₹99/month | ₹399/month |
| **Scans/Month** | 30 | 200 | 750 |
| **Excel/CSV Export** | ✅ | ✅ | ✅ |
| **Google Sheets Sync** | ❌ | ✅ | ✅ |
| **Tally/QuickBooks** | ❌ | ❌ | ✅ |
| **Multi-user** | 1 user | 1 user | 3 users |
| **Data History** | 60 days | 1 year | Unlimited |

## 🚦 MVP Development Phases

### Phase 1: Core Functionality & Free Tier ✅
- Document upload (PDF, Images, Screenshots)
- AI extraction pipeline with fallback logic
- Dashboard with search/filter
- Excel export
- Starter (Free) plan limits

### Phase 2: Monetization & Pro Tier
- Payment gateway integration (Razorpay)
- Pro subscription plan
- Automatic categorization
- Google Sheets sync

### Phase 3: Business Tier & Integrations
- Business plan implementation
- Tally/QuickBooks export
- Multi-user account management

### Phase 4: Advanced Features
- Reporting and analytics
- Alerts and notifications
- Advanced automation

## 🛠️ Setup Instructions

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- PostgreSQL (or Supabase account)
- Google Cloud account (for Vision API)
- Anthropic API key
- Razorpay account

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Configure environment variables
npm run dev
```

The frontend will run on `http://localhost:3000`

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
# Configure environment variables
uvicorn app.main:app --reload
```

The backend will run on `http://localhost:8000`

### Environment Variables

#### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_RAZORPAY_KEY=your_razorpay_key
```

#### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost/trulyinvoice
SECRET_KEY=your-secret-key-here
GOOGLE_CLOUD_VISION_API_KEY=your_google_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## 🧪 Testing

```bash
# Frontend tests
cd frontend
npm test

# Backend tests
cd backend
pytest
```

## 📦 Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel deploy
```

### Backend (Railway/Render)
```bash
cd backend
# Follow platform-specific deployment instructions
```

## 🔐 Security

- JWT-based authentication
- Row-level security in Supabase
- API rate limiting
- Encrypted file storage
- PCI DSS compliant payment handling

## 📊 Database Schema

Key tables:
- `users` - User accounts and authentication
- `subscriptions` - Subscription plans and billing
- `invoices` - Processed invoice data
- `documents` - Original uploaded files
- `categories` - Expense categories
- `usage_logs` - Track API usage per user

## 🤝 Contributing

This is a commercial project. For internal development only.

## 📄 License

Proprietary - All rights reserved

## 📞 Support

For questions or issues, contact: support@trulyinvoice.in

---

**Built with ❤️ for Indian businesses**
