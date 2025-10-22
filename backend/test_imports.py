#!/usr/bin/env python3
"""
Test all export functionality
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print('Testing imports step by step...')

try:
    print('1. Testing FastAPI...')
    from fastapi import FastAPI
    print('   ✅ FastAPI ok')

    print('2. Testing dotenv...')
    from dotenv import load_dotenv
    print('   ✅ dotenv ok')

    print('3. Testing main app creation...')
    from app.main import app
    print('   ✅ Main app created')
    print(f'   App title: {app.title}')

    print('4. Testing health endpoint...')
    from app.api.health import router as health_router
    print('   ✅ Health router ok')

    print('5. Testing documents router...')
    from app.api.documents import router as documents_router
    print('   ✅ Documents router ok')

    print('6. Testing invoices router...')
    from app.api.invoices import router as invoices_router
    print('   ✅ Invoices router ok')

    print('7. Testing exports router...')
    from app.api.exports import router as exports_router
    print('   ✅ Exports router ok')

    print('8. Testing payments router...')
    from app.api.payments import router as payments_router
    print('   ✅ Payments router ok')

    print('9. Testing auth router...')
    from app.api.auth import router as auth_router
    print('   ✅ Auth router ok')

    print('\n🎉 All imports successful!')

except Exception as e:
    print(f'❌ Error at step: {e}')
    import traceback
    traceback.print_exc()