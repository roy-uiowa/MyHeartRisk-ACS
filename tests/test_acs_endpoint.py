import requests
import json

# Target URL
url = "http://localhost:8000/acs"  # Replace with your actual URL

# Headers
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# JSON payload
payload = {
    "ptageatnotification": 57,
    "heartrate": 120,
    "canginapast2wk": 1,
    "killipclass": 3,
    "hdlc": 1.0,
    "ldlc": 5.01,
    "fbg": 13.50,
    "cabg": 1,
    "oralhypogly": 1,
    "antiarr": 1,
    "ecgabnormlocationll": 1,
    "cardiaccath": 0,
    "statin": 1,
    "lipidla":1
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
    print(response.text)