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

df = spark.read.format('jdbc').options(**options).load()
df.show()
