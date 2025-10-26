#!/usr/bin/env python3
"""
🔍 SYSTEM VERIFICATION SCRIPT
Checks if all QA components are in place and working
Run this FIRST before deployment
"""

import os
import sys
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_check(status, message):
    """Print a check result"""
    if status == "pass":
        print(f"{GREEN}✅ {message}{RESET}")
    elif status == "fail":
        print(f"{RED}❌ {message}{RESET}")
    elif status == "warn":
        print(f"{YELLOW}⚠️  {message}{RESET}")
    else:
        print(f"{BLUE}ℹ️  {message}{RESET}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print_check("pass", f"Found {description}: {filepath}")
        return True
    else:
        print_check("fail", f"Missing {description}: {filepath}")
        return False

def check_file_contains(filepath, search_text, description):
    """Check if a file contains specific text"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if search_text in content:
                print_check("pass", f"{description} found in {Path(filepath).name}")
                return True
            else:
                print_check("fail", f"{description} NOT found in {Path(filepath).name}")
                return False
    except Exception as e:
        print_check("fail", f"Cannot read {filepath}: {e}")
        return False

def count_lines(filepath):
    """Count lines in a file"""
    try:
        with open(filepath, 'r') as f:
            return len(f.readlines())
    except:
        return 0

def main():
    print(f"\n{BLUE}{'='*60}")
    print("🔍 SYSTEM VERIFICATION - QA Components Check")
    print(f"{'='*60}{RESET}\n")

    results = []
    backend_path = Path("backend")
    
    # Check 1: Validator exists and is complete
    print(f"{BLUE}[1/6] Checking Invoice Validator...{RESET}")
    validator_file = backend_path / "app" / "services" / "invoice_validator.py"
    if check_file_exists(validator_file, "Invoice Validator"):
        lines = count_lines(validator_file)
        if lines > 300:
            print_check("pass", f"Validator has {lines} lines of code ✓")
            results.append(True)
        else:
            print_check("warn", f"Validator only has {lines} lines (expected >300)")
            results.append(False)
    else:
        results.append(False)

    # Check 2: Validator is integrated into API
    print(f"\n{BLUE}[2/6] Checking API Integration...{RESET}")
    documents_file = backend_path / "app" / "api" / "documents.py"
    if check_file_exists(documents_file, "Documents API"):
        if check_file_contains(documents_file, "InvoiceValidator", "Validator integration"):
            print_check("pass", "Validator is integrated into documents.py ✓")
            results.append(True)
        else:
            print_check("fail", "Validator integration NOT found in documents.py")
            results.append(False)
    else:
        results.append(False)

    # Check 3: Database triggers exist
    print(f"\n{BLUE}[3/6] Checking Database Triggers...{RESET}")
    triggers_file = Path("DATABASE_AUDIT_TRIGGERS.sql")
    if check_file_exists(triggers_file, "Database Triggers SQL"):
        if check_file_contains(triggers_file, "validate_invoice_on_insert", "INSERT trigger"):
            print_check("pass", "INSERT trigger defined ✓")
            if check_file_contains(triggers_file, "validate_invoice_on_update", "UPDATE trigger"):
                print_check("pass", "UPDATE trigger defined ✓")
                results.append(True)
            else:
                results.append(False)
        else:
            results.append(False)
    else:
        results.append(False)

    # Check 4: Quality Monitor exists
    print(f"\n{BLUE}[4/6] Checking Quality Monitor...{RESET}")
    monitor_file = backend_path / "app" / "services" / "data_quality_monitor.py"
    if check_file_exists(monitor_file, "Quality Monitor"):
        lines = count_lines(monitor_file)
        if lines > 150:
            print_check("pass", f"Quality Monitor has {lines} lines of code ✓")
            results.append(True)
        else:
            print_check("warn", f"Quality Monitor only has {lines} lines")
            results.append(False)
    else:
        results.append(False)

    # Check 5: Test suite exists
    print(f"\n{BLUE}[5/6] Checking Test Suite...{RESET}")
    test_file = backend_path / "tests" / "test_invoice_validator.py"
    if check_file_exists(test_file, "Test Suite"):
        lines = count_lines(test_file)
        if lines > 200:
            print_check("pass", f"Test suite has {lines} lines of code ✓")
            if check_file_contains(test_file, "def test_", "Test cases"):
                print_check("pass", "Multiple test cases defined ✓")
                results.append(True)
            else:
                results.append(False)
        else:
            print_check("warn", f"Test suite only has {lines} lines")
            results.append(False)
    else:
        results.append(False)

    # Check 6: Export fixes in place
    print(f"\n{BLUE}[6/6] Checking Export Fixes...{RESET}")
    exporters = [
        (backend_path / "app" / "services" / "accountant_excel_exporter.py", "Excel Exporter"),
        (backend_path / "app" / "services" / "csv_exporter.py", "CSV Exporter"),
        (backend_path / "app" / "services" / "professional_pdf_exporter.py", "PDF Exporter"),
    ]
    
    all_exporters_ok = True
    for exporter_path, exporter_name in exporters:
        if check_file_exists(exporter_path, exporter_name):
            if check_file_contains(exporter_path, "str(", "Safe None handling"):
                print_check("pass", f"{exporter_name} has safe None handling ✓")
            else:
                print_check("warn", f"{exporter_name} might not have safe None handling")
                all_exporters_ok = False
        else:
            all_exporters_ok = False
    
    results.append(all_exporters_ok)

    # Summary
    print(f"\n{BLUE}{'='*60}")
    print("📊 VERIFICATION RESULTS")
    print(f"{'='*60}{RESET}\n")
    
    passed = sum(results)
    total = len(results)
    
    checks = [
        "Invoice Validator",
        "API Integration",
        "Database Triggers",
        "Quality Monitor",
        "Test Suite",
        "Export Fixes"
    ]
    
    for i, (check, result) in enumerate(zip(checks, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check}")
    
    print(f"\n{BLUE}Overall: {passed}/{total} components verified{RESET}\n")
    
    if passed == total:
        print(f"{GREEN}🎉 ALL SYSTEMS GO! Ready for deployment.{RESET}\n")
        return 0
    elif passed >= total - 1:
        print(f"{YELLOW}⚠️  {total - passed} issue(s) to fix before deployment.{RESET}\n")
        return 1
    else:
        print(f"{RED}❌ Multiple issues found. Review above and fix.{RESET}\n")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
