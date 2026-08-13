"""
Day 7 - Student Performance Prediction API
Remote Internship Task

This is a simple FastAPI app that loads our trained Logistic Regression
model (from Day 4-6) and exposes it through a POST /predict endpoint.

Run this with:
    uvicorn main:app --reload

Then visit http://127.0.0.1:8000/docs to see the interactive API docs,
or test it directly with Postman.
"""

import os
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Load the trained model, scaler, and feature order once,
# when the app starts (not on every request - that would be slow)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")

model = joblib.load(os.path.join(MODEL_DIR, "logistic_regression_model.joblib"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.joblib"))
feature_order = joblib.load(os.path.join(MODEL_DIR, "feature_order.joblib"))

app = FastAPI(
    title="Student Performance Prediction API",
    description="Predicts whether a student will Pass or Fail, based on attendance and scores.",
    version="1.0.0"
)


# ---------------------------------------------------------
# Define the shape of the incoming request using Pydantic.
# FastAPI will reject the request before our code even runs.
# ---------------------------------------------------------
class StudentInput(BaseModel):
    attendance: float = Field(
        ..., ge=0, le=100,
        description="Attendance percentage (0-100)",
        examples=[85]
    )
    assignment_score: float = Field(
        ..., ge=0, le=100,
        description="Assignment score (0-100)",
        examples=[78]
    )
    midterm_score: float = Field(
        ..., ge=0, le=100,
        description="Midterm exam score (0-100)",
        examples=[65]
    )
    final_score: float = Field(
        ..., ge=0, le=100,
        description="Final exam score (0-100)",
        examples=[72]
    )


# ---------------------------------------------------------
# Define the shape of our response, so the API always returns
# a consistent, predictable JSON structure.
# ---------------------------------------------------------
class PredictionOutput(BaseModel):
    prediction: str
    confidence: float


# ---------------------------------------------------------
# A simple root endpoint, just so visiting the base URL shows
# something useful instead of a blank 404 page.
# ---------------------------------------------------------
@app.get("/")
def read_root():
    return {
        "message": "Student Performance Prediction API is running.",
        "docs": "Visit /docs for interactive API documentation.",
        "endpoint": "POST /predict"
    }


# ---------------------------------------------------------
# The main prediction endpoint
# ---------------------------------------------------------
@app.post("/predict", response_model=PredictionOutput)
def predict(student: StudentInput):
    """
    Takes a student's attendance and scores, and predicts
    whether they will Pass or Fail, along with a confidence score.
    """
    try:
        input_data = pd.DataFrame([{
            "Attendance": student.attendance,
            "Assignment_Score": student.assignment_score,
            "Midterm_Score": student.midterm_score,
            "Final_Score": student.final_score
        }])[feature_order]  # reindex to guarantee correct column order

        # Scale the input the same way we scaled our training data
        input_scaled = scaler.transform(input_data)

        # Get the model's prediction (0 = Fail, 1 = Pass)
        prediction_value = model.predict(input_scaled)[0]

        # Get the model's confidence (probability) for that prediction
        probabilities = model.predict_proba(input_scaled)[0]
        confidence = probabilities[prediction_value]

        # Convert 1/0 into a readable label
        result_label = "Pass" if prediction_value == 1 else "Fail"

        return PredictionOutput(
            prediction=result_label,
            confidence=round(float(confidence), 4)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
