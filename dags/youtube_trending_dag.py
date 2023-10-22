import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from youtube_project.youtube_api import extract_trending_youtube_music_videos
from youtube_project.parse_youtube_trending_result import parse_top_10_youtube_music_trending
from youtube_project.plotly_visualization import create_HTML_dashboard

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
    description='Youtube Trending Music Videos in a Day',
    schedule_interval= '@once', #timedelta(minutes=30)
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



task_3 = PythonOperator(
    task_id='create_plotly_dashboard',
    python_callable=create_HTML_dashboard,
    op_kwargs = {'df': task_2.output}
    dag=youtube_trending_dag
)

task_1 >> task_2 >> task_3
