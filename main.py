
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

model = joblib.load("final_rf_model.pkl")
scaler = joblib.load("final_scaler.pkl")

app = FastAPI(title="Intrusion Detection API")

class InputData(BaseModel):
    network_packet_size: float
    protocol_type: int
    login_attempts: int
    session_duration: float
    encryption_used: int
    ip_reputation_score: float
    failed_logins: int
    browser_type: int
    unusual_time_access: int

@app.get("/")
def home():
    return {"message": "IDS API is running"}

@app.post("/predict")
def predict(data: InputData):

    features = np.array([[  
        data.network_packet_size,
        data.protocol_type,
        data.login_attempts,
        data.session_duration,
        data.encryption_used,
        data.ip_reputation_score,
        data.failed_logins,
        data.browser_type,
        data.unusual_time_access
    ]])

    features = scaler.transform(features)

    result = model.predict(features)[0]

    if result == 1:
        return {"prediction": "⚠️ Attack Detected"}
    else:
        return {"prediction": "✅ Normal Activity"}
