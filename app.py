
from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel

app = FastAPI(
    title="Intrusion Detection API",
    docs_url="/docs",
    redoc_url="/redoc"
)

model = joblib.load("final_rf_model.pkl")
scaler = joblib.load("final_scaler.pkl")


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
    return {"message": "Intrusion Detection API Running"}


@app.post("/predict")
def predict(data: InputData):

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

    scaled = scaler.transform(input_data)
    prediction = model.predict(scaled)

    return {"prediction": int(prediction[0])}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
