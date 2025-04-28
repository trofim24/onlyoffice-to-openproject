# example.py
from onlyoffice_api_client import OnlyOfficeClient
import json
import os
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get credentials from environment variables
    portal_url = os.getenv("ONLYOFFICE_PORTAL_URL", "https://yourportal.onlyoffice.com")
    username = os.getenv("ONLYOFFICE_USERNAME", "string")
    password = os.getenv("ONLYOFFICE_PASSWORD", "string")
    auth_code = os.getenv("ONLYOFFICE_AUTH_CODE")  # Optional
    verify_ssl = os.getenv("VERIFY_SSL", "True").lower() == "true"
    
    if not portal_url or not username or not password:
        print("Please set ONLYOFFICE_PORTAL_URL, ONLYOFFICE_USERNAME, and ONLYOFFICE_PASSWORD in your .env file")
        return
    
    # Initialize the client
    client = OnlyOfficeClient(portal_url, verify_ssl=verify_ssl)
    
    # Authenticate
    auth_result = client.authenticate(
        username=username,
        password=password,
        code=auth_code
    )
    
    print("Authentication result:")
    print(json.dumps(auth_result, indent=4))
    
    if "error" in auth_result and auth_result["error"]:
        print("Authentication failed")
        print(f"Status code: {auth_result.get('status_code')}")
        print(f"Error message: {auth_result.get('message')}")
        return
    
    # Only continue if authentication was successful
    print("\nAuthentication successful!")
    
    # Example of further API calls you could make:
    
    # Get people
    print("\nRetrieving people...")
    people_result = client.get_people()
    print("People result:")
    print(json.dumps(people_result, indent=4))
    
    # Get files
    print("\nRetrieving files...")
    files_result = client.get_files()
    print("Files result:")
    print(json.dumps(files_result, indent=4))


if __name__ == "__main__":
    main()
