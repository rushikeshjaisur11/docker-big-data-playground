from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
import datetime

dag = DAG(dag_id="edgeNodeDAG", start_date=datetime.datetime.now(),
          schedule_interval = None)

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

task3 = SSHOperator(task_id="hadoop_dirs",
                    ssh_conn_id="edgenode",
                    command="hadoop fs -ls /",
                    dag=dag)
task1 >> task2
task3
