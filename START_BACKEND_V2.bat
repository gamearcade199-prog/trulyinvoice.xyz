@echo off
echo ========================================
echo  STARTING TRULYINVOICE BACKEND v2.0
echo  Clean Architecture - Zero Conflicts
echo ========================================
cd /d "c:\Users\akib\Desktop\trulyinvoice.in\backend"
set PYTHONPATH=c:\Users\akib\Desktop\trulyinvoice.in\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
