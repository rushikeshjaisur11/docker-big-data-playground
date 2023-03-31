from pyspark.sql import SparkSession
spark = (SparkSession.builder.master("spark://spark-master:7077")
         .appName("hive_connection")
         .config("hive.metastore.uris", "thrift://hive-metastore:9083")
         .config("spark.sql.warehouse.dir", "hdfs://namenode:9000/user/hive/warehouse")
         .enableHiveSupport()
         .getOrCreate())
spark.sql("SET HIVE.ENFORCE.BUCKETING=TRUE;")
spark.sql("""
          create external table if not exists bigdataproject.member_score
          (
          member_id string,
          score float
          )
          row format delimited fields terminated by ','
          stored as textfile
          location '/project_input_data/input_data/member_score/';
          
          """)

spark.sql("""create external table if not exists bigdataproject.member_details
            (
            card_id bigint,
            member_id bigint,
            member_joining_dt timestamp ,
            card_purchase_dt string ,
            country string,
            city string,
            score float
            )
            row format delimited fields terminated by ','
            stored as textfile
            location '/project_input_data/input_data/member_details/'
        """)

spark.sql("""
          create table if not exists member_score_bucketed
            (
            member_id string,
            score float
            )
            CLUSTERED BY (member_id) into 8 buckets
          """)
spark.sql("""
          create table if not exists member_details_bucketed
            (
            card_id bigint,
            member_id bigint,
            member_joining_dt timestamp ,
            card_purchase_dt timestamp ,
            country string,
            city string,
            score float
            )
            CLUSTERED BY (card_id) into 8 buckets;
          """)

spark.sql("""
          create external table if not exists card_transactions (
            card_id bigint,
            member_id bigint,
            amount float,
            postcode int,
            pos_id bigint,
            transaction_dt timestamp,
            status string
            )
            row format delimited fields terminated by ','
            stored as textfile
            location '/project_input_data/card_transactions/';
          """)
