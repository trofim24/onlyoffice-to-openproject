from onlyoffice_api_client import OnlyOfficeClient
import json
import os
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get credentials from environment variables
    portal_url = os.getenv("ONLYOFFICE_PORTAL_URL")
    username = os.getenv("ONLYOFFICE_USERNAME")
    password = os.getenv("ONLYOFFICE_PASSWORD")
    
    if not portal_url or not username or not password:
        print("Please set ONLYOFFICE_PORTAL_URL, ONLYOFFICE_USERNAME, and ONLYOFFICE_PASSWORD in your .env file")
        return
    
    # Initialize the client
    client = OnlyOfficeClient(portal_url)
    
    # Authenticate
    auth_result = client.authenticate(username, password)
    print("Authentication result:")
    print(json.dumps(auth_result, indent=4))
    
    if "error" in auth_result and auth_result["error"]:
        print("Authentication failed")
        return
    
    # Get people
    people_result = client.get_people()
    print("\nPeople result:")
    print(json.dumps(people_result, indent=4))
    
    # Get files
    files_result = client.get_files()
    print("\nFiles result:")
    print(json.dumps(files_result, indent=4))

if __name__ == "__main__":
    main()
