import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

AUTHEN_NAME = os.getenv("AUTHEN_NAME")
PROJECT_ID  = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("DATASET_ID")

def create_table(table_id,dataset_id):
    pass

def load_dataset(file_path):
    df = pd.read_csv(file_path,encoding='unicode_escape')
    return df
def load_csv_to_bigquery(df,table_name):
    from google.oauth2 import service_account
    try:
        credentials = service_account.Credentials.from_service_account_file(f'/opt/airflow/dags/data/{AUTHEN_NAME}') # run in airflow
        df.to_gbq( destination_table=f'{DATASET_ID}.{table_name}',  project_id=PROJECT_ID, credentials=credentials, if_exists="replace" )
                
    except Exception as e:
        print("Data load error: " + str(e))

def transform_retail_data(data):
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    data['CustomerID'].fillna(-1,inplace=True)
    data['CustomerID'] = data['CustomerID'].astype('int')
    return data

def transform_country_data(data):
    data['numcode'] = pd.to_numeric(data['numcode'],errors='coerce').astype('Int64')
    return data