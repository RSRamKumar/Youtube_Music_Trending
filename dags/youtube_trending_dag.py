import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from youtube_project.youtube_api import extract_trending_youtube_music_videos
from youtube_project.parse_youtube_trending_result import parse_top_10_youtube_music_trending

import pandas as pd
from datetime import datetime, timedelta
import pendulum


default_args = {
    'owner': 'ramkumar',
    'start_date': days_ago(0) ,#pendulum.datetime(2023,3,29,15,50,tz='Europe/Berlin'),#datetime(2023,3,29,13),# days_ago(0)
    'retries':1,

}

youtube_trending_dag = DAG(
    'youtube_music_trending_dag',
    default_args=default_args,
    description='Youtube Trending Music Videos in a Day Every 30 mins',
    schedule_interval= timedelta(minutes=30),
    catchup=False
)

task_1 = PythonOperator(
    task_id='extraction_of_videos',
    python_callable= extract_trending_youtube_music_videos ,
    dag=youtube_trending_dag
)



task_2 = PythonOperator(
    task_id='parse_of_videos',
    python_callable= parse_top_10_youtube_music_trending ,
    op_kwargs = {'youtube_trending_results_raw': task_1.output},
    dag=youtube_trending_dag
)


def load_data_to_sqlite():
    df = pd.read_csv(f'{dag_path}/processed_data/trending_results.csv')



# task_3 = PythonOperator(
#     task_id='loading_of_videos_to_sqlite_db',
#     python_callable=load_data_to_sqlite,
#     dag=youtube_trending_dag
# )

task_1 >> task_2
