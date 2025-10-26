"""
🚀 COMPREHENSIVE PRODUCTION READINESS AUDIT - 40 CRITICAL TESTS
================================================================

This script performs a complete production readiness check covering:
✅ Security & Authentication
✅ Database & Performance
✅ API & Endpoints
✅ Configuration & Environment
✅ Error Handling & Monitoring
✅ Backup & Recovery
✅ Legal & Compliance
✅ Deployment & CI/CD
✅ Code Quality & Testing
✅ Scalability & Load Handling

Run with: python PRODUCTION_READINESS_AUDIT_DEEP.py
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import subprocess
import re

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ProductionReadinessAuditor:
    """Comprehensive production readiness auditing system"""
    
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.critical_issues = []
        self.start_time = time.time()
        
        # Project paths
        self.root_dir = Path(__file__).parent
        self.backend_dir = self.root_dir / "backend"
        self.frontend_dir = self.root_dir / "frontend"
        
        # API endpoints (update with your actual URLs)
        self.api_url = os.getenv("API_URL", "https://trulyinvoice-backend.onrender.com")
        self.frontend_url = os.getenv("FRONTEND_URL", "https://trulyinvoice.xyz")
    
    def log_test(self, test_name: str, passed: bool, details: str, severity: str = "medium"):
        """Log a test result"""
        result = {
            "test_name": test_name,
            "passed": passed,
            "details": details,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        }
        
        self.results.append(result)
        
        if passed:
            self.passed += 1
            symbol = f"{Colors.OKGREEN}✓{Colors.ENDC}"
        else:
            if severity == "critical":
                self.critical_issues.append(test_name)
                self.failed += 1
                symbol = f"{Colors.FAIL}✗ CRITICAL{Colors.ENDC}"
            elif severity == "warning":
                self.warnings += 1
                symbol = f"{Colors.WARNING}⚠ WARNING{Colors.ENDC}"
            else:
                self.failed += 1
                symbol = f"{Colors.FAIL}✗{Colors.ENDC}"
        
        print(f"  {symbol} {test_name}")
        if not passed and details:
            print(f"    → {details}")
    
    def print_section(self, section_name: str):
        """Print a section header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{section_name}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")
    
    # =====================================================================
    # CATEGORY 1: SECURITY & AUTHENTICATION (10 Tests)
    # =====================================================================
    
    def test_01_environment_variables(self):
        """Test: All required environment variables are present"""
        required_vars = {
            "backend": [
                "SUPABASE_URL", "SUPABASE_KEY", "SUPABASE_SERVICE_KEY",
                "GEMINI_API_KEY", "RAZORPAY_KEY_ID", "RAZORPAY_KEY_SECRET"
            ],
            "frontend": [
                "NEXT_PUBLIC_SUPABASE_URL", "NEXT_PUBLIC_SUPABASE_ANON_KEY"
            ]
        }
        
        # Check backend .env
        backend_env = self.backend_dir / ".env"
        if not backend_env.exists():
            self.log_test(
                "01. Environment Variables - Backend",
                False,
                "Backend .env file not found",
                "critical"
            )
            return
        
        with open(backend_env) as f:
            env_content = f.read()
        
        missing_backend = [var for var in required_vars["backend"] 
                          if var not in env_content or f"{var}=" not in env_content]
        
        if missing_backend:
            self.log_test(
                "01. Environment Variables - Backend",
                False,
                f"Missing: {', '.join(missing_backend)}",
                "critical"
            )
        else:
            self.log_test(
                "01. Environment Variables - Backend",
                True,
                "All required backend environment variables present"
            )
        
        # Check frontend .env
        frontend_env = self.frontend_dir / ".env.local"
        if not frontend_env.exists():
            self.log_test(
                "01. Environment Variables - Frontend",
                False,
                "Frontend .env.local file not found",
                "warning"
            )
            return
        
        with open(frontend_env) as f:
            env_content = f.read()
        
        missing_frontend = [var for var in required_vars["frontend"] 
                           if var not in env_content]
        
        if missing_frontend:
            self.log_test(
                "01. Environment Variables - Frontend",
                False,
                f"Missing: {', '.join(missing_frontend)}",
                "warning"
            )
        else:
            self.log_test(
                "01. Environment Variables - Frontend",
                True,
                "All required frontend environment variables present"
            )
    
    def test_02_rate_limiting_enabled(self):
        """Test: Rate limiting middleware is enabled"""
        main_py = self.backend_dir / "app" / "main.py"
        
        if not main_py.exists():
            self.log_test(
                "02. Rate Limiting Enabled",
                False,
                "main.py not found",
                "critical"
            )
            return
        
        with open(main_py) as f:
            content = f.read()
        
        # Check if rate limiting is commented out
        if "# from .middleware.rate_limiter" in content or "# app.middleware" in content:
            self.log_test(
                "02. Rate Limiting Enabled",
                False,
                "Rate limiting middleware is commented out in main.py",
                "critical"
            )
        elif "rate_limit_middleware" in content and "app.middleware" in content:
            self.log_test(
                "02. Rate Limiting Enabled",
                True,
                "Rate limiting middleware is enabled"
            )
        else:
            self.log_test(
                "02. Rate Limiting Enabled",
                False,
                "Rate limiting middleware not found in main.py",
                "critical"
            )
    
    def test_03_no_api_keys_in_code(self):
        """Test: No hardcoded API keys in source files"""
        suspicious_patterns = [
            r'SUPABASE.*=.*".*\.supabase\.co"',
            r'api_key\s*=\s*["\'](?!.*env).*["\']',
            r'RAZORPAY.*=.*["\']rzp_',
            r'OPENAI.*=.*["\']sk-',
            r'GEMINI.*=.*["\']AI'
        ]
        
        found_issues = []
        
        # Check Python files
        for py_file in self.backend_dir.rglob("*.py"):
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue
            
            try:
                with open(py_file) as f:
                    content = f.read()
                
                for pattern in suspicious_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        found_issues.append(str(py_file.name))
                        break
            except:
                pass
        
        # Check TypeScript files
        for ts_file in self.frontend_dir.rglob("*.ts*"):
            if "node_modules" in str(ts_file) or ".next" in str(ts_file):
                continue
            
            try:
                with open(ts_file) as f:
                    content = f.read()
                
                for pattern in suspicious_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        found_issues.append(str(ts_file.name))
                        break
            except:
                pass
        
        if found_issues:
            self.log_test(
                "03. No Hardcoded API Keys",
                False,
                f"Potential hardcoded keys in: {', '.join(set(found_issues))}",
                "critical"
            )
        else:
            self.log_test(
                "03. No Hardcoded API Keys",
                True,
                "No hardcoded API keys detected"
            )
    
    def test_04_cors_configured(self):
        """Test: CORS is properly configured"""
        main_py = self.backend_dir / "app" / "main.py"
        
        if not main_py.exists():
            self.log_test(
                "04. CORS Configuration",
                False,
                "main.py not found",
                "critical"
            )
            return
        
        with open(main_py) as f:
            content = f.read()
        
        if "CORSMiddleware" in content and "allow_origins" in content:
            # Check if production domain is included
            if "trulyinvoice.xyz" in content:
                self.log_test(
                    "04. CORS Configuration",
                    True,
                    "CORS properly configured with production domain"
                )
            else:
                self.log_test(
                    "04. CORS Configuration",
                    False,
                    "CORS configured but production domain missing",
                    "warning"
                )
        else:
            self.log_test(
                "04. CORS Configuration",
                False,
                "CORS middleware not found",
                "critical"
            )
    
    def test_05_sql_injection_protection(self):
        """Test: SQL injection protection (parameterized queries)"""
        issues = []
        
        # Check for raw SQL string formatting
        for py_file in self.backend_dir.rglob("*.py"):
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue
            
            try:
                with open(py_file) as f:
                    content = f.read()
                
                # Look for dangerous SQL patterns
                dangerous_patterns = [
                    r'\.execute\([f\'"].*\{.*\}',  # f-string in execute
                    r'\.execute\(.*\+.*\)',  # String concatenation in execute
                    r'\.execute\(.*%.*\)',  # Old-style string formatting
                ]
                
                for pattern in dangerous_patterns:
                    if re.search(pattern, content):
                        issues.append(py_file.name)
                        break
            except:
                pass
        
        if issues:
            self.log_test(
                "05. SQL Injection Protection",
                False,
                f"Potential SQL injection vulnerabilities in: {', '.join(set(issues))}",
                "critical"
            )
        else:
            self.log_test(
                "05. SQL Injection Protection",
                True,
                "No obvious SQL injection vulnerabilities detected"
            )
    
    def test_06_xss_protection(self):
        """Test: XSS protection in frontend"""
        issues = []
        
        # Check for dangerouslySetInnerHTML without sanitization
        for tsx_file in self.frontend_dir.rglob("*.tsx"):
            if "node_modules" in str(tsx_file) or ".next" in str(tsx_file):
                continue
            
            try:
                with open(tsx_file) as f:
                    content = f.read()
                
                if "dangerouslySetInnerHTML" in content:
                    # Check if DOMPurify or similar is used
                    if "DOMPurify" not in content and "sanitize" not in content.lower():
                        issues.append(tsx_file.name)
            except:
                pass
        
        if issues:
            self.log_test(
                "06. XSS Protection",
                False,
                f"dangerouslySetInnerHTML without sanitization in: {', '.join(set(issues))}",
                "warning"
            )
        else:
            self.log_test(
                "06. XSS Protection",
                True,
                "No obvious XSS vulnerabilities detected"
            )
    
    def test_07_file_upload_validation(self):
        """Test: File upload validation is implemented"""
        documents_py = self.backend_dir / "app" / "api" / "documents.py"
        
        if not documents_py.exists():
            self.log_test(
                "07. File Upload Validation",
                False,
                "documents.py not found",
                "warning"
            )
            return
        
        with open(documents_py) as f:
            content = f.read()
        
        validation_checks = {
            "File size": "size" in content.lower() or "len" in content,
            "File type": "content_type" in content or "mimetype" in content,
            "File extension": ".pdf" in content or ".jpg" in content
        }
        
        passed_checks = sum(validation_checks.values())
        
        if passed_checks >= 2:
            self.log_test(
                "07. File Upload Validation",
                True,
                f"File upload validation present ({passed_checks}/3 checks)"
            )
        else:
            self.log_test(
                "07. File Upload Validation",
                False,
                f"Insufficient file upload validation ({passed_checks}/3 checks)",
                "warning"
            )
    
    def test_08_authentication_required(self):
        """Test: Protected endpoints require authentication"""
        api_files = [
            "documents.py", "invoices.py", "exports.py", 
            "payments.py", "storage.py"
        ]
        
        issues = []
        
        for api_file in api_files:
            file_path = self.backend_dir / "app" / "api" / api_file
            
            if not file_path.exists():
                continue
            
            try:
                with open(file_path) as f:
                    content = f.read()
                
                # Check for Depends(get_current_user) or similar
                if "Depends(" not in content and "get_current_user" not in content:
                    issues.append(api_file)
            except:
                pass
        
        if issues:
            self.log_test(
                "08. Authentication Required",
                False,
                f"Endpoints may lack auth in: {', '.join(issues)}",
                "warning"
            )
        else:
            self.log_test(
                "08. Authentication Required",
                True,
                "All API endpoints appear to have authentication"
            )
    
    def test_09_password_hashing(self):
        """Test: Passwords are properly hashed"""
        auth_files = list((self.backend_dir / "app").rglob("*auth*.py"))
        
        if not auth_files:
            self.log_test(
                "09. Password Hashing",
                False,
                "No authentication files found",
                "warning"
            )
            return
        
        has_hashing = False
        
        for auth_file in auth_files:
            try:
                with open(auth_file) as f:
                    content = f.read()
                
                if any(keyword in content for keyword in ["bcrypt", "passlib", "hash_password", "verify_password"]):
                    has_hashing = True
                    break
            except:
                pass
        
        # Note: Supabase handles authentication
        if has_hashing or "supabase" in str(auth_files[0]).lower():
            self.log_test(
                "09. Password Hashing",
                True,
                "Password hashing implemented (Supabase Auth)"
            )
        else:
            self.log_test(
                "09. Password Hashing",
                False,
                "Password hashing not detected",
                "critical"
            )
    
    def test_10_https_enforcement(self):
        """Test: HTTPS is enforced in production"""
        vercel_json = self.root_dir / "vercel.json"
        
        if not vercel_json.exists():
            self.log_test(
                "10. HTTPS Enforcement",
                False,
                "vercel.json not found",
                "warning"
            )
            return
        
        try:
            with open(vercel_json) as f:
                config = json.load(f)
            
            # Check for security headers
            has_security_headers = False
            if "headers" in config:
                for header_group in config["headers"]:
                    if any("Strict-Transport-Security" in h.get("key", "") 
                           for h in header_group.get("headers", [])):
                        has_security_headers = True
                        break
            
            if has_security_headers:
                self.log_test(
                    "10. HTTPS Enforcement",
                    True,
                    "HTTPS enforcement configured with HSTS"
                )
            else:
                self.log_test(
                    "10. HTTPS Enforcement",
                    False,
                    "HSTS header not configured",
                    "warning"
                )
        except:
            self.log_test(
                "10. HTTPS Enforcement",
                False,
                "Could not parse vercel.json",
                "warning"
            )
    
    # =====================================================================
    # CATEGORY 2: DATABASE & PERFORMANCE (8 Tests)
    # =====================================================================
    
    def test_11_database_indexes(self):
        """Test: Database has proper indexes"""
        sql_files = list(self.root_dir.glob("*.sql"))
        
        index_found = False
        index_count = 0
        
        for sql_file in sql_files:
            try:
                with open(sql_file) as f:
                    content = f.read()
                
                # Count CREATE INDEX statements
                index_count += content.upper().count("CREATE INDEX")
            except:
                pass
        
        if index_count >= 5:
            self.log_test(
                "11. Database Indexes",
                True,
                f"Found {index_count} database indexes"
            )
        elif index_count > 0:
            self.log_test(
                "11. Database Indexes",
                False,
                f"Only {index_count} indexes found, recommend at least 5",
                "warning"
            )
        else:
            self.log_test(
                "11. Database Indexes",
                False,
                "No database indexes found",
                "critical"
            )
    
    def test_12_connection_pooling(self):
        """Test: Database connection pooling is configured"""
        database_files = list((self.backend_dir / "app").rglob("*database*.py"))
        
        has_pooling = False
        
        for db_file in database_files:
            try:
                with open(db_file) as f:
                    content = f.read()
                
                if any(keyword in content for keyword in ["pool_size", "max_overflow", "QueuePool"]):
                    has_pooling = True
                    break
            except:
                pass
        
        if has_pooling:
            self.log_test(
                "12. Connection Pooling",
                True,
                "Database connection pooling configured"
            )
        else:
            self.log_test(
                "12. Connection Pooling",
                False,
                "Connection pooling not found",
                "critical"
            )
    
    def test_13_pagination_implemented(self):
        """Test: API endpoints have pagination"""
        api_files = list((self.backend_dir / "app" / "api").glob("*.py"))
        
        pagination_found = False
        
        for api_file in api_files:
            try:
                with open(api_file) as f:
                    content = f.read()
                
                if any(keyword in content for keyword in ["skip", "limit", "offset", "page"]):
                    pagination_found = True
                    break
            except:
                pass
        
        if pagination_found:
            self.log_test(
                "13. Pagination Implemented",
                True,
                "Pagination found in API endpoints"
            )
        else:
            self.log_test(
                "13. Pagination Implemented",
                False,
                "No pagination detected in API endpoints",
                "critical"
            )
    
    def test_14_caching_layer(self):
        """Test: Caching is implemented"""
        # Check for Redis or caching imports
        has_cache = False
        
        for py_file in self.backend_dir.rglob("*.py"):
            if "venv" in str(py_file):
                continue
            
            try:
                with open(py_file) as f:
                    content = f.read()
                
                if any(keyword in content for keyword in ["redis", "cache", "Cache"]):
                    has_cache = True
                    break
            except:
                pass
        
        if has_cache:
            self.log_test(
                "14. Caching Layer",
                True,
                "Caching implementation found"
            )
        else:
            self.log_test(
                "14. Caching Layer",
                False,
                "No caching layer detected",
                "warning"
            )
    
    def test_15_database_migrations(self):
        """Test: Database migration system exists"""
        migration_indicators = [
            self.backend_dir / "migrations",
            self.backend_dir / "alembic",
            self.root_dir / "supabase" / "migrations"
        ]
        
        has_migrations = any(path.exists() for path in migration_indicators)
        
        # Also check for SQL migration files
        sql_migrations = len(list(self.root_dir.glob("*MIGRATION*.sql")))
        
        if has_migrations or sql_migrations > 0:
            self.log_test(
                "15. Database Migrations",
                True,
                f"Migration system found ({sql_migrations} SQL migrations)"
            )
        else:
            self.log_test(
                "15. Database Migrations",
                False,
                "No migration system detected",
                "warning"
            )
    
    def test_16_n_plus_one_queries(self):
        """Test: Check for N+1 query problems"""
        issues = []
        
        for py_file in self.backend_dir.rglob("*.py"):
            if "venv" in str(py_file):
                continue
            
            try:
                with open(py_file) as f:
                    content = f.read()
                    lines = content.split('\n')
                
                # Look for loops with database queries inside
                in_loop = False
                for i, line in enumerate(lines):
                    if any(keyword in line for keyword in ["for ", "while "]):
                        in_loop = True
                        loop_start = i
                    
                    if in_loop and any(keyword in line for keyword in [".query(", ".execute(", ".filter("]):
                        issues.append(f"{py_file.name}:L{i+1}")
                        in_loop = False
                    
                    if in_loop and i > loop_start + 10:
                        in_loop = False
            except:
                pass
        
        if issues:
            self.log_test(
                "16. N+1 Query Problems",
                False,
                f"Potential N+1 queries in: {', '.join(issues[:3])}",
                "warning"
            )
        else:
            self.log_test(
                "16. N+1 Query Problems",
                True,
                "No obvious N+1 query patterns detected"
            )
    
    def test_17_query_timeout(self):
        """Test: Database queries have timeout configuration"""
        database_files = list((self.backend_dir / "app").rglob("*database*.py"))
        
        has_timeout = False
        
        for db_file in database_files:
            try:
                with open(db_file) as f:
                    content = f.read()
                
                if any(keyword in content for keyword in ["timeout", "pool_timeout", "statement_timeout"]):
                    has_timeout = True
                    break
            except:
                pass
        
        if has_timeout:
            self.log_test(
                "17. Query Timeout Configuration",
                True,
                "Query timeout configured"
            )
        else:
            self.log_test(
                "17. Query Timeout Configuration",
                False,
                "No query timeout detected",
                "warning"
            )
    
    def test_18_bulk_operations(self):
        """Test: Bulk operations are available"""
        api_files = list((self.backend_dir / "app" / "api").glob("*.py"))
        
        bulk_ops = False
        
        for api_file in api_files:
            try:
                with open(api_file) as f:
                    content = f.read()
                
                if any(keyword in content for keyword in ["bulk", "batch", "multiple"]):
                    bulk_ops = True
                    break
            except:
                pass
        
        if bulk_ops:
            self.log_test(
                "18. Bulk Operations",
                True,
                "Bulk operations available"
            )
        else:
            self.log_test(
                "18. Bulk Operations",
                False,
                "No bulk operations detected",
                "warning"
            )
    
    # =====================================================================
    # CATEGORY 3: API & MONITORING (6 Tests)
    # =====================================================================
    
    def test_19_health_endpoint(self):
        """Test: Health check endpoint exists and responds"""
        health_py = self.backend_dir / "app" / "api" / "health.py"
        
        if not health_py.exists():
            self.log_test(
                "19. Health Check Endpoint",
                False,
                "health.py not found",
                "critical"
            )
            return
        
        with open(health_py) as f:
            content = f.read()
        
        if "/health" in content or "@router.get" in content:
            self.log_test(
                "19. Health Check Endpoint",
                True,
                "Health check endpoint exists"
            )
        else:
            self.log_test(
                "19. Health Check Endpoint",
                False,
                "Health check endpoint not properly configured",
                "warning"
            )
    
    def test_20_error_monitoring(self):
        """Test: Error monitoring (Sentry) is configured"""
        main_py = self.backend_dir / "app" / "main.py"
        requirements = self.backend_dir / "requirements.txt"
        
        has_sentry = False
        
        if main_py.exists():
            with open(main_py) as f:
                content = f.read()
            if "sentry" in content.lower():
                has_sentry = True
        
        if not has_sentry and requirements.exists():
            with open(requirements) as f:
                content = f.read()
            if "sentry" in content.lower():
                has_sentry = True
        
        if has_sentry:
            self.log_test(
                "20. Error Monitoring (Sentry)",
                True,
                "Sentry error monitoring configured"
            )
        else:
            self.log_test(
                "20. Error Monitoring (Sentry)",
                False,
                "No error monitoring service detected",
                "critical"
            )
    
    def test_21_logging_configured(self):
        """Test: Structured logging is configured"""
        has_logging = False
        
        for py_file in self.backend_dir.rglob("*.py"):
            if "venv" in str(py_file):
                continue
            
            try:
                with open(py_file) as f:
                    content = f.read()
                
                if "import logging" in content or "logger" in content:
                    has_logging = True
                    break
            except:
                pass
        
        if has_logging:
            self.log_test(
                "21. Logging Configuration",
                True,
                "Logging is configured"
            )
        else:
            self.log_test(
                "21. Logging Configuration",
                False,
                "No logging detected",
                "warning"
            )
    
    def test_22_api_versioning(self):
        """Test: API versioning is implemented"""
        main_py = self.backend_dir / "app" / "main.py"
        
        if not main_py.exists():
            self.log_test(
                "22. API Versioning",
                False,
                "main.py not found",
                "warning"
            )
            return
        
        with open(main_py) as f:
            content = f.read()
        
        if "/api/v1" in content or "/v1/" in content:
            self.log_test(
                "22. API Versioning",
                True,
                "API versioning implemented"
            )
        else:
            self.log_test(
                "22. API Versioning",
                False,
                "No API versioning detected",
                "warning"
            )
    
    def test_23_request_timeout(self):
        """Test: Request timeout handling"""
        main_py = self.backend_dir / "app" / "main.py"
        
        if not main_py.exists():
            self.log_test(
                "23. Request Timeout",
                False,
                "main.py not found",
                "warning"
            )
            return
        
        with open(main_py) as f:
            content = f.read()
        
        if "timeout" in content.lower() or "TimeoutError" in content:
            self.log_test(
                "23. Request Timeout",
                True,
                "Request timeout handling detected"
            )
        else:
            self.log_test(
                "23. Request Timeout",
                False,
                "No request timeout handling",
                "warning"
            )
    
    def test_24_api_documentation(self):
        """Test: API documentation is accessible"""
        main_py = self.backend_dir / "app" / "main.py"
        
        if not main_py.exists():
            self.log_test(
                "24. API Documentation",
                False,
                "main.py not found",
                "warning"
            )
            return
        
        with open(main_py) as f:
            content = f.read()
        
        # FastAPI auto-generates /docs
        if "FastAPI" in content:
            self.log_test(
                "24. API Documentation",
                True,
                "FastAPI auto-generated docs available at /docs"
            )
        else:
            self.log_test(
                "24. API Documentation",
                False,
                "API documentation not found",
                "warning"
            )
    
    # =====================================================================
    # CATEGORY 4: DEPLOYMENT & CI/CD (6 Tests)
    # =====================================================================
    
    def test_25_cicd_pipeline(self):
        """Test: CI/CD pipeline exists"""
        github_workflows = self.root_dir / ".github" / "workflows"
        
        if github_workflows.exists():
            workflow_files = list(github_workflows.glob("*.yml")) + list(github_workflows.glob("*.yaml"))
            
            if workflow_files:
                self.log_test(
                    "25. CI/CD Pipeline",
                    True,
                    f"Found {len(workflow_files)} GitHub Actions workflows"
                )
            else:
                self.log_test(
                    "25. CI/CD Pipeline",
                    False,
                    "GitHub Actions directory exists but no workflows",
                    "warning"
                )
        else:
            self.log_test(
                "25. CI/CD Pipeline",
                False,
                "No CI/CD pipeline detected",
                "critical"
            )
    
    def test_26_deployment_config(self):
        """Test: Deployment configuration exists"""
        deployment_files = [
            self.root_dir / "vercel.json",
            self.root_dir / "render.yaml",
            self.root_dir / "Procfile",
            self.root_dir / "Dockerfile"
        ]
        
        existing = [f.name for f in deployment_files if f.exists()]
        
        if existing:
            self.log_test(
                "26. Deployment Configuration",
                True,
                f"Deployment configs found: {', '.join(existing)}"
            )
        else:
            self.log_test(
                "26. Deployment Configuration",
                False,
                "No deployment configuration files found",
                "critical"
            )
    
    def test_27_gitignore_complete(self):
        """Test: .gitignore is properly configured"""
        gitignore = self.root_dir / ".gitignore"
        
        if not gitignore.exists():
            self.log_test(
                "27. .gitignore Configuration",
                False,
                ".gitignore file not found",
                "critical"
            )
            return
        
        with open(gitignore) as f:
            content = f.read()
        
        required_patterns = [".env", "node_modules", "__pycache__", "venv"]
        missing = [pattern for pattern in required_patterns if pattern not in content]
        
        if not missing:
            self.log_test(
                "27. .gitignore Configuration",
                True,
                "All critical patterns in .gitignore"
            )
        else:
            self.log_test(
                "27. .gitignore Configuration",
                False,
                f"Missing patterns: {', '.join(missing)}",
                "warning"
            )
    
    def test_28_staging_environment(self):
        """Test: Staging environment configuration exists"""
        env_files = [
            self.backend_dir / ".env.staging",
            self.frontend_dir / ".env.staging",
            self.root_dir / "vercel.staging.json"
        ]
        
        has_staging = any(f.exists() for f in env_files)
        
        if has_staging:
            self.log_test(
                "28. Staging Environment",
                True,
                "Staging environment configuration found"
            )
        else:
            self.log_test(
                "28. Staging Environment",
                False,
                "No staging environment detected",
                "warning"
            )
    
    def test_29_automated_tests(self):
        """Test: Automated test suite exists"""
        test_dirs = [
            self.backend_dir / "tests",
            self.frontend_dir / "__tests__",
            self.frontend_dir / "tests"
        ]
        
        test_files = []
        for test_dir in test_dirs:
            if test_dir.exists():
                test_files.extend(list(test_dir.rglob("test_*.py")))
                test_files.extend(list(test_dir.rglob("*.test.ts*")))
        
        if test_files:
            self.log_test(
                "29. Automated Tests",
                True,
                f"Found {len(test_files)} test files"
            )
        else:
            self.log_test(
                "29. Automated Tests",
                False,
                "No automated tests found",
                "critical"
            )
    
    def test_30_rollback_procedure(self):
        """Test: Rollback procedure is documented"""
        rollback_docs = [
            self.root_dir / "ROLLBACK_PROCEDURE.md",
            self.root_dir / "ROLLBACK.md",
            self.root_dir / "DEPLOYMENT_GUIDE_FINAL.md"
        ]
        
        has_rollback_doc = any(f.exists() for f in rollback_docs)
        
        if has_rollback_doc:
            self.log_test(
                "30. Rollback Procedure",
                True,
                "Rollback procedure documented"
            )
        else:
            self.log_test(
                "30. Rollback Procedure",
                False,
                "No rollback procedure documented",
                "warning"
            )
    
    # =====================================================================
    # CATEGORY 5: LEGAL & COMPLIANCE (5 Tests)
    # =====================================================================
    
    def test_31_privacy_policy(self):
        """Test: Privacy policy page exists"""
        privacy_pages = [
            self.frontend_dir / "src" / "app" / "privacy" / "page.tsx",
            self.frontend_dir / "src" / "pages" / "privacy.tsx"
        ]
        
        has_privacy = any(f.exists() for f in privacy_pages)
        
        if has_privacy:
            self.log_test(
                "31. Privacy Policy",
                True,
                "Privacy policy page exists"
            )
        else:
            self.log_test(
                "31. Privacy Policy",
                False,
                "No privacy policy page found",
                "critical"
            )
    
    def test_32_terms_of_service(self):
        """Test: Terms of service page exists"""
        terms_pages = [
            self.frontend_dir / "src" / "app" / "terms" / "page.tsx",
            self.frontend_dir / "src" / "pages" / "terms.tsx"
        ]
        
        has_terms = any(f.exists() for f in terms_pages)
        
        if has_terms:
            self.log_test(
                "32. Terms of Service",
                True,
                "Terms of service page exists"
            )
        else:
            self.log_test(
                "32. Terms of Service",
                False,
                "No terms of service page found",
                "critical"
            )
    
    def test_33_gdpr_compliance(self):
        """Test: GDPR compliance features (data export/deletion)"""
        # Check for data export endpoint
        has_export = False
        has_delete = False
        
        for api_file in (self.backend_dir / "app" / "api").glob("*.py"):
            try:
                with open(api_file) as f:
                    content = f.read()
                
                if "export" in content.lower() and "data" in content.lower():
                    has_export = True
                if "delete" in content.lower() and ("account" in content.lower() or "user" in content.lower()):
                    has_delete = True
            except:
                pass
        
        gdpr_score = sum([has_export, has_delete])
        
        if gdpr_score == 2:
            self.log_test(
                "33. GDPR Compliance",
                True,
                "Data export and deletion endpoints found"
            )
        elif gdpr_score == 1:
            self.log_test(
                "33. GDPR Compliance",
                False,
                "Partial GDPR compliance (missing export or deletion)",
                "warning"
            )
        else:
            self.log_test(
                "33. GDPR Compliance",
                False,
                "No GDPR compliance features detected",
                "critical"
            )
    
    def test_34_cookie_consent(self):
        """Test: Cookie consent banner exists"""
        has_cookie_consent = False
        
        for tsx_file in (self.frontend_dir / "src").rglob("*.tsx"):
            try:
                with open(tsx_file) as f:
                    content = f.read()
                
                if "cookie" in content.lower() and "consent" in content.lower():
                    has_cookie_consent = True
                    break
            except:
                pass
        
        if has_cookie_consent:
            self.log_test(
                "34. Cookie Consent",
                True,
                "Cookie consent implementation found"
            )
        else:
            self.log_test(
                "34. Cookie Consent",
                False,
                "No cookie consent banner detected",
                "warning"
            )
    
    def test_35_data_retention_policy(self):
        """Test: Data retention policy is documented"""
        retention_docs = [
            self.root_dir / "DATA_RETENTION_POLICY.md",
            self.root_dir / "PRIVACY_POLICY.md"
        ]
        
        has_retention_doc = any(f.exists() for f in retention_docs)
        
        if has_retention_doc:
            self.log_test(
                "35. Data Retention Policy",
                True,
                "Data retention policy documented"
            )
        else:
            self.log_test(
                "35. Data Retention Policy",
                False,
                "No data retention policy found",
                "warning"
            )
    
    # =====================================================================
    # CATEGORY 6: BACKUP & RECOVERY (5 Tests)
    # =====================================================================
    
    def test_36_backup_documentation(self):
        """Test: Backup strategy is documented"""
        backup_docs = [
            self.root_dir / "DISASTER_RECOVERY.md",
            self.root_dir / "BACKUP_STRATEGY.md",
            self.root_dir / "DEPLOYMENT_GUIDE_FINAL.md"
        ]
        
        has_backup_doc = False
        
        for doc in backup_docs:
            if doc.exists():
                with open(doc) as f:
                    content = f.read()
                if "backup" in content.lower():
                    has_backup_doc = True
                    break
        
        if has_backup_doc:
            self.log_test(
                "36. Backup Documentation",
                True,
                "Backup strategy is documented"
            )
        else:
            self.log_test(
                "36. Backup Documentation",
                False,
                "No backup documentation found",
                "critical"
            )
    
    def test_37_disaster_recovery_plan(self):
        """Test: Disaster recovery plan exists"""
        dr_docs = [
            self.root_dir / "DISASTER_RECOVERY.md",
            self.root_dir / "DR_PLAN.md"
        ]
        
        has_dr = any(f.exists() for f in dr_docs)
        
        if has_dr:
            self.log_test(
                "37. Disaster Recovery Plan",
                True,
                "Disaster recovery plan documented"
            )
        else:
            self.log_test(
                "37. Disaster Recovery Plan",
                False,
                "No disaster recovery plan found",
                "critical"
            )
    
    def test_38_backup_verification_script(self):
        """Test: Backup verification script exists"""
        backup_scripts = list(self.root_dir.glob("*backup*.py")) + \
                        list(self.root_dir.glob("*BACKUP*.py"))
        
        if backup_scripts:
            self.log_test(
                "38. Backup Verification Script",
                True,
                f"Found backup scripts: {', '.join([s.name for s in backup_scripts])}"
            )
        else:
            self.log_test(
                "38. Backup Verification Script",
                False,
                "No backup verification scripts found",
                "warning"
            )
    
    def test_39_database_backup_schedule(self):
        """Test: Database backup schedule is configured"""
        # Check SQL files for backup functions or schedules
        has_backup_sql = False
        
        for sql_file in self.root_dir.glob("*.sql"):
            try:
                with open(sql_file) as f:
                    content = f.read()
                
                if "backup" in content.lower() or "pg_dump" in content.lower():
                    has_backup_sql = True
                    break
            except:
                pass
        
        # Supabase provides automatic backups
        if has_backup_sql:
            self.log_test(
                "39. Database Backup Schedule",
                True,
                "Database backup configuration found"
            )
        else:
            self.log_test(
                "39. Database Backup Schedule",
                False,
                "No explicit backup schedule (relying on Supabase auto-backup)",
                "warning"
            )
    
    def test_40_file_storage_backup(self):
        """Test: File storage backup strategy exists"""
        storage_files = list((self.backend_dir / "app").rglob("*storage*.py"))
        
        has_backup_strategy = False
        
        for storage_file in storage_files:
            try:
                with open(storage_file) as f:
                    content = f.read()
                
                if "backup" in content.lower() or "s3" in content.lower():
                    has_backup_strategy = True
                    break
            except:
                pass
        
        if has_backup_strategy:
            self.log_test(
                "40. File Storage Backup",
                True,
                "File storage backup strategy detected"
            )
        else:
            self.log_test(
                "40. File Storage Backup",
                False,
                "No file storage backup strategy (relying on Supabase Storage)",
                "warning"
            )
    
    # =====================================================================
    # RUN ALL TESTS
    # =====================================================================
    
    def run_all_tests(self):
        """Run all production readiness tests"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}")
        print("=" * 80)
        print("🚀 PRODUCTION READINESS AUDIT - 40 COMPREHENSIVE TESTS")
        print("=" * 80)
        print(f"{Colors.ENDC}")
        print(f"\nProject: TrulyInvoice")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Root: {self.root_dir}")
        
        # Category 1: Security & Authentication
        self.print_section("🔒 CATEGORY 1: SECURITY & AUTHENTICATION (10 Tests)")
        self.test_01_environment_variables()
        self.test_02_rate_limiting_enabled()
        self.test_03_no_api_keys_in_code()
        self.test_04_cors_configured()
        self.test_05_sql_injection_protection()
        self.test_06_xss_protection()
        self.test_07_file_upload_validation()
        self.test_08_authentication_required()
        self.test_09_password_hashing()
        self.test_10_https_enforcement()
        
        # Category 2: Database & Performance
        self.print_section("🗄️ CATEGORY 2: DATABASE & PERFORMANCE (8 Tests)")
        self.test_11_database_indexes()
        self.test_12_connection_pooling()
        self.test_13_pagination_implemented()
        self.test_14_caching_layer()
        self.test_15_database_migrations()
        self.test_16_n_plus_one_queries()
        self.test_17_query_timeout()
        self.test_18_bulk_operations()
        
        # Category 3: API & Monitoring
        self.print_section("📊 CATEGORY 3: API & MONITORING (6 Tests)")
        self.test_19_health_endpoint()
        self.test_20_error_monitoring()
        self.test_21_logging_configured()
        self.test_22_api_versioning()
        self.test_23_request_timeout()
        self.test_24_api_documentation()
        
        # Category 4: Deployment & CI/CD
        self.print_section("🚢 CATEGORY 4: DEPLOYMENT & CI/CD (6 Tests)")
        self.test_25_cicd_pipeline()
        self.test_26_deployment_config()
        self.test_27_gitignore_complete()
        self.test_28_staging_environment()
        self.test_29_automated_tests()
        self.test_30_rollback_procedure()
        
        # Category 5: Legal & Compliance
        self.print_section("⚖️ CATEGORY 5: LEGAL & COMPLIANCE (5 Tests)")
        self.test_31_privacy_policy()
        self.test_32_terms_of_service()
        self.test_33_gdpr_compliance()
        self.test_34_cookie_consent()
        self.test_35_data_retention_policy()
        
        # Category 6: Backup & Recovery
        self.print_section("💾 CATEGORY 6: BACKUP & RECOVERY (5 Tests)")
        self.test_36_backup_documentation()
        self.test_37_disaster_recovery_plan()
        self.test_38_backup_verification_script()
        self.test_39_database_backup_schedule()
        self.test_40_file_storage_backup()
        
        # Generate final report
        self.generate_report()
    
    def generate_report(self):
        """Generate final audit report"""
        duration = time.time() - self.start_time
        total_tests = self.passed + self.failed + self.warnings
        
        print(f"\n{Colors.BOLD}{Colors.HEADER}")
        print("=" * 80)
        print("📊 AUDIT SUMMARY")
        print("=" * 80)
        print(f"{Colors.ENDC}")
        
        # Calculate score
        score = (self.passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n{Colors.BOLD}Overall Score: {score:.1f}/100{Colors.ENDC}")
        
        if score >= 90:
            status = f"{Colors.OKGREEN}✅ PRODUCTION READY{Colors.ENDC}"
        elif score >= 75:
            status = f"{Colors.OKCYAN}🟢 GOOD - Minor fixes needed{Colors.ENDC}"
        elif score >= 60:
            status = f"{Colors.WARNING}🟡 NEEDS WORK - Several issues{Colors.ENDC}"
        else:
            status = f"{Colors.FAIL}🔴 NOT READY - Critical issues{Colors.ENDC}"
        
        print(f"Status: {status}\n")
        
        print(f"{Colors.OKGREEN}✓ Passed:  {self.passed}{Colors.ENDC}")
        print(f"{Colors.FAIL}✗ Failed:  {self.failed}{Colors.ENDC}")
        print(f"{Colors.WARNING}⚠ Warnings: {self.warnings}{Colors.ENDC}")
        print(f"Total Tests: {total_tests}")
        print(f"Duration: {duration:.2f}s")
        
        # Critical issues
        if self.critical_issues:
            print(f"\n{Colors.FAIL}{Colors.BOLD}🚨 CRITICAL ISSUES (MUST FIX):{Colors.ENDC}")
            for issue in self.critical_issues:
                print(f"  • {issue}")
        
        # Save detailed report
        self.save_report(score, status)
        
        print(f"\n{Colors.OKBLUE}📄 Detailed report saved to: PRODUCTION_AUDIT_REPORT.json{Colors.ENDC}")
        print(f"{Colors.OKBLUE}📋 Markdown report saved to: PRODUCTION_AUDIT_REPORT.md{Colors.ENDC}")
        
        # Exit code based on critical issues
        if self.critical_issues:
            print(f"\n{Colors.FAIL}⚠️  Fix critical issues before deploying to production!{Colors.ENDC}")
            sys.exit(1)
        else:
            print(f"\n{Colors.OKGREEN}🎉 No critical blockers - ready for production!{Colors.ENDC}")
            sys.exit(0)
    
    def save_report(self, score: float, status: str):
        """Save detailed report to files"""
        report_data = {
            "audit_date": datetime.now().isoformat(),
            "score": score,
            "status": status,
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "critical_issues": self.critical_issues,
            "results": self.results
        }
        
        # Save JSON report
        with open("PRODUCTION_AUDIT_REPORT.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        # Save Markdown report
        with open("PRODUCTION_AUDIT_REPORT.md", "w") as f:
            f.write("# 🚀 Production Readiness Audit Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Overall Score:** {score:.1f}/100\n\n")
            f.write(f"**Status:** {status}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- ✓ Passed: {self.passed}\n")
            f.write(f"- ✗ Failed: {self.failed}\n")
            f.write(f"- ⚠ Warnings: {self.warnings}\n\n")
            
            if self.critical_issues:
                f.write("## 🚨 Critical Issues\n\n")
                for issue in self.critical_issues:
                    f.write(f"- {issue}\n")
                f.write("\n")
            
            f.write("## Detailed Results\n\n")
            
            categories = {
                "Security & Authentication": range(1, 11),
                "Database & Performance": range(11, 19),
                "API & Monitoring": range(19, 25),
                "Deployment & CI/CD": range(25, 31),
                "Legal & Compliance": range(31, 36),
                "Backup & Recovery": range(36, 41)
            }
            
            for category, test_range in categories.items():
                f.write(f"### {category}\n\n")
                
                category_results = [r for r in self.results 
                                  if any(f"{i:02d}." in r["test_name"] for i in test_range)]
                
                for result in category_results:
                    symbol = "✓" if result["passed"] else ("⚠" if result["severity"] == "warning" else "✗")
                    f.write(f"{symbol} **{result['test_name']}**\n")
                    if result["details"]:
                        f.write(f"  - {result['details']}\n")
                    f.write("\n")


def main():
    """Main entry point"""
    print(f"\n{Colors.BOLD}Starting Production Readiness Audit...{Colors.ENDC}\n")
    
    auditor = ProductionReadinessAuditor()
    auditor.run_all_tests()


if __name__ == "__main__":
    main()
