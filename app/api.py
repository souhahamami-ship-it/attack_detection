from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Anomaly Detection API")

scaler = joblib.load("artifacts/scaler.pkl")
attack_le = joblib.load("artifacts/attack_label_encoder.pkl")
model = joblib.load("artifacts/xgb_model.pkl")


class InputData(BaseModel):
    duration: float
    protocol_type: int
    service: int
    flag: int
    src_bytes: float
    dst_bytes: float
    logged_in: int
    num_failed_logins: int
    count: float
    srv_count: float
    serror_rate: float
    rerror_rate: float
    num_compromised: float
    num_root: float
    num_file_creations: float
    num_shells: float
    num_access_files: float
    hot: float


@app.get("/")
def home():
    return {"message": "API running 🚀"}


@app.post("/predict")
def predict(data: InputData):
    features = np.array([[*data.dict().values()]])
    features_scaled = scaler.transform(features)

    pred = model.predict(features_scaled)[0]
    label = attack_le.classes_[pred]

    return {"prediction": label}