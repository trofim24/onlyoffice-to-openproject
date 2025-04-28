# onlyoffice_api_client/client.py
from .auth import OnlyOfficeAuth
import requests
import json
from typing import Dict, Any, Optional

class OnlyOfficeClient:
    """
    Main client for interacting with ONLYOFFICE API
    """
    
    def __init__(self, portal_url: str, verify_ssl: bool = True):
        """
        Initialize the ONLYOFFICE API client
        
        Args:
            portal_url (str): Your ONLYOFFICE portal URL
            verify_ssl (bool): Whether to verify SSL certificates
        """
        self.portal_url = portal_url.rstrip('/')
        self.auth = OnlyOfficeAuth(portal_url, verify_ssl=verify_ssl)
        self.verify_ssl = verify_ssl
    
    def authenticate(self, username: str, password: str, code: str = None) -> Dict[str, Any]:
        """
        Authenticate with the ONLYOFFICE API
        
        Args:
            username (str): Your ONLYOFFICE username
            password (str): Your ONLYOFFICE password
            code (str, optional): Authentication code if required
            
        Returns:
            dict: The authentication result
        """
        return self.auth.login(
            username=username, 
            password=password,
            code=code
        )
    
    def get_people(self) -> Dict[str, Any]:
        """
        Get list of people from ONLYOFFICE
        
        Returns:
            dict: The people response from the API
        """
        if not self.auth.get_token():
            return {"error": True, "message": "Not authenticated"}
            
        endpoint = f"{self.portal_url}/api/2.0/people.json"
        
        try:
            response = requests.get(
                endpoint,
                headers=self.auth.headers,
                verify=self.verify_ssl
            )
            
            # Accept both 200 and 201 as success codes
            if response.status_code in [200, 201]:
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
    
    def get_files(self, folder_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get files from ONLYOFFICE
        
        Args:
            folder_id (str, optional): Folder ID to get files from
            
        Returns:
            dict: The files response from the API
        """
        if not self.auth.get_token():
            return {"error": True, "message": "Not authenticated"}
            
        endpoint = f"{self.portal_url}/api/2.0/files"
        if folder_id:
            endpoint += f"/@folder/{folder_id}"
        endpoint += ".json"
        
        try:
            response = requests.get(
                endpoint,
                headers=self.auth.headers,
                verify=self.verify_ssl
            )
            
            # Accept both 200 and 201 as success codes
            if response.status_code in [200, 201]:
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
