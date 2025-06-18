# modules/visualization_module.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

def run_dashboard():
    st.subheader("📈 Patient Health Metrics Dashboard")
    
    uploaded_file = st.file_uploader("Upload patient history CSV", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file, parse_dates=["VisitDate"])

        if 'PatientID' in df.columns:
            patient_ids = df['PatientID'].unique()
            selected_patient = st.selectbox("Select Patient ID", patient_ids)
            df = df[df['PatientID'] == selected_patient]

        st.markdown("### Blood Pressure Over Time")
        if 'VisitDate' in df.columns and 'BP_Systolic' in df.columns and 'BP_Diastolic' in df.columns:
            fig, ax = plt.subplots(figsize=(10, 4))
            df_sorted = df.sort_values("VisitDate")
            sns.lineplot(x="VisitDate", y="BP_Systolic", data=df_sorted, label="Systolic", ax=ax)
            sns.lineplot(x="VisitDate", y="BP_Diastolic", data=df_sorted, label="Diastolic", ax=ax)
            plt.ylabel("Blood Pressure (mmHg)")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        st.markdown("### Glucose & HbA1c Trends")
        if 'GlucoseLevel' in df.columns and 'HbA1c' in df.columns:
            fig2 = px.line(df.sort_values("VisitDate"), x='VisitDate', y=['GlucoseLevel', 'HbA1c'],
                           labels={'value': 'Level', 'VisitDate': 'Date'}, title="Glucose & HbA1c Over Time")
            st.plotly_chart(fig2)

        st.markdown("### Risk Prediction Distribution (if included)")
        if 'Diabetes' in df.columns and 'HeartDisease' in df.columns:
            col1, col2 = st.columns(2)

            with col1:
                fig3 = px.histogram(df, x="Diabetes", color="Diabetes", title="Diabetes Risk Distribution")
                st.plotly_chart(fig3)

            with col2:
                fig4 = px.histogram(df, x="HeartDisease", color="HeartDisease", title="Heart Disease Risk Distribution")
                st.plotly_chart(fig4)
