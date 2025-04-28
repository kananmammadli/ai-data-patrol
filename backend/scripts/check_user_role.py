import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_user_role():
    # Use the token from the logs
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZmMxZjM3OS1jZmQ3LTRlNmItOTU5MS0yY2FhMmQ0M2M1NDUiLCJleHAiOjE3NDYzOTI3NzR9._6PPnJVVi3dr7u817T4W4QYEi8GSom7UaeAkb0fCXI0"

    # Make the request to get user info
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get('http://localhost:8000/api/v1/users/me', headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"User email: {user_data['email']}")
            print(f"User role: {user_data['role']}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error making request: {str(e)}")

if __name__ == "__main__":
    check_user_role() 