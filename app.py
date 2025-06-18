import streamlit as st
import pandas as pd
from modules.prediction_module import run_prediction, model, scaler
from modules.visualization_module import run_dashboard
from modules.database_module import fetch_data_from_db, upload_csv_to_db
from utils.preprocessing import preprocess_input

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

# ---------------------- PREDICTION MODE ----------------------
if option == "Prediction":
    input_mode = st.selectbox("Choose input mode", ["Manual Entry", "From CSV File", "From Database"])

    # --- Manual Entry ---
    if input_mode == "Manual Entry":
        run_prediction()

    # --- Prediction from CSV File ---
    elif input_mode == "From CSV File":
        uploaded = st.file_uploader("📁 Upload CSV with patient data", type="csv")
        if uploaded:
            df = pd.read_csv(uploaded)
            st.subheader("📄 Data Preview")
            st.dataframe(df.head())

            st.subheader("🔍 Predictions")
            for i, row in df.iterrows():
                try:
                    features = preprocess_input(row.to_dict())
                    scaled = scaler.transform([features])
                    prediction = model.predict(scaled)[0]
                    
                    st.write(f"### 🧑‍⚕️ Patient {i+1}")
                    st.success(f"🩸 Diabetes: {'Yes' if prediction[0] else 'No'}")
                    st.success(f"❤️ Heart Disease: {'Yes' if prediction[1] else 'No'}")
                    st.markdown("---")
                except Exception as e:
                    st.error(f"Prediction failed for Patient {i+1}")
                    st.exception(e)

    # --- Prediction from Database ---
    elif input_mode == "From Database":
        df = fetch_data_from_db()
        if not df.empty:
            st.subheader("📦 Data from Database")
            st.dataframe(df.head())

            st.subheader("🔍 Predictions")
            for i, row in df.iterrows():
                try:
                    features = preprocess_input(row.to_dict())
                    scaled = scaler.transform([features])
                    prediction = model.predict(scaled)[0]
                    
                    st.write(f"### 🧑‍⚕️ Patient {i+1}")
                    st.success(f"🩸 Diabetes: {'Yes' if prediction[0] else 'No'}")
                    st.success(f"❤️ Heart Disease: {'Yes' if prediction[1] else 'No'}")
                    st.markdown("---")
                except Exception as e:
                    st.error(f"Prediction failed for Patient {i+1}")
                    st.exception(e)
        else:
            st.warning("⚠️ No data available in the database.")

# ---------------------- DASHBOARD ----------------------
elif option == "Dashboard":
    run_dashboard()

# ---------------------- CSV UPLOAD TO DB ----------------------
elif option == "Upload CSV to DB":
    st.subheader("📤 Upload Patient CSV to Database")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            uploaded_df = upload_csv_to_db(df)
            if uploaded_df is not None:
                st.success("✅ CSV uploaded to database successfully!")
                st.dataframe(uploaded_df)
        except Exception as e:
            st.error("❌ Failed to upload CSV.")
            st.exception(e)

# ---------------------- DATABASE VIEW ----------------------
elif option == "Database Viewer":
    st.subheader("📂 View Patients from Database")
    df = fetch_data_from_db()
    if not df.empty:
        st.dataframe(df)
    else:
        st.warning("⚠️ No data found in the database.")
