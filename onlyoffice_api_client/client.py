from .auth import OnlyOfficeAuth
import requests
import json
from typing import Dict, Any, Optional

class OnlyOfficeClient:
    """
    Main client for interacting with ONLYOFFICE API
    """
    
    def __init__(self, portal_url: str):
        """
        Initialize the ONLYOFFICE API client
        
        Args:
            portal_url (str): Your ONLYOFFICE portal URL
        """
        self.portal_url = portal_url.rstrip('/')
        self.auth = OnlyOfficeAuth(portal_url)
    
    def authenticate(self, username: str, password: str) -> Dict[str, Any]:
        """
        Authenticate with the ONLYOFFICE API
        
        Args:
            username (str): Your ONLYOFFICE username
            password (str): Your ONLYOFFICE password
            
        Returns:
            dict: The authentication result
        """
        return self.auth.login(username, password)
    
    def get_people(self) -> Dict[str, Any]:
        """
        Get list of people from ONLYOFFICE
        
        Returns:
            dict: The people response from the API
        """
        if not self.auth.get_token():
            return {"error": True, "message": "Not authenticated"}
            
        endpoint = f"{self.portal_url}/api/2.0/people.json"
        
        response = requests.get(
            endpoint,
            headers=self.auth.headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": response.text
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
        
        response = requests.get(
            endpoint,
            headers=self.auth.headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": response.text
            }

