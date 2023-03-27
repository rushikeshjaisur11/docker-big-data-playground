from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
import datetime

dag = DAG(dag_id="edgeNodeDAG", start_date=datetime.datetime.now())

task1 = SSHOperator(
    task_id="echo_task",
    ssh_conn_id="edgenode",
    command="whoami",
    dag=dag
)
task2 = SSHOperator(task_id="spark_version",
                    ssh_conn_id="edgenode",
                    command="pyspark --verison",
                    dag=dag)
