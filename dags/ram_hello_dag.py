from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

def print_hello_with_time():
    now = datetime.now()
    print(f"Hello Ram, now it is {now.strftime('%I:%M %p')}")

def print_time_over():
    print("Time over")

default_args = {
    'owner': 'Ram Kumar',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'retries': 0,
     'catchup': True,
}

dag = DAG(
    'hello_ram_minutes',
    default_args=default_args,
    schedule_interval=timedelta(minutes=5),
)

with dag:
    tasks = []
    for i in range(11):
        task_id = f'print_hello_with_time_{i}'
        task = PythonOperator(
            task_id=task_id,
            python_callable=print_hello_with_time,
            dag=dag,
        )
        tasks.append(task)

    time_over_task = PythonOperator(
        task_id='print_time_over',
        python_callable=print_time_over,
        dag=dag,
    )

    for i in range(10):
        tasks[i] >> tasks[i+1]

    tasks[-1] >> time_over_task

