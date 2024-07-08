from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import requests
import pandas as pd
import boto3
from io import StringIO

# Configuration
API_KEY = 'c7a5f3cea80fee1ee97edb578137292c'
CITY = 'Arizona'
S3_BUCKET = 'open-weather-s3-bucket'
S3_KEY = 'weather_data/weather.csv'

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition with no scheduler
dag = DAG(
    'OpenWeather_to_s3',
    default_args=default_args,
    description='Fetches weather data, transforms it, and loads it to S3',
    schedule_interval=None,  # Setting schedule_interval to None disables the scheduler
)

def fetch_weather_data():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data

def transform_weather_data(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='fetch_weather_data')

    weather = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'pressure': data['main']['pressure'],
        'humidity': data['main']['humidity'],
        'weather': data['weather'][0]['description'],
        'wind_speed': data['wind']['speed'],
        'date': datetime.utcfromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
    }

    df = pd.DataFrame([weather])
    return df

def load_data_to_s3(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='transform_weather_data')

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    print(df)

    s3_resource = boto3.resource('s3')
    s3_resource.Object(S3_BUCKET, S3_KEY).put(Body=csv_buffer.getvalue())

fetch_task = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=fetch_weather_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_weather_data',
    python_callable=transform_weather_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data_to_s3',
    python_callable=load_data_to_s3,
    provide_context=True,
    dag=dag,
)

fetch_task >> transform_task >> load_task