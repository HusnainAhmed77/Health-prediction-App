import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import streamlit as st

# 🔐 Database credentials – customize these
DB_NAME = "health_db"
DB_USER = "postgres"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"

# 🌐 Create connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 📌 1. Create SQLAlchemy engine
def get_engine():
    try:
        engine = create_engine(DATABASE_URL)
        return engine
    except Exception as e:
        st.error(f"Error creating database engine: {e}")
        return None

# 📌 2. Load CSV into database
def load_csv_to_postgres(csv_path: str, table_name: str = "patients"):
    try:
        df = pd.read_csv(csv_path)
        engine = get_engine()
        if engine:
            df.to_sql(table_name, engine, index=False, if_exists="replace")
            st.success(f"✅ CSV data loaded into '{table_name}' table.")
    except Exception as e:
        st.error(f"Error loading CSV to DB: {e}")

# 📌 3. Fetch data from table
def fetch_data_from_db(table_name: str = "patients"):
    try:
        engine = get_engine()
        if engine:
            df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
            return df
    except Exception as e:
        st.error(f"Error fetching data from DB: {e}")
        return pd.DataFrame()
