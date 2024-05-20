import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.http.sensors.http import HttpSensor
from plotly_viz import create_HTML_dashboard

from parse_youtube_trending_result import parse_top_10_youtube_music_trending
from youtube_api import extract_trending_youtube_videos

default_args = {
    "owner": "ramkumar",
    "start_date": pendulum.today(
        "Europe/Berlin"
    ),  # pendulum.datetime(2024,5,19,tz='Europe/Berlin'),#datetime(2023,3,29,13)
    "retries": 1,
}

with DAG(
    "Youtube-Music-Trending-DAG",
    default_args=default_args,
    description="Youtube Trending Music Videos in a Day",
    schedule="@once",  # timedelta(minutes=30)
    catchup=False,
) as dag:
    task_0 = HttpSensor(
        task_id="check_youtube_api_ready",
        http_conn_id="youtube_api_url",
        endpoint="youtube/v3/videos?part=contentDetails%2Cid%2Csnippet%2Cstatistics&chart=mostPopular&maxResults=10&regionCode=IN&videoCategoryId=10&key=AIzaSyDeydpyIqXNbwAlAnjuqxcpr5s_n12QynQ&alt=json",
    )

    task_1 = PythonOperator(
        task_id="extraction_of_videos",
        python_callable=extract_trending_youtube_videos,
    )

    task_2 = PythonOperator(
        task_id="parse_of_videos",
        python_callable=parse_top_10_youtube_music_trending,
        op_kwargs={"youtube_trending_results_raw": task_1.output},
    )

    task_3 = BashOperator(
        task_id="copy_data_from_landing_to_intermediate_bucket",
        bash_command='aws s3 cp {{ti.xcom_pull("parse_of_videos")[1]}} s3://youtube-data-bucket-ram-intermediate-data/{{ti.xcom_pull("parse_of_videos")[0]}}',
    )

    task_4 = S3KeySensor(
        task_id="check_for_transformed_csv_data",
        bucket_key='{{ti.xcom_pull("parse_of_videos")[2]}}',
        bucket_name="youtube-data-bucket-ram-transformed-data",
        aws_conn_id="aws_default",
        poke_interval=15,
        timeout=120,
    )

    task_5 = PythonOperator(
        task_id="create_plotly_dashboard",
        python_callable=create_HTML_dashboard,
        op_kwargs={
            "file_path": 's3://youtube-data-bucket-ram-transformed-data/{{ti.xcom_pull("parse_of_videos")[2]}}'
        },
    )

    task_6 = BashOperator(
        task_id="move_plotly_dashboard_from_ec2_to_transformed_bucket",
        bash_command='aws s3 mv {{ti.xcom_pull("create_plotly_dashboard")[0]}} s3://youtube-data-bucket-ram-transformed-data/',
    )

    task_0 >> task_1 >> task_2 >> task_3 >> task_4 >> task_5 >> task_6
