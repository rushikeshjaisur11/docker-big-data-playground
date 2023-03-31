from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
spark = (SparkSession.builder
         .master("spark://spark-master:7077")
         .appName("read_mysql")
         .config("spark.jars.packages", "mysql:mysql-connector-java:8.0.17")

         .getOrCreate())

options = {'url': 'jdbc:mysql://mysql:3306/bigdataproject',
           'user': 'root',
           'password': 'root',
           'dbtable': 'stg_card_transactions',
           'driver': 'com.mysql.cj.jdbc.Driver'
           }
schema = StructType([
    StructField('card_id', StringType()),
    StructField('member_id', StringType()),
    StructField('amount', StringType()),
    StructField('postcode', StringType()),
    StructField('pos_id', StringType()),
    StructField('transaction_dt', StringType()),
    StructField('status', StringType()),
])
data = spark.read.csv(
    'hdfs://namenode:9000/project_input_data/input_data/card_transactions.csv', schema=schema)
spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
data = data.withColumn('transaction_dt', date_format(to_timestamp(
    col('transaction_dt'),  "dd-MM-yyyy HH:mm:ss"), "yyyy-MM-dd HH:mm:ss"))
data = data.dropDuplicates(subset=['card_id', 'transaction_dt'])
data.write.mode('append').format('jdbc').options(**options).save()
