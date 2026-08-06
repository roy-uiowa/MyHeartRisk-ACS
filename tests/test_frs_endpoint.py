import requests
import json

# Target URL
url = "http://localhost:8000/frs"  # Replace with your actual URL

# Headers
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# JSON payload
payload = {
    "age": 57,
    "hdlc": 1.0,
    "sex": 0,
    "tc": 2.5,
    "bpsys": 120.0,
    "bpsys_treatment": 1,
    "smoker": 0,
    "diabetes": 0
}

try:
    # Send POST request
    response = requests.post(url, headers=headers, json=payload, timeout=10)

    # Raise an error for bad HTTP status codes
    response.raise_for_status()

    # Try to parse JSON response
    try:
        data = response.json()
        print("Response JSON:", json.dumps(data, indent=2))
    except ValueError:
        print("Response Text:", response.text)

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")