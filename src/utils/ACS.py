from pydantic import BaseModel, Field
from typing import Optional

# ============================================================================
# Pydantic Request Models (mirror your TypeScript interfaces)
# ============================================================================

class ACSData(BaseModel):
    ptageatnotification: Optional[int] = Field(None, ge=0, description="Patient age at notification")
    heartrate: Optional[float] = Field(None, ge=0, description="Heart rate (bpm)")
    canginapast2wk: Optional[int] = Field(None, ge=0, le=1, description="Angina past 2 weeks: 0=No, 1=Yes")
    killipclass: Optional[int] = Field(None, ge=1, le=4, description="Killip class I-IV")
    hdlc: Optional[float] = Field(None, ge=0, description="HDL Cholesterol (mg/dL)")
    ldlc: Optional[float] = Field(None, ge=0, description="LDL Cholesterol (mg/dL)")
    fbg: Optional[float] = Field(None, ge=0, description="Fasting blood glucose (mg/dL)")
    cabg: Optional[int] = Field(None, ge=0, le=1, description="CABG history: 0=No, 1=Yes")
    oralhypogly: Optional[int] = Field(None, ge=0, le=1, description="Oral hypoglycemic: 0=No, 1=Yes")
    antiarr: Optional[int] = Field(None, ge=0, le=1, description="Antiarrhythmic: 0=No, 1=Yes")
    ecgabnormlocationll: Optional[int] = Field(None, ge=0, le=1, description="ECG abnormality lower lead: 0=No, 1=Yes")
    cardiaccath: Optional[int] = Field(None, ge=0, le=1, description="Cardiac cath: 0=No, 1=Yes")
    statin: Optional[int] = Field(None, ge=0, le=1, description="Statin use: 0=No, 1=Yes")
    lipidla: Optional[int] = Field(None, ge=0, le=1, description="Lipid lowering agent: 0=No, 1=Yes")

    class Config:
        json_schema_extra = {
            "example": {
                "ptageatnotification": 68,
                "heartrate": 88,
                "canginapast2wk": 1,
                "killipclass": 2,
                "hdlc": 38,
                "ldlc": 140,
                "fbg": 110,
                "cabg": 0,
                "oralhypogly": 1,
                "antiarr": 0,
                "ecgabnormlocationll": 1,
                "cardiaccath": 0,
                "statin": 1,
                "lipidla": 1
            }
        }

def calculate_acs(data: ACSData) -> tuple[float, str]:
    """
    Placeholder ACS risk calculation.
    Replace with your validated GRACE / TIMI / custom ML model.
    """
    # Default values
    age = data.ptageatnotification or 60
    hr = data.heartrate or 70
    killip = data.killipclass or 1
    hdl = data.hdlc or 40
    ldl = data.ldlc or 100
    fbg = data.fbg or 100

    # ---- Placeholder heuristic ----
    score = 0.0

    # Age contribution
    score += min(age * 0.5, 30)

    # Heart rate
    if hr > 100:
        score += 10
    elif hr > 80:
        score += 5

    # Killip class
    score += (killip - 1) * 10

    # Lipids
    if ldl > 130:
        score += 5
    if hdl < 40:
        score += 5

    # Glucose
    if fbg > 126:
        score += 5

    # Binary flags
    flags = [
        data.canginapast2wk, data.cabg, data.oralhypogly,
        data.antiarr, data.ecgabnormlocationll,
        data.cardiaccath, data.statin, data.lipidla
    ]
    score += sum(f for f in flags if f) * 2

    # Normalize to 0-100
    # risk = min(score, 100)
    risk = score

    if risk < 108:
        category = "Low Risk"
    elif 109<= risk <= 140:
        category = "Intermediate Risk"
    else:
        category = "High Risk"

    return risk, category
