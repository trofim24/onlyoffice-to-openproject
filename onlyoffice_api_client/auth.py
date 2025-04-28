# onlyoffice_api_client/auth.py
import requests
import json
from typing import Dict, Any, Optional

class OnlyOfficeAuth:
    """
    Class for handling authentication with ONLYOFFICE API
    """
    
    def __init__(self, portal_url: str):
        """
        Initialize the authentication client
        
        Args:
            portal_url (str): Your ONLYOFFICE portal URL (e.g., https://yourportal.onlyoffice.com)
        """
        self.portal_url = portal_url.rstrip('/')
        self.auth_endpoint = f"{self.portal_url}/api/2.0/authentication.json"
        self.token = None
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Authenticate with username and password
        
        Args:
            username (str): Your ONLYOFFICE username
            password (str): Your ONLYOFFICE password
            
        Returns:
            dict: The JSON response from the authentication API
        """
        data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(
            self.auth_endpoint, 
            headers=self.headers, 
            data=json.dumps(data)
        )
        
        if response.status_code == 200:
            result = response.json()
            if "response" in result and "token" in result["response"]:
                self.token = result["response"]["token"]
                # Update headers with token for future requests
                self.headers["Authorization"] = f"Bearer {self.token}"
            return result
        else:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": response.text
            }
    
    def get_token(self) -> Optional[str]:
        """
        Get the current authentication token
        
        Returns:
            str or None: The authentication token if available
        """
        return self.token
    
    def logout(self) -> Dict[str, Any]:
        """
        Logout and invalidate the current token
        
        Returns:
            dict: The JSON response from the logout API
        """
        if not self.token:
            return {"error": True, "message": "Not logged in"}
            
        logout_endpoint = f"{self.portal_url}/api/2.0/authentication/logout.json"
        
        response = requests.post(
            logout_endpoint,
            headers=self.headers
        )
        
        if response.status_code == 200:
            self.token = None
            if "Authorization" in self.headers:
                del self.headers["Authorization"]
            return response.json()
        else:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": response.text
            }
