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
    username = os.getenv("ONLYOFFICE_USERNAME")
    password = os.getenv("ONLYOFFICE_PASSWORD")
    auth_code = os.getenv("ONLYOFFICE_AUTH_CODE")  # Optional
    auth_token = os.getenv("ONLYOFFICE_AUTH_TOKEN")  # Optional
    verify_ssl = os.getenv("VERIFY_SSL", "True").lower() == "true"
    
    if not portal_url or not username or not password:
        print("Please set ONLYOFFICE_PORTAL_URL, ONLYOFFICE_USERNAME, and ONLYOFFICE_PASSWORD in your .env file")
        return
    
    # Initialize the client
    client = OnlyOfficeClient(portal_url, verify_ssl=verify_ssl, auth_token=auth_token)
    
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
    
    # Get projects
#    print("\nRetrieving my projects...")
#    projects_result = client.get_projects()
#    print("Projects result:")
#    print(json.dumps(projects_result, indent=4))

    # Get tasks
    print("\nRetrieving my tasks...")
    tasks_result = client.get_project_tasks(project_id=220, statuses=["open", "closed"])
    print("Tasks result:")
    print(json.dumps(tasks_result, indent=4))

    output_file = "tasks_result.json"
    with open(output_file, "w") as f:
        json.dump(tasks_result, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
