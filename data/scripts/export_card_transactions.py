from pyspark.sql import SparkSession

spark = (SparkSession.builder.master("spark://spark-master:7077")
         .appName("hive_connection")
         .config("hive.metastore.uris", "thrift://hive-metastore:9083")
         .config("spark.sql.warehouse.dir", "hdfs://namenode:9000/user/hive/warehouse")
         .enableHiveSupport()
         .getOrCreate())
schema = """ card_id bigint,member_id bigint,amount int,postcode int,pos_id bigint,transaction_dt string,status string"""
df = spark.read.csv('hdfs://namenode:9000/project_input_data/input_data/card_transactions.csv',
                    header=False, schema=schema)
df = df.dropDuplicates(subset=['card_id', 'transaction_dt'])
df.write.mode("append").format("hive").saveAsTable(
    "bigdataproject.card_transactions")
