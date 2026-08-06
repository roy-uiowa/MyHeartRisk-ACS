import pandas as pd
import numpy as np

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
    }