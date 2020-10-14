import requests

from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow.operators.python_operator import PythonOperator
from ptt_trend_radar.initialize import article_sender


def send_ifttt():
    articles = article_sender()
    if len(articles)>10:
        url = ('https://maker.ifttt.com/trigger/{your_trigger}/with/key/{your_keys}' +
            '?value1='+articles)
        r = requests.get(url)     

default_args = {
    'owner': 'weed',
    'start_date': datetime(2020, 10, 2, 10, 10),
    'retries': 2,
    'retry_delay':timedelta(seconds=5)
}


with DAG('PTT-alert', default_args=default_args, schedule_interval=timedelta(seconds=30.5), catchup=False) as dag:
    PythonOperator(
        python_callable=send_ifttt,
        task_id="article_sender"
    )

