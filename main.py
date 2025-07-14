from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Add this import
from pydantic import BaseModel
import numpy as np
import pickle
import os

# ------------------------------
# Load the Random Forest model
# ------------------------------
MODEL_PATH = "rf_model.pkl"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found. Please place it in the same directory.")

with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)

# ------------------------------
# SRQ-20 Features List
# ------------------------------
FEATURES = [
    'headache', 'appetite', 'sleep', 'fear', 'shaking', 'nervous', 'digestion',
    'troubled', 'unhappy', 'cry', 'enjoyment', 'decisions', 'work', 'play',
    'interest', 'worthless', 'suicide', 'tiredness', 'uncomfortable', 'easily_tired'
]

# ------------------------------
# Request Body Schema
# ------------------------------
class SRQ20Input(BaseModel):
    headache: int
    appetite: int
    sleep: int
    fear: int
    shaking: int
    nervous: int
    digestion: int
    troubled: int
    unhappy: int
    cry: int
    enjoyment: int
    decisions: int
    work: int
    play: int
    interest: int
    worthless: int
    suicide: int
    tiredness: int
    uncomfortable: int
    easily_tired: int

# ------------------------------
# FastAPI App
# ------------------------------
app = FastAPI(title="SRQ-20 Depression Detection API", version="1.0")

# Add CORS middleware here - right after creating the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the SRQ-20 Depression Detection API. Use /predict to get a prediction."
    }

@app.post("/predict")
def predict_depression(data: SRQ20Input):
    try:
        # Prepare input for the model
        input_data = np.array([getattr(data, feature) for feature in FEATURES]).reshape(1, -1)

        # Predict class and probabilities
        prediction = model.predict(input_data)[0]
        proba = model.predict_proba(input_data)[0]
        
        # Get predicted class and confidence
        predicted_class = "Depressed" if prediction == 1 else "Not Depressed"
        confidence = float(proba[prediction])  # confidence for the predicted class

        # Apply threshold logic to determine final class
        final_class = apply_threshold_logic(predicted_class, confidence)

        return {
            "prediction": int(prediction),
            "predicted_class": predicted_class,
            "confidence": round(confidence, 4),
            "final_class": final_class
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------
# Threshold Logic Function
# ------------------------------
def apply_threshold_logic(predicted_class: str, confidence: float) -> str:
    if predicted_class == "Depressed":
        if confidence >= 0.85:
            return "Severe Depression"
        elif 0.70 <= confidence < 0.85:
            return "Moderate Depression"
        elif 0.55 <= confidence < 0.70:
            return "Mild Depression"
        else:
            return "No Depression"
    else:  # predicted_class == "Not Depressed"
        if confidence >= 0.85:
            return "No Depression"
        elif 0.70 <= confidence < 0.85:
            return "Mild Depression"
        elif 0.55 <= confidence < 0.70:
            return "Moderate Depression"
        else:
            return "Severe Depression"