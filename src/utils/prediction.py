import pandas as pd
import numpy as np

def categorizedRisk(probability):
        if probability < 0.35:
                category = "Low Risk"
        elif 0.36<= probability <= 0.65:
                category = "Intermediate Risk"
        else:
                category = "High Risk"
        return category

# Predict Function
def predict_risk(data: dict,model, class_names: list):
    # Default Threshold
    threshold = 0.5
    
    # Class Prediction
    df = pd.DataFrame([data])
    prediction = model.predict(df)

    # Convert to class name
    index = int(np.ravel(prediction)[0])
    result = class_names[index]


    # Predict Probability
    probability = model.predict_proba(df)[:, 1]
    formatted_probability = np.round(float(probability[0]), 3)

    # Return result
    return {
            # 'threshold': threshold,
            'result': result,
            'probability': formatted_probability,
            'category': categorizedRisk(formatted_probability)
    }