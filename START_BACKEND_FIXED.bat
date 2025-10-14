@echo off
echo Starting TrulyInvoice Backend...
cd /d "C:\Users\akib\Desktop\trulyinvoice.in\backend"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
pause
