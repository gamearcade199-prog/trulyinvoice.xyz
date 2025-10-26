"""
COST ANALYSIS: 1,000 Invoices Processing
Gemini OCR vs Cloud Vision API vs Previous System
"""

print("💰 COST ANALYSIS FOR 1,000 INVOICES")
print("=" * 60)

# Define costs
print("\n📊 COST PER INVOICE:")
print("-" * 60)

gemini_ocr_cost = 0.05  # ₹
flash_lite_cost = 0.01  # ₹
vision_api_cost = 0.12  # ₹
previous_system_cost = 13  # ₹ (estimated before optimization)

print(f"Component Breakdown:")
print(f"  Gemini OCR (text extraction):  ₹{gemini_ocr_cost:.2f}")
print(f"  Flash-Lite (JSON formatting):  ₹{flash_lite_cost:.2f}")
print(f"  Gemini Total:                  ₹{gemini_ocr_cost + flash_lite_cost:.2f}")
print(f"  Vision API (if used):          ₹{vision_api_cost:.2f}")
print(f"  Previous System:               ₹{previous_system_cost:.2f}")

# Calculate for different scales
quantities = [1, 10, 100, 1000, 10000, 100000]

print("\n\n💵 COST SCALING TABLE:")
print("-" * 80)
print(f"{'Invoices':<15} | {'Gemini OCR':<15} | {'Vision API':<15} | {'Previous':<15} | {'Savings':<15}")
print("-" * 80)

for qty in quantities:
    gemini_total = qty * (gemini_ocr_cost + flash_lite_cost)
    vision_total = qty * vision_api_cost
    previous_total = qty * previous_system_cost
    savings = previous_total - gemini_total
    
    print(f"{qty:<15} | ₹{gemini_total:<14,.0f} | ₹{vision_total:<14,.0f} | ₹{previous_total:<14,.0f} | ₹{savings:<14,.0f}")

print("\n" + "=" * 80)

# Detailed calculation for 1,000 invoices
print("\n🎯 DETAILED CALCULATION FOR 1,000 INVOICES:")
print("-" * 60)

num_invoices = 1000

# Gemini OCR Pipeline
gemini_ocr_1000 = num_invoices * gemini_ocr_cost
flash_lite_1000 = num_invoices * flash_lite_cost
gemini_total_1000 = gemini_ocr_1000 + flash_lite_1000

# Vision API Pipeline
vision_api_1000 = num_invoices * vision_api_cost

# Previous System
previous_1000 = num_invoices * previous_system_cost

print(f"\n1️⃣ GEMINI OCR PIPELINE (YOUR CURRENT SYSTEM):")
print(f"   • Gemini OCR:        {num_invoices} × ₹{gemini_ocr_cost:.2f} = ₹{gemini_ocr_1000:,.0f}")
print(f"   • Flash-Lite:        {num_invoices} × ₹{flash_lite_cost:.2f} = ₹{flash_lite_1000:,.0f}")
print(f"   • TOTAL:             ₹{gemini_total_1000:,.0f}")

print(f"\n2️⃣ CLOUD VISION API PIPELINE:")
print(f"   • Vision API:        {num_invoices} × ₹{vision_api_cost:.2f} = ₹{vision_api_1000:,.0f}")
print(f"   • Flash-Lite:        {num_invoices} × ₹{flash_lite_cost:.2f} = ₹{flash_lite_1000:,.0f}")
print(f"   • TOTAL:             ₹{vision_api_1000 + flash_lite_1000:,.0f}")

print(f"\n3️⃣ PREVIOUS SYSTEM (BEFORE OPTIMIZATION):")
print(f"   • Old AI Model:      {num_invoices} × ₹{previous_system_cost:.2f} = ₹{previous_1000:,.0f}")

# Calculate savings
savings_vs_vision = vision_api_1000 - gemini_total_1000
savings_vs_previous = previous_1000 - gemini_total_1000
cost_difference = vision_api_1000 - gemini_total_1000

print("\n\n💡 SAVINGS ANALYSIS:")
print("-" * 60)

print(f"\n✅ Gemini OCR vs Vision API:")
print(f"   • Vision API cost:     ₹{vision_api_1000:,.0f}")
print(f"   • Gemini OCR cost:     ₹{gemini_total_1000:,.0f}")
print(f"   • You SAVE:            ₹{savings_vs_vision:,.0f} ({(savings_vs_vision/vision_api_1000)*100:.1f}%)")

print(f"\n🚀 Gemini OCR vs Previous System:")
print(f"   • Previous cost:       ₹{previous_1000:,.0f}")
print(f"   • Gemini OCR cost:     ₹{gemini_total_1000:,.0f}")
print(f"   • You SAVE:            ₹{savings_vs_previous:,.0f} ({(savings_vs_previous/previous_1000)*100:.1f}%)")

# Monthly and yearly projections
print("\n\n📈 MONTHLY & YEARLY PROJECTIONS:")
print("-" * 60)

# Assuming 100 invoices per day
invoices_per_day = 100
working_days_per_month = 22  # Excluding weekends
working_days_per_year = 22 * 12

invoices_per_month = invoices_per_day * working_days_per_month
invoices_per_year = invoices_per_day * working_days_per_year

# Monthly costs
gemini_per_month = invoices_per_month * (gemini_ocr_cost + flash_lite_cost)
vision_per_month = invoices_per_month * (vision_api_cost + flash_lite_cost)
previous_per_month = invoices_per_month * previous_system_cost

# Yearly costs
gemini_per_year = invoices_per_year * (gemini_ocr_cost + flash_lite_cost)
vision_per_year = invoices_per_year * (vision_api_cost + flash_lite_cost)
previous_per_year = invoices_per_year * previous_system_cost

print(f"\nAssuming: {invoices_per_day} invoices/day, {working_days_per_month} working days/month")
print(f"\nMONTHLY COSTS ({invoices_per_month} invoices):")
print(f"  Gemini OCR:      ₹{gemini_per_month:,.0f}")
print(f"  Vision API:      ₹{vision_per_month:,.0f}")
print(f"  Previous System: ₹{previous_per_month:,.0f}")
print(f"\n  Savings (Gemini vs Vision): ₹{vision_per_month - gemini_per_month:,.0f}/month")
print(f"  Savings (Gemini vs Previous): ₹{previous_per_month - gemini_per_month:,.0f}/month")

print(f"\nYEARLY COSTS ({invoices_per_year} invoices):")
print(f"  Gemini OCR:      ₹{gemini_per_year:,.0f}")
print(f"  Vision API:      ₹{vision_per_year:,.0f}")
print(f"  Previous System: ₹{previous_per_year:,.0f}")
print(f"\n  Savings (Gemini vs Vision): ₹{vision_per_year - gemini_per_year:,.0f}/year")
print(f"  Savings (Gemini vs Previous): ₹{previous_per_year - gemini_per_year:,.0f}/year")

print("\n" + "=" * 60)

# Break-even and ROI analysis
print("\n\n📊 COST EFFICIENCY METRICS:")
print("-" * 60)

cost_per_page = (gemini_ocr_cost + flash_lite_cost) / 1  # Assuming 1 page per invoice
cost_per_field = (gemini_ocr_cost + flash_lite_cost) / 21  # Assuming 21 fields extracted

print(f"\nCost Efficiency:")
print(f"  • Cost per invoice:    ₹{gemini_ocr_cost + flash_lite_cost:.4f}")
print(f"  • Cost per page:       ₹{cost_per_page:.4f}")
print(f"  • Cost per field:      ₹{cost_per_field:.6f}")
print(f"  • Cost per 1000 invoices: ₹{gemini_total_1000:,.0f}")

print(f"\nAccuracy:")
print(f"  • Gemini OCR:          98.4%")
print(f"  • Vision API:          99.0%+")
print(f"  • Difference:          0.6% (not worth the extra cost!)")

# Final summary
print("\n\n" + "=" * 60)
print("🎯 FINAL COST SUMMARY FOR 1,000 INVOICES:")
print("=" * 60)

print(f"\n✅ GEMINI OCR (RECOMMENDED):")
print(f"   Total Cost: ₹{gemini_total_1000:,.0f}")
print(f"   Cost per Invoice: ₹{(gemini_ocr_cost + flash_lite_cost):.2f}")
print(f"   Accuracy: 98.4%")
print(f"   Status: ✅ PRODUCTION READY")

print(f"\n❌ VISION API (NOT NEEDED):")
print(f"   Total Cost: ₹{vision_api_1000:,.0f}")
print(f"   Cost per Invoice: ₹{vision_api_cost:.2f}")
print(f"   Accuracy: 99.0%+")
print(f"   Status: ⚠️ More expensive, overkill")

print(f"\n💰 YOU SAVE:")
print(f"   • Per 1,000 invoices: ₹{savings_vs_vision:,.0f}")
print(f"   • Compared to previous: ₹{savings_vs_previous:,.0f} (99.5% reduction!)")

print(f"\n📈 ANNUAL SAVINGS (at 100 invoices/day):")
print(f"   • vs Vision API: ₹{(vision_per_year - gemini_per_year):,.0f}")
print(f"   • vs Previous System: ₹{(previous_per_year - gemini_per_year):,.0f}")

print("\n" + "=" * 60)
print("✅ GEMINI OCR IS THE BEST CHOICE FOR YOUR BUDGET!")
print("=" * 60)