from datetime import timedelta,datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator

import Jobs.pipline_jobs as jobs
default_args = {
    'owner': 'minhduc',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'etl_to_bigquery',
    default_args=default_args,
    description="ETL data from csv file to DWH BigQuery",
    catchup=False, # Chay cac job truoc do
    schedule="@daily", # same "0 0 * * *" ~ "minute hour DayofMonth Month DayofWeek"
    start_date=datetime(2024, 3, 25)
) as dag:
    
    create_retail_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_retail_dataset',
        project_id='steady-monitor-415517',
        dataset_id='retail',
        location='asia-southeast1',
        gcp_conn_id='gcp'
    )


    # create_table = BigQueryCreateEmptyTableOperator(
    #     task_id='create_table',
    #     dataset_id='retail',
    #     table_id='invoice_cleaned',
    #     schema_fields=[
    #         {'name': 'InvoiceNo', 'type': 'STRING'},
    #         {'name': 'StockCode', 'type': 'STRING'},
    #         {'name': 'Description', 'type': 'STRING'},
    #         {'name': 'Quantity', 'type': 'INTEGER'},
    #         {'name': 'InvoiceDate', 'type': 'DATETIME'},
    #         {'name': 'UnitPrice', 'type': 'FLOAT'},
    #         {'name': 'CustomerID', 'type': 'INTEGER'},
    #         {'name': 'Country', 'type': 'STRING'}
    #     ],
    #     gcp_conn_id='gcp'
    # )
    
    # Load file csv file
    start_etl = EmptyOperator(
        task_id='start_etl'
    )

    extract_retail_file = PythonOperator(
        task_id='extract_retail_file',
        python_callable=jobs.load_dataset,
        op_kwargs={
            'file_path':'/opt/airflow/dags/data/Online_Retail.csv'
        }
    )

    extract_country_file = PythonOperator(
        task_id='extract_country_file',
        python_callable=jobs.load_dataset,
        op_kwargs={
            'file_path':'/opt/airflow/dags/data/country.csv'
        }
    )


    transform_retail_data = PythonOperator(
        task_id='transform_retail_data',
        python_callable=jobs.transform_retail_data,
        op_kwargs={
            'data': extract_retail_file.output
        }
    )

    transform_country_data = PythonOperator(
        task_id='transform_country_data',
        python_callable=jobs.transform_country_data,
        op_kwargs={
            'data': extract_country_file.output
        }
    )

    
    load_retail_data = PythonOperator(
        task_id='load_retail_data_to_BigQuery',
        python_callable=jobs.load_csv_to_bigquery,
        op_kwargs={
            'df': transform_retail_data.output,
            'table_name':'invoice_cleaned'
        }
    )

    load_country_data = PythonOperator(
        task_id='load_country_data_to_BigQuery',
        python_callable=jobs.load_csv_to_bigquery,
        op_kwargs={
            'df': transform_country_data.output,
            'table_name':'country'
        }
    )
    create_retail_DWH_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_retail_DWH_dataset',
        project_id='steady-monitor-415517',
        dataset_id='retail_DWH',
        location='asia-southeast1',
        gcp_conn_id='gcp'
    )
    dbt_build_warehouse = BashOperator(
        task_id='dbt_build_warehouse',
        bash_command='cd /opt/airflow/dags/dbt_transform && dbt run --profiles-dir .'
    )
    end_etl = EmptyOperator(
        task_id='end_etl'
    )

#DAG
start_etl >> create_retail_dataset 

create_retail_dataset >> [extract_retail_file,extract_country_file]

[transform_retail_data,transform_country_data]

[load_retail_data,load_country_data] >>  dbt_build_warehouse >> end_etl