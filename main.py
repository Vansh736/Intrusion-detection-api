
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

# Create FastAPI app
app = FastAPI(title="Intrusion Detection API")

# Get current directory path (important for cloud)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model and scaler safely
model_path = os.path.join(BASE_DIR, "final_rf_model.pkl")
scaler_path = os.path.join(BASE_DIR, "final_scaler.pkl")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)


# Input Data Model
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


# Home Route
@app.get("/")
def home():
    return {"message": "IDS API is running"}


# Prediction Route
@app.post("/predict")
def predict(data: InputData):

    # Convert input to numpy array
    input_data = np.array([[
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

    # Scale data
    scaled_data = scaler.transform(input_data)

    # Make prediction
    prediction = model.predict(scaled_data)

    # Result
    result = "Intrusion Detected" if prediction[0] == 1 else "Normal Traffic"

    return {
        "prediction": int(prediction[0]),
        "result": result
    }
