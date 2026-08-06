import requests
import pytest

BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

@pytest.mark.parametrize("payload,expected_probability,expected_category", [
    (
        {"age": 57, "hdlc": 1.0, "sex": 0, "tc": 2.5, "bpsys": 120.0, "bpsys_treatment": 1, "smoker": 0, "diabetes": 0},
        "15.6%",
        "Intermediate Risk"
    ),
    # Add more test cases here
])
def test_frs_scenarios(payload, expected_probability, expected_category):
    response = requests.post(f"{BASE_URL}/frs", headers=HEADERS, json=payload, timeout=10)
    
    assert response.status_code == 200
    data = response.json()
    assert data["probability"] == expected_probability
    assert data["risk_category"] == expected_category
    # print("✅ FRS endpoint test passed")


@pytest.mark.parametrize("payload,expected_probability,expected_result", [
    (
        {"ptageatnotification": 57, "heartrate": 120, "canginapast2wk": 1, 
         "killipclass": 3, "hdlc": 1.0, "ldlc": 5.01, "fbg": 13.50, "cabg": 1, "oralhypogly": 1, 
         "antiarr": 1, "ecgabnormlocationll": 1, "cardiaccath": 0, "statin": 1, "lipidla":1},
         
         0.261,
         "alive"
    ),
    # Add more test cases here
])

def test_acs_scenarios(payload, expected_probability, expected_result):
    response = requests.post(f"{BASE_URL}/acs", headers=HEADERS, json=payload, timeout=10)
    
    assert response.status_code == 200
    data = response.json()
    assert data["model_prediction"]["probability"] == expected_probability
    assert data["model_prediction"]["result"] == expected_result
    # print("✅ ACS endpoint test passed")
