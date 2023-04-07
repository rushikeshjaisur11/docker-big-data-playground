from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
spark = (SparkSession.builder
         .master("spark://spark-master:7077")
         .appName("read_mysql")
         .config("hive.metastore.uris", "thrift://hive-metastore:9083")
         .config("spark.sql.warehouse.dir", "hdfs://namenode:9000/user/hive/warehouse")
         .enableHiveSupport()

         .getOrCreate())
df_ucl = spark.sql("""
			with cte_rownum as
			(
			select card_id,amount,member_id,transaction_dt,
			first_value(postcode) over(partition by card_id order by transaction_dt desc) as postcode,
			row_number() over(partition by card_id order by transaction_dt desc) rownum
			from bigdataproject.card_transactions
			)
			select card_id,member_id,
			round((avg(amount)+ 3* max(std)),0) as ucl ,
			max(score) score,
			max(transaction_dt) as last_txn_time,
			max(Postcode)as last_txn_zip	
			from
			(	select
			card_id,amount,
			c.member_id,
			m.score,
			c.transaction_dt,
			Postcode,
			STDDEV (amount) over(partition by card_id order by (select 1)  desc) std
			from cte_rownum c
			inner join bigdataproject.member_score_bucketed m on c.member_id=m.member_id 
			where rownum<=10
			)a
			group by card_id,member_id
			""")
df = df_ucl.select("card_id", "member_id", "ucl", "score",
                   "last_txn_time", "last_txn_zip")
df.show()
df.write.mode("append").saveAsTable("bigdataproject.card_lookup_stg")
