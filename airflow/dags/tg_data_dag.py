from telegram_feature.telegram_utils import TelegramClient, read_tg_channels, read_tg_info
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

args = {
    'owner': 'bro',
    'start_date': datetime(2024,   2,   22),
    'provide_context': True
}

api_id, api_hash = read_tg_info()
session_string = "AgFfAc4ALjzMYIRz_9iLm_ptYPK5cFGQARRXPakqBwVYTf6HWie7qDJ0WD2vXLCy99QJf63OnWllsvcQreSZF5TEKY1i0tGLUM2uU8fkIYVhdrxjyKU_6F20Eh-yRiZp6nCTsPCK8GQfsOy3QqNeI0FsgPGdbcL77kZ4mPRM3Pfh2JT8NPz0CvwbLbHjRejqts8UdskIbqPqPJ-kXpnfeCBDNA7l8OaSKx11mry7VPjCXoS6iMKZt4tQAlApvN7qgSps58V-YTJe2lhtn0cIKpp_cuBktINFiFEKmF3ztOtnpTXCyWCRCdXDA9y3eQQPLsVMG657OD9KXhojzdEwv1fAD6DHrwAAAAFs60KSAA"
client = TelegramClient(api_id, api_hash, session_string)

def retrieve_posts(client, channel_id, n, **kwargs):
    client.get_n_last_posts(channel_id, n)

with DAG('tg_data_dag', description='Retrieve last n posts from Telegram channels', schedule_interval='*/2 * * * *',  catchup=False, default_args=args) as dag:
    channels = read_tg_channels()
    for i, channel_id in enumerate(channels):
        task = PythonOperator(
            task_id=f'retrieve_posts_channel_{i}',
            python_callable=retrieve_posts,
            op_args=[client, channel_id,   150]
        )