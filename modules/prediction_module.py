# modules/prediction_module.py

import streamlit as st
import numpy as np
import joblib
from utils.preprocessing import preprocess_input

# Load model and scaler once
model = joblib.load("models/diabetes_heart_model.pkl")
scaler = joblib.load("models/scaler.pkl")

def run_prediction():
    st.subheader("🩺 Predict Diabetes & Heart Disease")

    # User input fields
    age = st.slider("Age", 1, 100)
    sex = st.selectbox("Sex", ["Male", "Female"])
    bmi = st.number_input("BMI")
    glucose = st.number_input("Glucose Level")
    hba1c = st.number_input("HbA1c (%)")
    systolic = st.number_input("Systolic BP")
    diastolic = st.number_input("Diastolic BP")
    smoker = st.selectbox("Smoker", ["Yes", "No"])
    activity = st.selectbox("Physical Activity", ["Active", "Inactive"])
    stress = st.selectbox("Stress Level", ["Low", "Medium", "High"])
    sleep = st.slider("Sleep Hours", 0.0, 24.0, step=0.5)
    diet = st.selectbox("Diet Type", ["High-carb", "High-protein", "Balanced"])

    if st.button("Predict"):
        # Prepare dictionary for preprocessing
        data = {
            "Age": age,
            "Sex": sex,
            "BMI": bmi,
            "GlucoseLevel": glucose,
            "HbA1c": hba1c,
            "BP_Systolic": systolic,
            "BP_Diastolic": diastolic,
            "Smoker": smoker,
            "PhysicalActivity": activity,
            "StressLevel": stress,
            "SleepHours": sleep,
            "DietType": diet
        }

        # Preprocess and scale
        features = preprocess_input(data)
        scaled = scaler.transform([features])

        prediction = model.predict(scaled)[0]  # [diabetes_pred, heart_pred]
        probs = model.predict_proba(scaled)    # List of arrays or single array

        diabetes_pred = prediction[0]
        heart_pred = prediction[1]

        # Confidence handling
        if isinstance(probs, list) and len(probs) == 2:
            diabetes_conf = probs[0][0][diabetes_pred] * 100
            heart_conf = probs[1][0][heart_pred] * 100
        else:
            diabetes_conf = heart_conf = None

        # Display Results
        st.success(f"🩸 Diabetes Risk: {'Yes' if diabetes_pred else 'No'}"
                   + (f" ({diabetes_conf:.2f}%)" if diabetes_conf is not None else ""))

        st.success(f"❤️ Heart Disease Risk: {'Yes' if heart_pred else 'No'}"
                   + (f" ({heart_conf:.2f}%)" if heart_conf is not None else ""))

        # Optional: Risk bar display
        if diabetes_conf is not None:
            st.write("Diabetes Risk Level:")
            st.progress(int(diabetes_conf))

        if heart_conf is not None:
            st.write("Heart Disease Risk Level:")
            st.progress(int(heart_conf))
