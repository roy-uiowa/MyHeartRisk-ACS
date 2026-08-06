import pandas as pd
import warnings
import json
import re

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


def explain(data: dict, explainer, lime_model):

    with open('data/advice.json', 'r') as f:
        advice_json = json.load(f)
    
    # Choose an instance to explain
    instance = pd.Series(data)

    # Explain the prediction
    explanation = explainer.explain_instance(
        data_row=instance,
        predict_fn=lime_model.predict_proba
    )

    # Get the explanation for each feature
    lime_explanation = explanation.as_list()

    # Result JSON 
    instance_explanation = []


    for feature, contribution in lime_explanation:
        impact = "positive" if contribution >= 0 else 'negative'

        # Get feature name from the feature by lime
        # Regex to find letters
        letters = re.findall(r'[a-zA-Z]+', feature)

        # Join the found letters into a single string
        feature_name = ''.join(letters)

        # If result is bad, provide advice
        if impact == "positive":
            for feature_item, details in advice_json.items():
                if feature_item == feature_name:
                    advice = details['advice_en']
        else:
            advice = []   
        
        # Combine and return result
        instance_explanation.append({
            "feature": feature,
            "contribution": round(contribution, 3),
            "impact": impact,
            "advice": advice
        })

    return instance_explanation