# onlyoffice_api_client/auth.py
import requests
import json
from typing import Dict, Any, Optional

class OnlyOfficeAuth:
    """
    Class for handling authentication with ONLYOFFICE API
    """
    
    def __init__(self, portal_url: str, verify_ssl: bool = True):
        """
        Initialize the authentication client
        
        Args:
            portal_url (str): Your ONLYOFFICE portal URL (e.g., https://yourportal.onlyoffice.com)
            verify_ssl (bool): Whether to verify SSL certificates
        """
        self.portal_url = portal_url.rstrip('/')
        self.auth_base_endpoint = f"{self.portal_url}/api/2.0/authentication"
        self.token = None
        self.headers = {
            "Content-Type": "application/json"
        }
        self.verify_ssl = verify_ssl
    
    def login(self, username: str, password: str, code: str = None) -> Dict[str, Any]:
        """
        Authenticate with ONLYOFFICE
        
        Args:
            username (str): Your ONLYOFFICE username
            password (str): Your ONLYOFFICE password
            code (str, optional): Authentication code if required
            
        Returns:
            dict: The JSON response from the authentication API
        """
        # Build request payload
        data = {
            "username": username,
            "password": password
        }
        
        # Determine the endpoint based on whether a code is provided
        if code:
            auth_endpoint = f"{self.auth_base_endpoint}/{code}"
        else:
            auth_endpoint = f"{self.auth_base_endpoint}.json"
        
        try:
            response = requests.post(
                auth_endpoint, 
                headers=self.headers, 
                data=json.dumps(data),
                verify=self.verify_ssl
            )
            
            # Check if request was successful (200 OK or 201 Created)
            if response.status_code in [200, 201]:
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
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "exception": str(e),
                "message": "Connection error occurred"
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
            
        logout_endpoint = f"{self.auth_base_endpoint}/logout.json"
        
        try:
            response = requests.post(
                logout_endpoint,
                headers=self.headers,
                verify=self.verify_ssl
            )
            
            # Accept both 200 and 201 as success codes
            if response.status_code in [200, 201]:
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
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "exception": str(e),
                "message": "Connection error occurred"
            }
