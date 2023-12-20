from numpy import save
import yaml
from sqlalchemy import create_engine
import pandas as pd
import os
from pathlib import Path

def load_credentials(file_path='credentials.yaml'):
    """
    Load database credentials from a YAML file.

    Parameters:
    - file_path (str): Path to the YAML file containing credentials.

    Returns:
    - dict: Database credentials.
    """
    with open(file_path, 'r') as file:
        credentials = yaml.safe_load(file)
    return credentials

def load_data(file_path):
    pwd = os.getcwd()
    df = pd.read_csv(pwd + file_path)
    return df

class RDSDatabaseConnector:
    def __init__(self, credentials):
        """
        Initialize the RDSDatabaseConnector.

        Parameters:
        - credentials (dict): Dictionary containing database connection details.
        """
        self.credentials = credentials
        self.engine = self.create_engine()

    def create_engine(self):
        """
        Create a SQLAlchemy engine for database connection.

        Returns:
        - sqlalchemy.engine.base.Engine: SQLAlchemy engine object.
        """
        db_url = f"postgresql+psycopg2://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}:{self.credentials['RDS_PORT']}/{self.credentials['RDS_DATABASE']}"
        engine = create_engine(db_url)
        return engine

    def extract_data(self, table_name='loan_payments'):
        """
        Extract data from the RDS database and return it as a Pandas DataFrame.

        Parameters:
        - table_name (str): Name of the table to extract data from.

        Returns:
        - pd.DataFrame: Pandas DataFrame containing the extracted data.
        """
        query = f"SELECT * FROM {table_name};"
        data_frame = pd.read_sql(query, self.engine)
        return data_frame

    def save_to_csv(self, data_frame, file_name='loan_payments.csv'):
        """
        Save Pandas DataFrame to a local CSV file.

        Parameters:
        - data_frame (pd.DataFrame): Pandas DataFrame to be saved.
        - file_name (str): Name of the CSV file to save.

        Returns:
        - None
        """
        data_frame.to_csv(file_name, index=False)

# Corrected Example Usage
if __name__ == "__main__":
    # Load credentials
    credentials = load_credentials()

    # Create RDSDatabaseConnector instance
    rds_connector = RDSDatabaseConnector(credentials)

    # Extract data
    data = rds_connector.extract_data()

    # Save data to local CSV
    rds_connector.save_to_csv(data)
