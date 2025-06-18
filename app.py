import streamlit as st
from modules.prediction_module import run_prediction
from modules.visualization_module import run_dashboard
from modules.database_module import fetch_data_from_db, upload_csv_to_db

import pandas as pd
import os

st.set_page_config(page_title="Smart Healthcare Assistant", layout="wide")

st.title("🧠 Smart Healthcare Assistant")
st.markdown("Predict health risks and visualize patient metrics using AI.")

# Sidebar Navigation
option = st.sidebar.radio("Choose View", [
    "Prediction", 
    "Dashboard", 
    "Upload CSV to DB", 
    "Database Viewer"
])

if option == "Prediction":
    input_mode = st.selectbox("Choose input mode", ["Manual Entry", "From CSV File", "From Database"])

    if input_mode == "Manual Entry":
        run_prediction()

    elif input_mode == "From CSV File":
        uploaded = st.file_uploader("Upload CSV with patient data", type="csv")
        if uploaded:
            df = pd.read_csv(uploaded)
            st.write("📄 Data Preview", df.head())

            from utils.preprocessing import preprocess_input
            from modules.prediction_module import model, scaler

            for i, row in df.iterrows():
                features = preprocess_input(row.to_dict())
                scaled = scaler.transform([features])
                prediction = model.predict(scaled)[0]

                st.write(f"Patient {i+1}:")
                st.success(f"🩸 Diabetes: {'Yes' if prediction[0] else 'No'}")
                st.success(f"❤️ Heart Disease: {'Yes' if prediction[1] else 'No'}")
                st.markdown("---")

    elif input_mode == "From Database":
        df = fetch_data_from_db()
        st.write("📦 Data from Database", df.head())

        from utils.preprocessing import preprocess_input
        from modules.prediction_module import model, scaler

        for i, row in df.iterrows():
            features = preprocess_input(row.to_dict())
            scaled = scaler.transform([features])
            prediction = model.predict(scaled)[0]

            st.write(f"Patient {i+1}:")
            st.success(f"🩸 Diabetes: {'Yes' if prediction[0] else 'No'}")
            st.success(f"❤️ Heart Disease: {'Yes' if prediction[1] else 'No'}")
            st.markdown("---")

elif option == "Dashboard":
    run_dashboard()

elif option == "Upload CSV to DB":
    st.subheader("📤 Upload Patient CSV to Database")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df_uploaded = upload_csv_to_db(df)
        st.success("✅ CSV uploaded to database!")
        st.dataframe(df_uploaded)

elif option == "Database Viewer":
    st.subheader("📂 View Patients from Database")
    df = fetch_data_from_db()
    st.dataframe(df)
