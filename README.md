# MyHeartRisk: ACS Prediction API

**Version:** 1.0.0  
**Description:** This API uses machine learning models to predict the risk of death for Acute Coronary Syndrome (ACS) patients based on clinical parameters, and provides risk explanations using LIME. This project was developed according to the standard of [ACS_2019](https://www.safetyandquality.gov.au/clinical-care-standards/acute-coronary-syndromes)
 

## Table of Contents
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Running the API](#running-the-api)
- [Docker Integration](#docker-integration)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

```
MyHeartRisk-ACS/
├── model/
│   ├── XGB_model.pkl         # XGBoost prediction model
│   └── LIME_XGB_model.pkl    # LIME explainer model
├── src/
|   ├── app/
|   │   └── server.py         # FastAPI server and routes
|   ├── utils/
|   │   ├── prediction.py         # Prediction logic
|   │   ├── LIME.py               # LIME explanation logic
|   │   └── FRS.py                # Framingham Risk Score logic 
├── notebooks/
│   └── EDA.ipynb    # Exploratory data analysis
├── data/
│   ├── advice.json              # List of Suggestion based on Patient Conditions
│   ├── tool_tip.json            # List of tips on how to use MyHeartRisk API
│   ├── X_test_stemi_state.pkl   # Test data for LIME
│   └── X_train_stemi_state.pkl  # Training data for LIME
├── Dockerfile                     # Docker instructions
├── requirements.txt               # Python dependencies
└── README.md                      # Documentation
```

## API Endpoints

### 1. Health Check
- **URL:** `/`
- **Method:** `GET`
- **Description:** Simple health check endpoint to confirm the API is running.
- **Response:**
  ```json
  {
    "message": "STEMI API Endpoint is Running"
  }
  ```

### 2. FRS Risk Prediction
- **URL:** `/frs`
- **Method:** `POST`
- **Description:** Predicts the Framingham Risk Score based on input features.
- **Request Body:** JSON object with features for FRS prediction.
- **Response:**
  ```json
  {
    "frs_prediction": FRS_risk_score
  }
  ```

### 3. ACS Risk Prediction
- **URL:** `/acs`
- **Method:** `POST`
- **Description:** Predicts ACS death risk and provides an explanation using LIME.
- **Request Body:** JSON object with features for ACS risk prediction.
- **Response:**
  ```json
  {
    "model_prediction": risk_prediction,
    "contribution_to_death": feature_contributions
  }
  ```

## Features
- Predict ACS risk using an XGBoost model.
- Explain predictions using LIME (Local Interpretable Model-agnostic Explanations).
- Calculate Framingham Risk Scores for patients.
- FastAPI server for efficient and scalable performance.

## Technologies Used
- **FastAPI:** Backend framework for building APIs.
- **XGBoost:** Machine learning model for risk prediction.
- **LIME:** Tool for explaining model predictions.
- **Docker:** Containerization for easier deployment.
- **Joblib:** For loading and saving models.
- **Pandas/Numpy:** For data manipulation and analysis.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/roy-uiowa/MyHeartRisk-ACS.git
cd MyHeartRisk-ACS
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Prepare the Models
Ensure the models (`XGB_model.pkl` and `LIME_XGB_model.pkl`) and training data (`X_train_stemi_state.pkl`) are in the `model/` and `data/` directories, respectively.

## Running the API

### Local Development
Run the FastAPI server locally:

```bash
uvicorn app.server:app --reload
```

The API will be available at: `http://127.0.0.1:8000/`

### Using Docker
You can build and run the API using Docker.

#### 1. Build the Docker Image
```bash
docker build -t your_dockerhub_username/acs-ai:latest .
```

#### 2. Run the Docker Container
```bash
docker run -p 8000:8000 your_dockerhub_username/acs-ai:latest
```

The API will be available at: `http://localhost:8000/`

## Docker Integration
This project includes a GitHub Actions workflow to automatically build and push the Docker image to Docker Hub on a new tag starting with `prod`.

### Docker Hub Workflow

1. Push a new tag to GitHub:
   ```bash
   git tag prod-<version>
   git push origin prod-<version>
   ```

2. The GitHub Actions workflow will trigger and build/push the image to Docker Hub.

## Contributing
Feel free to open an issue or submit a pull request for any improvements or new features.

## License
This project is licensed under the MIT License.

---

Make sure to replace `"yourusername"` and `"your_dockerhub_username"` with the appropriate values in the instructions. This README provides a comprehensive guide for users to understand, install, and run the MyHeartRisk API.