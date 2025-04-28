# onlyoffice_api_client/client.py
from .auth import OnlyOfficeAuth
import requests
import json
from typing import Dict, Any, Optional

class OnlyOfficeClient:
    """
    Main client for interacting with ONLYOFFICE API
    """
    
    def __init__(self, portal_url: str, verify_ssl: bool = True, auth_token: Optional[str] = None):
        """
        Initialize the ONLYOFFICE API client

        Args:
            portal_url (str): Your ONLYOFFICE portal URL
            verify_ssl (bool): Whether to verify SSL certificates
            auth_token (str, optional): Pre-set authentication token
        """
        self.portal_url = portal_url.rstrip('/')
        self.auth = OnlyOfficeAuth(portal_url, verify_ssl=verify_ssl)
        self.verify_ssl = verify_ssl
        if auth_token:
            # Set the auth token directly if provided
            self.auth.token = auth_token
    
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
        if not self.auth.get_token():
            return self.auth.login(
                username=username, 
                password=password,
                code=code
            )
        return {"message": "Already authenticated with a token"}
    
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
    
    def get_projects(self, filter_type: str = "@self") -> Dict[str, Any]:
        """
        Get projects from ONLYOFFICE
        
        Args:
            filter_type (str, optional): Filter type for projects. 
                Default is "@self" for current user's projects.
                Other options include: "@followed", "@recent", "@favorite", etc.
                
        Returns:
            dict: The projects response from the API
        """
        if not self.auth.get_token():
            return {"error": True, "message": "Not authenticated"}
            
        endpoint = f"{self.portal_url}/api/2.0/project/{filter_type}.json"
        
        try:
            response = requests.get(
                endpoint,
                headers=self.auth.headers,
                verify=self.verify_ssl
            )
            
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
    from typing import Union, List

    from typing import Union, List

    def get_project_tasks(self, project_id: int, statuses: Optional[Union[str, List[str]]] = None) -> Dict[str, Any]:
        """
        Get tasks from a project by one or multiple statuses.
        
        Args:
            project_id (int): ID of the project
            statuses (Union[str, List[str]], optional): Status or list of statuses. 
                If None, fetches tasks for all statuses.
            
        Returns:
            dict: The combined tasks response from the API
        """
        if not self.auth.get_token():
            return {"error": True, "message": "Not authenticated"}

        allowed_statuses = {"notaccept", "open", "closed", "disable", "unclassified", "notinmilestone"}

        # If no statuses specified, use all allowed statuses
        if statuses is None:
            statuses = list(allowed_statuses)
        elif isinstance(statuses, str):
            statuses = [statuses]

        invalid_statuses = [status for status in statuses if status not in allowed_statuses]
        if invalid_statuses:
            return {"error": True, "message": f"Invalid statuses: {', '.join(invalid_statuses)}"}

        all_tasks = []
        errors = []

        for status in statuses:
            endpoint = f"{self.portal_url}/api/2.0/project/{project_id}/task/{status}.json"
            try:
                response = requests.get(
                    endpoint,
                    headers=self.auth.headers,
                    verify=self.verify_ssl
                )
                
                if response.status_code in [200, 201]:
                    data = response.json()
                    if "response" in data:
                        all_tasks.extend(data["response"])
                else:
                    errors.append({
                        "status": status,
                        "status_code": response.status_code,
                        "message": response.text
                    })
            except requests.exceptions.RequestException as e:
                errors.append({
                    "status": status,
                    "exception": str(e),
                    "message": "Connection error occurred"
                })

        result = {"tasks": all_tasks}
        if errors:
            result["errors"] = errors

        return result
