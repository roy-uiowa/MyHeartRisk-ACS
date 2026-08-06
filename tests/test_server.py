import sys
from unittest.mock import MagicMock, patch
from pathlib import Path

# =============================================================================
# STEP 1: Patch all heavy/IO operations BEFORE importing the app module
# =============================================================================
# This prevents actual model/data loading during test collection/import

_mock_model = MagicMock()
_mock_lime_model = MagicMock()
_mock_x_train = MagicMock()
_mock_x_train.columns.to_list.return_value = [
    "ptageatnotification", "canginapast2wk", "killipclass", "heartrate",
    "ldlc", "hdlc", "fbg", "ecgabnormlocationll", "cardiaccath", "cabg",
    "oralhypogly", "antiarr", "statin", "lipidla"
]

_patches = [
    patch("joblib.load", return_value=_mock_model),
    patch("pandas.read_pickle", return_value=_mock_x_train),
    patch("pathlib.Path", return_value=MagicMock()),
    patch("src.utils.prediction.predict_risk"),
    patch("src.utils.LIME.explain"),
    patch("src.utils.FRS.getFRSRisk"),
]

# Apply all patches
for p in _patches:
    p.start()

# Now safe to import the app
from fastapi.testclient import TestClient
import src.app.server as main  # your file name (adjust if different)

client = TestClient(main.app)

# Stop patches after import (we'll re-patch per-test as needed)
for p in _patches:
    p.stop()


# =============================================================================
# Fixtures & Helpers
# =============================================================================
import pytest

@pytest.fixture
def mock_predict_risk():
    with patch("main.predict_risk") as mock:
        yield mock

@pytest.fixture
def mock_explain():
    with patch("main.explain") as mock:
        yield mock

@pytest.fixture
def mock_get_frs():
    with patch("main.getFRSRisk") as mock:
        yield mock


# =============================================================================
# Tests
# =============================================================================

class TestHealthCheck:
    def test_root_returns_running_message(self):
        """GET / should return health status."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "STEMI API Endpint is Running"}


class TestFRSEndpoint:
    def test_frs_valid_payload(self, mock_get_frs):
        """POST /frs should accept valid FRS payload and return risk score."""
        mock_get_frs.return_value = {"frs_risk": 12.5}

        payload = {
            "age": 57,
            "hdlc": 1.0,
            "sex": 0,
            "tc": 2.5,
            "bpsys": 120.00,
            "bpsys_treatment": 1,
            "smoker": 0,
            "diabetes": 0
        }

        response = client.post("/frs", json=payload)
        assert response.status_code == 200
        assert response.json() == {"frs_risk": 12.5}
        mock_get_frs.assert_called_once_with(payload)

    def test_frs_missing_field(self):
        """POST /frs should handle missing fields gracefully (422 or custom)."""
        payload = {
            "age": 57,
            # missing hdlc, sex, etc.
        }
        response = client.post("/frs", json=payload)
        # FastAPI auto-validates dict schema; since no Pydantic model is used,
        # missing keys won't trigger 422. The function will just pass partial
        # dict to getFRSRisk. If you want strict validation, use a Pydantic model.
        assert response.status_code == 200  # or 422 if you add validation later

    def test_frs_empty_body(self):
        """POST /frs with empty body."""
        response = client.post("/frs", json={})
        assert response.status_code == 200
        mock_get_frs.assert_called_once_with({}  # patched in fixture if needed


class TestACSEndpoint:
    def test_acs_valid_payload(self, mock_predict_risk, mock_explain):
        """POST /acs should return prediction and LIME explanation."""
        mock_predict_risk.return_value = {
            "prediction": "death",
            "probability": 0.85
        }
        mock_explain.return_value = [
            {"feature": "killipclass", "contribution": 0.34, "advice": "Monitor closely"}
        ]

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
            "lipidla": 1
        }

        response = client.post("/acs", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert "model_prediction" in data
        assert "contribution_to_death" in data
        assert data["model_prediction"]["prediction"] == "death"
        assert data["contribution_to_death"][0]["feature"] == "killipclass"

        # Verify LIME data subset is passed correctly
        expected_lime_data = {
            "ptageatnotification": 57,
            "canginapast2wk": 1,
            "killipclass": 3,
            "heartrate": 120,
            "ldlc": 5.01,
            "hdlc": 1.0,
            "fbg": 13.50,
            "ecgabnormlocationll": 1,
            "cardiaccath": 0,
            "cabg": 1,
            "oralhypogly": 1,
            "antiarr": 1,
            "statin": 1,
            "lipidla": 1
        }
        mock_explain.assert_called_once()
        call_args = mock_explain.call_args[0]
        assert call_args[0] == expected_lime_data

    def test_acs_extra_fields_ignored(self, mock_predict_risk, mock_explain):
        """Extra fields in payload should be ignored or not break the endpoint."""
        mock_predict_risk.return_value = {"prediction": "alive", "probability": 0.2}
        mock_explain.return_value = []

        payload = {
            "ptageatnotification": 40,
            "heartrate": 80,
            "canginapast2wk": 0,
            "killipclass": 1,
            "hdlc": 1.2,
            "ldlc": 2.0,
            "fbg": 5.0,
            "cabg": 0,
            "oralhypogly": 0,
            "antiarr": 0,
            "ecgabnormlocationll": 0,
            "cardiaccath": 0,
            "statin": 0,
            "lipidla": 0,
            "extra_field": "should_be_ignored"
        }

        response = client.post("/acs", json=payload)
        assert response.status_code == 200

    def test_acs_missing_lime_field(self, mock_predict_risk, mock_explain):
        """If a required LIME field is missing, the endpoint should raise KeyError (or handle gracefully)."""
        payload = {
            "ptageatnotification": 57,
            "heartrate": 120,
            # missing other fields
        }

        # Since the endpoint directly accesses data["canginapast2wk"], this will KeyError
        response = client.post("/acs", json=payload)
        assert response.status_code == 500  # Currently no error handling


class TestCORS:
    def test_cors_headers_present(self):
        """Ensure CORS middleware allows cross-origin requests."""
        response = client.options(
            "/",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers


# =============================================================================
# Optional: Test the utility functions in isolation
# =============================================================================
class TestUtils:
    @patch("src.utils.prediction.joblib.load")  # adjust imports as needed
    def test_predict_risk_logic(self, mock_load):
        """Test predict_risk if you want to test logic without FastAPI."""
        # Example structure - adjust based on actual implementation
        pass