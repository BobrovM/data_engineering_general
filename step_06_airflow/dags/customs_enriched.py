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
        /opt/hadoop/bin/hdfs dfs -put -f /data_share/06_airflowed_tnved/'TNVED3_DECODED.TXT' /task1/input
        /opt/hadoop/bin/hdfs dfs -ls /task1/input
        """,
    )

    run_mapreduce_codedescs = SSHOperator(
        task_id='run_mapreduce_codedescs',
        ssh_conn_id='hdfs-namenode-ssh',
        command="""
        echo "Hostname: $(hostname)"
 
        # SetEnvVars
        export JAVA_HOME=/opt/java/openjdk
        export HADOOP_HOME=/opt/hadoop
        export HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
        export YARN_HOME=/opt/hadoop
        export HADOOP_LOG_DIR=/var/log/hadoop
        export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
        
        echo "JAVA_HOME: $JAVA_HOME"
        echo "HADOOP_HOME: $HADOOP_HOME"
        echo "HADOOP_CONF_DIR: $HADOOP_CONF_DIR"
        echo "YARN_HOME: $YARN_HOME"
        echo "PATH: $PATH"
        
        # Magic
        # idk why do i use full path but let it be
        /opt/hadoop/bin/hdfs dfs -rm -r -f /task1/output_t1
        bash /scripts/shell_scripts_codedescs/yarn_step1_v4.sh
        /opt/hadoop/bin/hdfs dfs -ls /task1/output_t1
        """
    )

    run_mapreduce_history = SSHOperator(
        task_id='run_mapreduce_history',
        ssh_conn_id='hdfs-namenode-ssh',
        command="""
        echo "Hostname: $(hostname)"
 
        # SetEnvVars
        export JAVA_HOME=/opt/java/openjdk
        export HADOOP_HOME=/opt/hadoop
        export HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
        export YARN_HOME=/opt/hadoop
        export HADOOP_LOG_DIR=/var/log/hadoop
        export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
        
        echo "JAVA_HOME: $JAVA_HOME"
        echo "HADOOP_HOME: $HADOOP_HOME"
        echo "HADOOP_CONF_DIR: $HADOOP_CONF_DIR"
        echo "YARN_HOME: $YARN_HOME"
        echo "PATH: $PATH"
        
        # Magic
        # idk why do i use full path but let it be
        /opt/hadoop/bin/hdfs dfs -rm -r -f /task1/output_t2
        bash /scripts/shell_scripts_history_csv/yarn_step2_v2.sh
        /opt/hadoop/bin/hdfs dfs -ls /task1/output_t2
        """
    )

    run_mapreduce_lazysort = SSHOperator(
        task_id='run_mapreduce_lazysort',
        ssh_conn_id='hdfs-namenode-ssh',
        command="""
        echo "Hostname: $(hostname)"
 
        # SetEnvVars
        export JAVA_HOME=/opt/java/openjdk
        export HADOOP_HOME=/opt/hadoop
        export HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
        export YARN_HOME=/opt/hadoop
        export HADOOP_LOG_DIR=/var/log/hadoop
        export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
        
        echo "JAVA_HOME: $JAVA_HOME"
        echo "HADOOP_HOME: $HADOOP_HOME"
        echo "HADOOP_CONF_DIR: $HADOOP_CONF_DIR"
        echo "YARN_HOME: $YARN_HOME"
        echo "PATH: $PATH"
        
        # Magic
        # idk why do i use full path but let it be
        /opt/hadoop/bin/hdfs dfs -rm -r -f /task1/output_lazysort
        bash /scripts/shell_scripts_lazysort/yarn_step_lazysort_v4.sh
        /opt/hadoop/bin/hdfs dfs -ls /task1/output_lazysort
        /opt/hadoop/bin/hdfs dfs -get /task1/output_lazysort /scripts/results_from_hdfs_lazysort_FINAL_OUTPUT
        """
    )


check_mdate >> [task_no_update, put_into_hdfs]
put_into_hdfs >> run_mapreduce_codedescs >> run_mapreduce_history >> run_mapreduce_lazysort