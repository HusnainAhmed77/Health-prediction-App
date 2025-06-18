import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

# Load database connection info from Streamlit secrets
def get_engine():
    db_config = st.secrets["postgres"]
    user = db_config["user"]
    password = db_config["password"]
    host = db_config["host"]
    port = db_config["port"]
    database = db_config["database"]

    db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    return create_engine(db_url)

# Create the SQLAlchemy engine once
engine = get_engine()

def upload_csv_to_db(df, table_name="patient_data", if_exists="replace"):
    """
    Uploads a DataFrame to the specified PostgreSQL table.

    Args:
        df (pd.DataFrame): DataFrame to upload.
        table_name (str): Name of the database table.
        if_exists (str): What to do if the table exists ('replace', 'append', 'fail').

    Returns:
        pd.DataFrame | None: The uploaded DataFrame, or None if failed.
    """
    try:
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        st.success(f"✅ Data uploaded successfully to '{table_name}' table.")
        return df
    except Exception as e:
        st.error("❌ Failed to upload data to the database.")
        st.exception(e)
        return None

def fetch_data_from_db(table_name="patient_data"):
    """
    Fetches all data from the specified PostgreSQL table.

    Args:
        table_name (str): Name of the database table.

    Returns:
        pd.DataFrame: Retrieved data, or empty DataFrame on failure.
    """
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"❌ Failed to fetch data from table '{table_name}'.")
        st.exception(e)
        return pd.DataFrame()
