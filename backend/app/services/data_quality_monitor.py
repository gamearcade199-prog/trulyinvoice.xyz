"""
📊 INVOICE DATA QUALITY MONITORING & LOGGING
Tracks data issues and generates quality reports
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from app.services.supabase_helper import supabase


class DataQualityMonitor:
    """Monitors and logs data quality issues"""
    
    # Issue severity levels
    SEVERITY_CRITICAL = 'critical'
    SEVERITY_WARNING = 'warning'
    SEVERITY_INFO = 'info'
    
    # Issue categories
    CATEGORY_VALIDATION = 'validation'
    CATEGORY_EXTRACTION = 'extraction'
    CATEGORY_EXPORT = 'export'
    CATEGORY_DATABASE = 'database'
    
    @classmethod
    def log_validation_issue(
        cls,
        user_id: str,
        invoice_data: Dict[str, Any],
        severity: str,
        issue_type: str,
        description: str
    ) -> bool:
        """
        Log a data quality issue
        
        Args:
            user_id: User who owns the invoice
            invoice_data: The invoice data that caused the issue
            severity: 'critical', 'warning', or 'info'
            issue_type: Type of issue (e.g., 'missing_field', 'invalid_value')
            description: Human-readable description of the issue
        
        Returns:
            True if logged successfully
        """
        try:
            log_entry = {
                'user_id': user_id,
                'invoice_id': invoice_data.get('id'),
                'document_id': invoice_data.get('document_id'),
                'severity': severity,
                'issue_type': issue_type,
                'category': cls.CATEGORY_VALIDATION,
                'description': description,
                'invoice_snapshot': {
                    'invoice_number': invoice_data.get('invoice_number'),
                    'vendor_name': invoice_data.get('vendor_name'),
                    'total_amount': invoice_data.get('total_amount'),
                    'payment_status': invoice_data.get('payment_status')
                },
                'created_at': datetime.now().isoformat()
            }
            
            # Try to save to monitoring table
            supabase.table('invoice_quality_logs').insert(log_entry).execute()
            
            # Also print to logs for immediate visibility
            emoji = '🔴' if severity == cls.SEVERITY_CRITICAL else '⚠️' if severity == cls.SEVERITY_WARNING else 'ℹ️'
            print(f"{emoji} [{severity.upper()}] {issue_type}: {description}")
            
            return True
        except Exception as e:
            print(f"❌ Failed to log quality issue: {e}")
            return False
    
    @classmethod
    def generate_quality_report(cls, user_id: str, days: int = 7) -> Dict[str, Any]:
        """
        Generate a data quality report for a user
        
        Args:
            user_id: User ID
            days: Number of days to analyze
        
        Returns:
            Quality report with statistics
        """
        try:
            # Query logs from the last N days
            start_date = datetime.now().isoformat()
            
            logs = supabase.table('invoice_quality_logs')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .execute()
            
            if not logs.data:
                return {
                    'user_id': user_id,
                    'period_days': days,
                    'total_issues': 0,
                    'critical_issues': 0,
                    'warnings': 0,
                    'quality_score': 100.0,
                    'status': '✅ No issues found'
                }
            
            # Analyze logs
            critical = sum(1 for log in logs.data if log['severity'] == cls.SEVERITY_CRITICAL)
            warnings = sum(1 for log in logs.data if log['severity'] == cls.SEVERITY_WARNING)
            infos = sum(1 for log in logs.data if log['severity'] == cls.SEVERITY_INFO)
            
            total_issues = critical + warnings + infos
            
            # Calculate quality score (0-100)
            # Each critical issue = -20 points
            # Each warning = -5 points
            # Each info = -1 point
            quality_score = max(0, 100 - (critical * 20 + warnings * 5 + infos * 1))
            
            # Group by issue type
            issue_types = {}
            for log in logs.data:
                issue_type = log['issue_type']
                issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
            
            status = '✅ Excellent' if quality_score >= 90 else \
                     '🟢 Good' if quality_score >= 70 else \
                     '🟡 Fair' if quality_score >= 50 else \
                     '🔴 Poor'
            
            return {
                'user_id': user_id,
                'period_days': days,
                'quality_score': quality_score,
                'status': status,
                'total_issues': total_issues,
                'critical_issues': critical,
                'warnings': warnings,
                'info_messages': infos,
                'issue_breakdown': issue_types,
                'top_issues': sorted(issue_types.items(), key=lambda x: x[1], reverse=True)[:5]
            }
        
        except Exception as e:
            print(f"❌ Failed to generate quality report: {e}")
            return {'error': str(e)}
    
    @classmethod
    def get_problematic_invoices(cls, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get invoices with the most quality issues
        
        Returns:
            List of problematic invoices with issue counts
        """
        try:
            logs = supabase.table('invoice_quality_logs')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .execute()
            
            if not logs.data:
                return []
            
            # Group by invoice_id and count issues
            invoice_issues = {}
            for log in logs.data:
                invoice_id = log['invoice_id']
                if invoice_id:
                    if invoice_id not in invoice_issues:
                        invoice_issues[invoice_id] = {
                            'invoice_id': invoice_id,
                            'document_id': log['document_id'],
                            'issue_count': 0,
                            'critical_count': 0,
                            'last_issue': log['created_at'],
                            'issues': []
                        }
                    
                    invoice_issues[invoice_id]['issue_count'] += 1
                    if log['severity'] == cls.SEVERITY_CRITICAL:
                        invoice_issues[invoice_id]['critical_count'] += 1
                    
                    invoice_issues[invoice_id]['issues'].append({
                        'type': log['issue_type'],
                        'severity': log['severity'],
                        'description': log['description']
                    })
            
            # Sort by issue count and return top N
            sorted_issues = sorted(
                invoice_issues.values(),
                key=lambda x: (x['critical_count'], x['issue_count']),
                reverse=True
            )[:limit]
            
            return sorted_issues
        
        except Exception as e:
            print(f"❌ Failed to get problematic invoices: {e}")
            return []


# ============ CONVENIENCE FUNCTIONS ============

def log_critical_issue(user_id: str, invoice_data: Dict, issue_type: str, description: str):
    """Shorthand for logging critical issues"""
    DataQualityMonitor.log_validation_issue(
        user_id=user_id,
        invoice_data=invoice_data,
        severity=DataQualityMonitor.SEVERITY_CRITICAL,
        issue_type=issue_type,
        description=description
    )


def log_warning_issue(user_id: str, invoice_data: Dict, issue_type: str, description: str):
    """Shorthand for logging warning issues"""
    DataQualityMonitor.log_validation_issue(
        user_id=user_id,
        invoice_data=invoice_data,
        severity=DataQualityMonitor.SEVERITY_WARNING,
        issue_type=issue_type,
        description=description
    )


def get_user_quality_score(user_id: str) -> float:
    """Get user's overall data quality score (0-100)"""
    report = DataQualityMonitor.generate_quality_report(user_id)
    return report.get('quality_score', 100.0)
