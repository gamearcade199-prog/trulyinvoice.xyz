"""
Supabase Helper - Direct REST API calls using requests
NO httpx/httpcore dependency conflicts!
"""
import os
import requests
from typing import Dict, Any, List, Optional

class SupabaseClient:
    """Simple Supabase client using REST API"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_SERVICE_KEY")
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    def query(self, table: str, method: str = "GET", filters: Dict = None, data: Dict = None) -> Dict:
        """Execute a Supabase query"""
        url = f"{self.url}/rest/v1/{table}"
        
        # Add filters to URL
        if filters:
            params = []
            for key, value in filters.items():
                if value is None:
                    params.append(f"{key}=is.null")
                else:
                    params.append(f"{key}=eq.{value}")
            url += "?" + "&".join(params)
        
        # Execute request
        if method == "GET":
            response = requests.get(url, headers=self.headers)
        elif method == "POST":
            response = requests.post(url, headers=self.headers, json=data)
        elif method == "PATCH":
            response = requests.patch(url, headers=self.headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=self.headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        if response.status_code >= 400:
            raise Exception(f"Supabase error: {response.status_code} - {response.text}")
        
        return response.json()
    
    def select(self, table: str, columns: str = "*", filters: Dict = None) -> List[Dict]:
        """SELECT query"""
        url = f"{self.url}/rest/v1/{table}?select={columns}"
        
        if filters:
            for key, value in filters.items():
                url += f"&{key}=eq.{value}"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code >= 400:
            raise Exception(f"Supabase error: {response.status_code} - {response.text}")
        
        return response.json()
    
    def insert(self, table: str, data: Dict) -> Dict:
        """INSERT query"""
        result = self.query(table, method="POST", data=data)
        return result[0] if result else {}
    
    def update(self, table: str, filters: Dict, data: Dict) -> Dict:
        """UPDATE query"""
        result = self.query(table, method="PATCH", filters=filters, data=data)
        return result[0] if result else {}
    
    def delete(self, table: str, filters: Dict) -> bool:
        """DELETE query"""
        self.query(table, method="DELETE", filters=filters)
        return True


# Global instance
supabase = SupabaseClient()
