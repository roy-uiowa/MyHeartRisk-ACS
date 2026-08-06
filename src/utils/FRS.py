# This file contains the Framingham Risk Score (FRS) calculation and return the risk probability result
# Source:
# https://ccs.ca/app/uploads/2020/12/FRS_eng_2017_fnl1.pdf
# https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.107.699579#FD1

# Input Parameters
# sex = 'men', 'women'
# age = integer, 30 - Inf
# hdlc = float, 0 - 2.5 (mmol/l)
# tc = float, 0 - 8 (mmol/L)
# sbp = integer, 90-200 (mmHg)
# sbp_treatment = 0 (not treated), 1 (treated)
# smoker = 0 (no), 1 (yes)
# diabetes = 0 (no), 1 (yes)


# Import Library
import numpy as np

# Scoring for FRS
# Variables Needed: sex,age, hdlc(mmol/l), total cholesterol, systolic BP(mmHg), tratment of hypertension, smoker, diabetes

# Age Scores 
age_map = {
    "30-34": {"men": 0, "women": 0},
    "35-39": {"men": 2, "women": 2},
    "40-44": {"men": 5, "women": 4},
    "45-49": {"men": 6, "women": 5},
    "50-54": {"men": 8, "women": 7},
    "55-59": {"men": 10, "women": 8},
    "60-64": {"men": 11, "women": 9},
    "65-69": {"men": 12, "women": 10},
    "70-74": {"men": 14, "women": 11},
    ">75": {"men": 15, "women": 12}
}
def get_age_group(age):
    for age_range in age_map:
        if '-' in age_range:
            min_age, max_age = map(int, age_range.split('-'))
            if min_age <= age <= max_age:
                return age_range
        elif age_range.startswith('>') and age > int(age_range[1:]):
            return age_range
    return None  



# HDLC Scores
hdlc_map = {
        ">1.6": {"men": -2, "women": -2},
        "1.3-1.6": {"men": -1, "women": -1},
        "1.2-1.29": {"men": 0, "women": 0},
        "0.9-1.19": {"men": 1, "women": 1},
        "<0.9": {"men": 2, "women": 2}
}
def get_hdlc_group(hdlc):
    for hdlc_range in hdlc_map:
        if '-' in hdlc_range:
            min_hdlc, max_hdlc = map(float, hdlc_range.split('-'))
            if min_hdlc <= hdlc <= max_hdlc:
                return hdlc_range
        elif hdlc_range.startswith('>') and hdlc > float(hdlc_range[1:]):
            return hdlc_range
        elif hdlc_range.startswith('<') and hdlc < float(hdlc_range[1:]):
            return hdlc_range
    return None  


# Total Cholesterol Score
tc_map = {
        "<4.1": {"men": 0, "women": 0},
        "4.1-5.19": {"men": 1, "women": 1},
        "5.2-6.19": {"men": 2, "women": 3},
        "6.2-7.2": {"men": 3, "women": 4},
        ">7.2": {"men": 4, "women": 5}
    }
def get_tc_group(tc):
    for tc_range in tc_map:
        if '-' in tc_range:
            min_tc, max_tc = map(float, tc_range.split('-'))
            if min_tc <= tc <= max_tc:
                return tc_range
        elif tc_range.startswith('>') and tc > float(tc_range[1:]):
            return tc_range
        elif tc_range.startswith('<') and tc < float(tc_range[1:]):
            return tc_range
    return None  


# Systolic Blood Pressure Score
systolic_bp_map = {
        # 0 for not treated, 1 for treated
        "men": {
            "<120": {0: -2, 1: 0},
            "120-129": {0: 0, 1: 2},
            "130-139": {0: 1, 1: 3},
            "140-159": {0: 2, 1: 4},
            ">160": {0: 3, 1: 5}
        },
        "women": {
            "<120": {0: -3, 1: -1},
            "120-129": {0: 0, 1: 2},
            "130-139": {0: 1, 1: 3},
            "140-149": {0: 2, 1: 5},
            "150-159": {0: 4, 1: 6},
            ">160": {0: 5, 1: 7}
        }
}
def get_sbp_group(sex, sbp):
    if sex not in systolic_bp_map:
        return None
    
    for sbp_range in systolic_bp_map[sex]:
        if '-' in sbp_range:
            min_sbp, max_sbp = map(float, sbp_range.split('-'))
            if min_sbp <= sbp <= max_sbp:
                return sbp_range
        elif sbp_range.startswith('>') and sbp > float(sbp_range[1:]):
            return sbp_range
        elif sbp_range.startswith('<') and sbp < float(sbp_range[1:]):
            return sbp_range
    return None 


# Smoker Score
smoker_map = {
    0: {"men":0,"women":0},
    1: {"men":4,"women":3},
}

# Diabetes Score
diabetes_map = {
    0: {"men":0,"women":0},
    1: {"men":3,"women":4},
}


# FRS Score and Risk Probability
men_score_risk = {
    "<-2": {
        "probability":"<1%", 
        "risk_category":"Low Risk", 
        },
    "-2": {
        "probability":"1.1%", 
        "risk_category":"Low Risk", 
        },
    "-1": {
        "probability":"1.4%", 
        "risk_category":"Low Risk", 
        },
    "0":{
        "probability":"1.6%", 
        "risk_category":"Low Risk", 
        },
    "1": {
        "probability":"1.9%", 
        "risk_category":"Low Risk", 
        },
    "2": {
        "probability":"2.3%", 
        "risk_category":"Low Risk", 
        },
    "3": {
        "probability":"2.8%", 
        "risk_category":"Low Risk", 
        },
    "4": {
        "probability":"3.3%", 
        "risk_category":"Low Risk", 
        },
    "5": {
        "probability":"3.9%", 
        "risk_category":"Low Risk", 
        },
    "6": {
        "probability":"4.7%", 
        "risk_category":"Low Risk", 
        },
    "7": {
        "probability":"5.6%", 
        "risk_category":"Low Risk", 
        },
    "8":{
        "probability":"6.7%", 
        "risk_category":"Low Risk", 
        },
    "9":{
        "probability":"7.9%", 
        "risk_category":"Low Risk", 
        },
    "10": {
        "probability":"9.4%", 
        "risk_category":"Low Risk", 
        },
    "11":{
        "probability":"11.2%", 
        "risk_category":"Intermediate Risk", 
        },
    "12": {
        "probability":"13.2%", 
        "risk_category":"Intermediate Risk", 
        },
    "13": {
        "probability":"15.6%", 
        "risk_category":"Intermediate Risk", 
        },
    "14": {
        "probability":"18.4%", 
        "risk_category":"Intermediate Risk", 
        },
    "15":{
        "probability":"21.6%", 
        "risk_category":"High Risk", 
        },
    "16": {
        "probability":"25.3%", 
        "risk_category":"High Risk", 
        },
    "17": {
        "probability":"29.4%", 
        "risk_category":"High Risk", 
        },
    ">18": {
        "probability":">30%", 
        "risk_category":"High Risk", 
        }
}
def get_men_score_group(score):
    for score_range in men_score_risk:
        # Handle "less than" range, e.g., "<-2"
        if score_range.startswith('<'):
            if score < int(score_range[1:]):  # Convert the part after '<' to an integer
                return score_range
        
        # Handle "greater than" range, e.g., ">18"
        elif score_range.startswith('>'):
            if score > int(score_range[1:]):  # Convert the part after '>' to an integer
                return score_range
        
        # Handle exact matches for numeric keys (e.g., "-2", "0", "5", etc.)
        elif score == int(score_range):
                return score_range
    return None  


women_score_risk = {
    "<-2": {
        "probability":"<1%", 
        "risk_category":"Low Risk", 
        },
    "-1": {
        "probability":"1%", 
        "risk_category":"Low Risk", 
        },
    "0": {
        "probability":"1.2%", 
        "risk_category":"Low Risk", 
        },
    "1": {
        "probability":"1.5%", 
        "risk_category":"Low Risk", 
        },
    "2": {
        "probability":"1.7%", 
        "risk_category":"Low Risk", 
        },
    "3": {
        "probability":"2.0%", 
        "risk_category":"Low Risk", 
        },
    "4": {
        "probability":"2.4%", 
        "risk_category":"Low Risk", 
        },
    "5": {
        "probability":"2.8%", 
        "risk_category":"Low Risk", 
        },
    "6": {
        "probability":"3.3%", 
        "risk_category":"Low Risk", 
        },
    "7": {
        "probability":"3.9%", 
        "risk_category":"Low Risk", 
        },
    "8": {
        "probability":"4.5%", 
        "risk_category":"Low Risk", 
        },
    "9": {
        "probability":"5.3%", 
        "risk_category":"Low Risk", 
        },
    "10": {
        "probability":"6.3%", 
        "risk_category":"Low Risk", 
        },
    "11": {
        "probability":"7.3%", 
        "risk_category":"Low Risk", 
        },
    "12":{
        "probability":"8.6%", 
        "risk_category":"Low Risk", 
        },
    "13":{
        "probability":"10.0%", 
        "risk_category":"Intermediate Risk", 
        },
    "14": {
        "probability":"11.7%", 
        "risk_category":"Intermediate Risk", 
        },
    "15":{
        "probability":"13.7%", 
        "risk_category":"Intermediate Risk", 
        },
    "16": {
        "probability":"15.9%", 
        "risk_category":"Intermediate Risk", 
        },
    "17": {
        "probability":"18.5%", 
        "risk_category":"Intermediate Risk", 
        },
    "18": {
        "probability":"21.5%", 
        "risk_category":"High Risk", 
        },
    "19":{
        "probability":"24.8%", 
        "risk_category":"High Risk", 
        },
    "20": {
        "probability":"28.0%", 
        "risk_category":"High Risk", 
        },
    ">20": {
        "probability":">30.0%", 
        "risk_category":"High Risk", 
        },
}

def get_women_score_group(score):
    for score_range in women_score_risk:
        # Handle "less than" range, e.g., "<-2"
        if score_range.startswith('<'):
            if score < int(score_range[1:]):  # Convert the part after '<' to an integer
                return score_range
        
        # Handle "greater than" range, e.g., ">18"
        elif score_range.startswith('>'):
            if score > int(score_range[1:]):  # Convert the part after '>' to an integer
                return score_range
        
        # Handle exact matches for numeric keys (e.g., "-2", "0", "5", etc.)
        elif score == int(score_range):
                return score_range
    return None  


# Risk Calculation Function
def getFRSRisk(data:dict):

    # Extract value
    age =  round(data['age'])
    sex =  'men' if data['sex'] == 0 else 'women'
    hdlc =  data['hdlc']
    tc =  data['tc']
    sbp =  data['bpsys']
    sbp_treatment =  data['bpsys_treatment']
    smoker =  data['smoker']
    diabetes =  data['diabetes']

    # Intialize points
    points = 0

    # Get score from age
    age_group = get_age_group(age)
    points += age_map[age_group][sex]

    # Get score from hldc
    hdlc_group = get_hdlc_group(hdlc)
    points += hdlc_map[hdlc_group][sex]

    # Get score from tc
    tc_group = get_tc_group(tc)
    points += tc_map[tc_group][sex]

    # Get score form sbp
    sbp_group = get_sbp_group(sex,sbp)
    points += systolic_bp_map[sex][sbp_group][sbp_treatment]

    # Get score from smoker
    points += smoker_map[smoker][sex]

    # Get score from diabetes
    points += diabetes_map[diabetes][sex]

    # Get Result
    if sex == 'men':
        score_group = get_men_score_group(points)
        result = men_score_risk[score_group]
    elif sex =='women':
        score_group = get_women_score_group(points)
        result = women_score_risk[score_group]

    return result



