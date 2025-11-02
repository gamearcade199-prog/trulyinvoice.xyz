"""
Virus Scanner Service
SECURITY FIX: Malware/virus scanning for uploaded files
Supports VirusTotal API (recommended) or ClamAV (self-hosted)
"""

import os
import hashlib
import logging
import requests
from typing import Dict, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class VirusTotalScanner:
    """
    Scan files using VirusTotal API
    Free tier: 4 requests/minute, 500/day
    """
    
    def __init__(self):
        self.api_key = os.getenv('VIRUSTOTAL_API_KEY')
        self.api_url = "https://www.virustotal.com/api/v3/files"
        self.enabled = bool(self.api_key)
        
        if not self.enabled:
            logger.warning("VirusTotal API key not found. Malware scanning disabled.")
            logger.info("Set VIRUSTOTAL_API_KEY in .env to enable malware scanning")
    
    def calculate_file_hash(self, file_content: bytes) -> str:
        """Calculate SHA256 hash of file"""
        return hashlib.sha256(file_content).hexdigest()
    
    def scan_file(self, file_content: bytes, filename: str = "file") -> Dict:
        """
        Scan file for malware
        
        Args:
            file_content: File content as bytes
            filename: Original filename
        
        Returns:
            Dictionary with scan results
        """
        if not self.enabled:
            return {
                "scanned": False,
                "safe": True,  # Assume safe if scanning disabled
                "message": "Malware scanning disabled (no API key)",
                "details": {}
            }
        
        try:
            # Calculate file hash
            file_hash = self.calculate_file_hash(file_content)
            
            # Check if file was previously scanned
            cached_result = self._check_hash(file_hash)
            if cached_result:
                return cached_result
            
            # Upload and scan new file
            headers = {"x-apikey": self.api_key}
            files = {"file": (filename, file_content)}
            
            logger.info(f"Scanning file with VirusTotal: {filename} ({len(file_content)} bytes)")
            
            response = requests.post(
                self.api_url,
                headers=headers,
                files=files,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                analysis_id = data.get("data", {}).get("id")
                
                # Get scan results
                if analysis_id:
                    result = self._get_scan_results(analysis_id)
                    return result
                else:
                    logger.error("No analysis ID returned from VirusTotal")
                    return {
                        "scanned": False,
                        "safe": True,  # Assume safe if scan fails
                        "message": "Scan failed - no analysis ID",
                        "details": {}
                    }
            
            elif response.status_code == 429:
                # Rate limit exceeded
                logger.warning("VirusTotal rate limit exceeded")
                return {
                    "scanned": False,
                    "safe": True,  # Assume safe if rate limited
                    "message": "Rate limit exceeded - scan skipped",
                    "details": {}
                }
            
            else:
                logger.error(f"VirusTotal API error: {response.status_code}")
                return {
                    "scanned": False,
                    "safe": True,  # Assume safe if API error
                    "message": f"API error: {response.status_code}",
                    "details": {}
                }
        
        except requests.Timeout:
            logger.error("VirusTotal API timeout")
            return {
                "scanned": False,
                "safe": True,
                "message": "Scan timeout",
                "details": {}
            }
        
        except Exception as e:
            logger.error(f"VirusTotal scan error: {str(e)}")
            return {
                "scanned": False,
                "safe": True,
                "message": f"Scan error: {str(e)}",
                "details": {}
            }
    
    def _check_hash(self, file_hash: str) -> Dict:
        """Check if file hash was previously scanned"""
        try:
            headers = {"x-apikey": self.api_key}
            url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                
                malicious = stats.get("malicious", 0)
                suspicious = stats.get("suspicious", 0)
                
                logger.info(f"File hash found in VirusTotal cache: {file_hash[:8]}...")
                
                return {
                    "scanned": True,
                    "safe": malicious == 0 and suspicious == 0,
                    "message": "Previously scanned (cached result)",
                    "details": {
                        "malicious": malicious,
                        "suspicious": suspicious,
                        "undetected": stats.get("undetected", 0),
                        "harmless": stats.get("harmless", 0)
                    }
                }
            
            return None  # Not in cache
        
        except Exception as e:
            logger.debug(f"Hash check failed: {str(e)}")
            return None
    
    def _get_scan_results(self, analysis_id: str, max_attempts: int = 3) -> Dict:
        """
        Get scan results from VirusTotal
        Polls for results if analysis is still pending
        """
        import time
        
        headers = {"x-apikey": self.api_key}
        url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("data", {}).get("attributes", {}).get("status")
                    
                    if status == "completed":
                        stats = data.get("data", {}).get("attributes", {}).get("stats", {})
                        
                        malicious = stats.get("malicious", 0)
                        suspicious = stats.get("suspicious", 0)
                        
                        return {
                            "scanned": True,
                            "safe": malicious == 0 and suspicious == 0,
                            "message": f"Scan complete: {malicious} threats detected",
                            "details": {
                                "malicious": malicious,
                                "suspicious": suspicious,
                                "undetected": stats.get("undetected", 0),
                                "harmless": stats.get("harmless", 0)
                            }
                        }
                    
                    # Still queued/in-progress
                    if attempt < max_attempts - 1:
                        time.sleep(2)  # Wait 2 seconds before retry
                        continue
                
                # Timeout or error
                return {
                    "scanned": False,
                    "safe": True,
                    "message": "Scan timeout - assuming safe",
                    "details": {}
                }
            
            except Exception as e:
                logger.error(f"Error getting scan results: {str(e)}")
                return {
                    "scanned": False,
                    "safe": True,
                    "message": f"Error: {str(e)}",
                    "details": {}
                }
        
        # Max attempts reached
        return {
            "scanned": False,
            "safe": True,
            "message": "Scan timeout - assuming safe",
            "details": {}
        }
    
    def is_safe(self, scan_result: Dict) -> bool:
        """Check if file is safe based on scan result"""
        return scan_result.get("safe", True)


class ClamAVScanner:
    """
    Scan files using ClamAV (self-hosted antivirus)
    Requires clamd service running
    """
    
    def __init__(self):
        try:
            import clamd
            self.cd = clamd.ClamdUnixSocket()
            self.enabled = True
            logger.info("ClamAV scanner initialized")
        except ImportError:
            self.enabled = False
            logger.warning("ClamAV not available (clamd not installed)")
        except Exception as e:
            self.enabled = False
            logger.warning(f"ClamAV not available: {str(e)}")
    
    def scan_file(self, file_content: bytes, filename: str = "file") -> Dict:
        """Scan file with ClamAV"""
        if not self.enabled:
            return {
                "scanned": False,
                "safe": True,
                "message": "ClamAV not available",
                "details": {}
            }
        
        try:
            result = self.cd.scan_stream(file_content)
            
            if result is None:
                # Clean file
                return {
                    "scanned": True,
                    "safe": True,
                    "message": "File is clean",
                    "details": {}
                }
            else:
                # Virus found
                return {
                    "scanned": True,
                    "safe": False,
                    "message": f"Virus detected: {result}",
                    "details": {"result": str(result)}
                }
        
        except Exception as e:
            logger.error(f"ClamAV scan error: {str(e)}")
            return {
                "scanned": False,
                "safe": True,
                "message": f"Scan error: {str(e)}",
                "details": {}
            }
    
    def is_safe(self, scan_result: Dict) -> bool:
        """Check if file is safe"""
        return scan_result.get("safe", True)


# Default scanner (VirusTotal)
_scanner = None

def get_scanner():
    """Get active virus scanner"""
    global _scanner
    
    if _scanner is None:
        # Try VirusTotal first (preferred)
        vt_scanner = VirusTotalScanner()
        if vt_scanner.enabled:
            _scanner = vt_scanner
            logger.info("Using VirusTotal scanner")
        else:
            # Fall back to ClamAV
            clamav_scanner = ClamAVScanner()
            if clamav_scanner.enabled:
                _scanner = clamav_scanner
                logger.info("Using ClamAV scanner")
            else:
                # No scanner available - create disabled scanner
                _scanner = VirusTotalScanner()  # Returns safe=True for all scans
                logger.warning("No virus scanner available - malware scanning disabled")
    
    return _scanner


def scan_file(file_content: bytes, filename: str = "file") -> Tuple[bool, str]:
    """
    Scan file for malware
    
    Args:
        file_content: File content as bytes
        filename: Original filename
    
    Returns:
        Tuple of (is_safe: bool, message: str)
    """
    scanner = get_scanner()
    result = scanner.scan_file(file_content, filename)
    
    is_safe = scanner.is_safe(result)
    message = result.get("message", "Scan complete")
    
    if result.get("scanned") and result.get("details"):
        details = result["details"]
        if details.get("malicious", 0) > 0:
            message = f"Malware detected: {details['malicious']} threats found"
        elif details.get("suspicious", 0) > 0:
            message = f"Suspicious file: {details['suspicious']} warnings"
    
    return is_safe, message


if __name__ == "__main__":
    print("✅ Virus Scanner module loaded")
    print("\nAvailable scanners:")
    print("  - VirusTotal API (requires VIRUSTOTAL_API_KEY)")
    print("  - ClamAV (requires clamd service)")
    print("\nTo enable:")
    print("  1. Add VIRUSTOTAL_API_KEY=your_key to .env")
    print("  2. Or install ClamAV: pip install clamd")
