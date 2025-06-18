import pandas as pd
from sqlalchemy import create_engine
import getpass
import streamlit as st


DATABASE_URL = st.secrets["DATABASE_URL"]  # You’ll set this in Streamlit Cloud

engine = create_engine(DATABASE_URL)


def upload_csv_to_db(data, table_name="patients", if_exists="append"):
    """
    Uploads data to PostgreSQL from a DataFrame or CSV file path.

    Args:
        data (str or pd.DataFrame): CSV path or DataFrame
        table_name (str): Target table name
        if_exists (str): 'fail', 'replace', or 'append'
    """
    if isinstance(data, str):
        df = pd.read_csv(data)
    elif isinstance(data, pd.DataFrame):
        df = data
    else:
        raise ValueError("Input must be a CSV file path or pandas DataFrame.")

    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    return df

def fetch_data_from_db(table_name="patients"):
    """
    Fetches entire table from PostgreSQL into a pandas DataFrame.
    """
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    return df
