from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.models import Variable
from pathlib import Path
import os
import logging


def _check_mdate():
    logger = logging.getLogger(__name__)

    logger.info('check_mdate_start')

    paths = []
    paths.append(Path('/') / 'app' / 'data_share' / '06_airflowed_tnved')
    paths.append(Path('..') / '..' / 'data_share' / '06_airflowed_tnved')
    outpath = '/'

    logger.info('check_mdate_path')

    for path in paths:
        path = path.resolve()
        if path.exists():
            outpath = path
            break

    logger.info('check_mdate_outpath')

    filetime = str(os.path.getmtime(outpath / 'TNVED3_DECODED.TXT'))
    airflow_filetime = Variable.get('TNVED3_DECODED_filetime', default_var=None)

    logger.info('check_mdate_mtime')

    if not airflow_filetime or filetime > airflow_filetime:
        Variable.set('TNVED3_DECODED_filetime', filetime)
        return 'put_into_hdfs'
    else:
        return 'task_no_update'


'''def _enrich_mapreduce():
    pass'''


with DAG(
    'customs_enriched',
    start_date=datetime(2026, 8, 1),
    catchup=False,
    schedule='@daily'
) as dag:
    check_mdate = BranchPythonOperator(
        task_id='check_mdate',
        python_callable=_check_mdate,
    )

    task_no_update = EmptyOperator(
        task_id='task_no_update',
    )

    # PURE BRAINFUCK
    put_into_hdfs = SSHOperator(
        task_id='put_into_hdfs',
        ssh_conn_id='hdfs-namenode-ssh',
        command="""
        export JAVA_HOME=/opt/java/openjdk
        /opt/hadoop/bin/hdfs dfs -mkdir /TESTSSH
        /opt/hadoop/bin/hdfs dfs -ls /
        """,
    )

    '''
    enrich_mapreduce = PythonOperator(
        task_id='enrich_mapreduce',
        python_callable=_enrich_mapreduce,
    )'''

check_mdate >> [task_no_update, put_into_hdfs]