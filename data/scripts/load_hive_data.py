from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
spark = (SparkSession.builder
         .master("spark://spark-master:7077")
         .appName("read_mysql")
         .config("hive.metastore.uris", "thrift://hive-metastore:9083")
         .config("spark.sql.warehouse.dir", "hdfs://namenode:9000/user/hive/warehouse")
         .config("spark.jars.packages", "mysql:mysql-connector-java:8.0.17")
         .enableHiveSupport()

         .getOrCreate())
options = {'url': 'jdbc:mysql://mysql:3306/bigdataproject',
           'user': 'root',
           'password': 'root',
           'dbtable': 'card_transactions',
           'driver': 'com.mysql.cj.jdbc.Driver'
           }

# df_member_score = spark.sql("select * from bigdataproject.member_score")
# df_member_score.write.bucketBy(8,'card_id').mode('append').format(
#     'hive').saveAsTable("bigdataproject.member_score_bucketed")

# df_member_details = spark.sql("select * from bigdataproject.member_details")
# df_member_details.write.mode('append').format(
#     'hive').saveAsTable("bigdataproject.member_details_bucketed")

df = spark.read.format("jdbc").options(**options).load()
df = df.withColumn("transaction_dt", to_timestamp(
    col('transaction_dt'), "yyyy-MM-dd'T'HH:mm:ss.SSSSSSS'Z'"))
df = df.withColumn('transaction_dt', col('transaction_dt').cast(StringType()))
df.show()
df.write.mode("overwrite").format("csv").save(
    "hdfs://namenode:9000/project_input_data/card_transactions")

# df_card_transactions = spark.sql(
#     "select * from bigdataproject.card_transactions")
# df_card_transactions = (df_card_transactions
#                         .withColumn("card_id2", col('card_id').cast(StringType()))
#                         .withColumn("card_id2", col('transaction_dt').cast(StringType()))
#                         .withColumn("cardid_txnts", concat_ws('~', col('card_id2'), col('transaction_dt2')))
#                         ).drop("card_id2", "card_id2")
# df_card_transactions = df_card_transactions.select(
#     'cardid_txnts', 'card_id', 'member_id', 'amount', 'postcode', 'pos_id', 'transaction_dt', 'status')

# df_card_transactions.write.mode('append').format(
#     'hive').saveAsTable("bigdataproject.card_transactions_bucketed")
