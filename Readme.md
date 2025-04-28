# ONLYOFFICE API Client

A Python client library for interacting with the ONLYOFFICE API.

## Features

- Easy authentication with the ONLYOFFICE API
- Token management for authenticated requests
- Methods to interact with common ONLYOFFICE APIs
- Simple and intuitive interface

## Installation

```bash
pip install onlyoffice-api-client
```

Or directly from the repository:

```bash
git clone https://github.com/yourusername/onlyoffice-api-client.git
cd onlyoffice-api-client
pip install -e .
```

## Usage

### Basic Authentication

```python
from onlyoffice_api_client import OnlyOfficeClient

# Initialize the client
client = OnlyOfficeClient("https://yourportal.onlyoffice.com")

# Authenticate
result = client.authenticate("yourusername", "yourpassword")
print(result)
```

### Environment Variables

For security, you can use environment variables:

```python
import os
from dotenv import load_dotenv
from onlyoffice_api_client import OnlyOfficeClient

# Load environment variables
load_dotenv()

# Get credentials from environment variables
portal_url = os.getenv("ONLYOFFICE_PORTAL_URL")
username = os.getenv("ONLYOFFICE_USERNAME")
password = os.getenv("ONLYOFFICE_PASSWORD")

# Initialize and authenticate
client = OnlyOfficeClient(portal_url)
client.authenticate(username, password)
```

### Using the Authentication Class Directly

```python
from onlyoffice_api_client import OnlyOfficeAuth

# Initialize the auth client
auth = OnlyOfficeAuth("https://yourportal.onlyoffice.com")

# Login
result = auth.login("yourusername", "yourpassword")
print(result)

# Get the token
token = auth.get_token()
print(f"Token: {token}")

# Logout
logout_result = auth.logout()
print(logout_result)
```

### Getting People and Files

```python
from onlyoffice_api_client import OnlyOfficeClient

client = OnlyOfficeClient("https://yourportal.onlyoffice.com")
client.authenticate("yourusername", "yourpassword")

# Get people
people = client.get_people()
print(people)

# Get files from root folder
files = client.get_files()
print(files)

# Get files from a specific folder
folder_id = "123"
folder_files = client.get_files(folder_id)
print(folder_files)
```

## Project Structure

```
onlyoffice-api-client/
├── onlyoffice_api_client/
│   ├── __init__.py
│   ├── auth.py
│   └── client.py
├── example.py
├── setup.py
├── README.md
├── .gitignore
└── .env.example
```

## Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install development dependencies: `pip install -e ".[dev]"`
5. Copy `.env.example` to `.env` and fill in your ONLYOFFICE credentials

## License

MIT