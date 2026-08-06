
# Loading Requirements
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import joblib
from lime.lime_tabular import LimeTabularExplainer
import sklearn 
import xgboost
import json
from pathlib import Path 

# load functions from utils
from src.utils.prediction import predict_risk
from src.utils.LIME import explain
from src.utils.FRS import getFRSRisk
from src.utils.ACS import calculate_acs, ACSData
SEED = 42


####### Settings #######
# Loading Models 
model = joblib.load(Path('model/XGB_model.pkl'))
lime_model = joblib.load('model/LIME_XGB_model.pkl')
class_names = ['alive', 'death']
X_train = pd.read_pickle('data/X_train_stemi_state.pkl')
feature_names = X_train.columns.to_list()

####### LIME Setup #######
# Only build once, saving computational power and time

# Create LIME explainer
explainer = LimeTabularExplainer(
    training_data=X_train.values,
    feature_names=feature_names,
    class_names=['alive', 'death'],  # Adjust based on your classes
    mode='classification',
)


###### Fast API #######
app = FastAPI(
    title="MyHeartRisk: ACS Prediction API",
    description="Using ACS Model 2019",
    version="1.0.0",
)

# allow all origin
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###### Endpoints #######
# Health Check
@app.get('/', summary='Health Check')
def root():
    """
    Health Check Endpoint
    """
    return {'message': "STEMI API Endpint is Running"}



# FRS Endpoint
@app.post('/frs',summary="Get FRS Risk")
def predict(data:dict):
    """
    Predicts the FRS for a given input.

    **body**: A JSON object containing the following features:\n
        Framingham Risk Scores
        •⁠ age:                 Patient's Age (30 - 100)
        •⁠ hdlc:                HDL Cholesterol, (0.1 - 2.5 (mmol/l))
        •⁠ sex:                 Patient's Sex (0 (men), 1 (women))
        •⁠ tc:                  Total Cholesterol (0.1 - 8 (mmol/L))
        •⁠ bpsys:               Systolic Blood Pressure (0.1-8(mmol/L))
        •⁠ bpsys_treatment:     Treament for Hypertension (0 (not treated), 1 (treated))
        •⁠ smoker:              Current Smoker (0 (no), 1 (yes))
        •⁠ diabetes:            Diabetes (0 (no), 1 (yes))

     Request JSON Examples:
    {
        "age": 57,
        "hdlc": 1.0,
        "sex": 0,
        "tc": 2.5,
        "bpsys": 120.00,
        "bpsys_treatment": 1,
        "smoker": 0,
        "diabetes": 0
    }

    Returns:
    - FRS risk score
    """
        

    frs_prediction = getFRSRisk(data)
    result = frs_prediction

    return result


# ACS Endpoint
@app.post('/acs',summary="Predict Risk Probability and Explanation")
def predict_acs(data:ACSData):
    """
    Predicts the class and probability for a given input.

    **body**: A JSON object containing the following features:\n
        •⁠ ptageatnotification: Patient's age at notification (30 - 100),
        •⁠ heartrate:           Heart Rate (30-200 bpm),
        •⁠ canginapast2wk:      Chronic Angina (Past 2 weeks) (0 (no), 1 (yes)),
        •⁠ killipclass:         Killip Class (1 - 4),
        •⁠ hdlc:                HDL Cholesterol, (0.1 - 2.5 (mmol/l))
        •⁠ ldlc:                LDL Cholesterol (0.1 - 7 (mmol/l),
        •⁠ fbg:                 Fasting Blood glucose ,
        •⁠ cabg:                Coronary Artery Bypass Graft (0 (no), 1 (yes)),
        •⁠ oralhypogly":        Oral hypoglycemic agent (0 (no), 1 (yes)),
        •⁠ antiarr:             Anti-arrhythmic agent (0 (no), 1 (yes)),
        •⁠ ecgabnormlocationll: ST-segment elevation ≥ 1mm (in ≥ 2 contiguous limb leads) (0 (no), 1 (yes)),
        •⁠ cardiaccath:         Cardiac catheterization (0 (no), 1 (yes)),
        •⁠ statin:              Statin (0 (no), 1 (yes)),
        •⁠ lipidla:             Lipid Lowering Agent (0 (no), 1 (yes))

     Request JSON Examples:
    {
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

    Returns:
    - `model_prediction`: ACS Risk prediciton.
    - `contribution_to_death`: Features and their contributions to death with advice.
    """

    lime_data={
        "ptageatnotification": data.ptageatnotification,
        "canginapast2wk": data.canginapast2wk,
        "killipclass": data.killipclass,
        "heartrate": data.heartrate,
        "ldlc": data.ldlc,
        "hdlc": data.hdlc,
        "fbg": data.fbg,
        "ecgabnormlocationll": data.ecgabnormlocationll,
        "cardiaccath": data.cardiaccath,
        "cabg": data.cabg,
        "oralhypogly": data.oralhypogly,
        "antiarr": data.antiarr,
        "statin": data.statin,
        "lipidla": data.lipidla
    }


        

    model_prediction = predict_risk(lime_data, lime_model, class_names)
    model_prediction['GRACE_risk_score'], model_prediction['category'] = calculate_acs(data)
    contribution_to_death = explain(lime_data, explainer, lime_model)
    result = {
        'model_prediction': model_prediction,
        'contribution_to_death': contribution_to_death,
    }

    return result