from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
spark = (SparkSession.builder
         .master("spark://spark-master:7077")
         .appName("read_mysql")
         .config("spark.jars.packages", "mysql:mysql-connector-java:8.0.17")

         .getOrCreate())
options = {'url': 'jdbc:mysql://mysql:3306/bigdataproject',
           'user': 'root',
           'password': 'root',
           'dbtable': 'card_transactions',
           'driver': 'com.mysql.cj.jdbc.Driver'
           }
# spark.sql("""insert into table bigdataproject.member_score_bucketed
#   select * from bigdataproject.member_score""")
# spark.sql("""insert into table bigdataproject.member_details_bucketed
# select * from bigdataproject.member_details;""")

df = spark.read.format("jdbc").options(**options).load()
df.write.mode("overwrite").format("parquet").save(
    "hdfs://namenode:9000/project_input_data/card_transactions")

# spark.sql("""insert into table bigdataproject.card_transactions_bucketed
# select concat_ws('~',cast(card_id as string),cast(transaction_dt as string)) as
# cardid_txnts,card_id,member_id,amount,postcode,pos_id,transaction_dt,status
# from bigdataproject.card_transactions;
# """)
