from pyspark.sql import SparkSession
import findspark
findspark.init('/spark')
spark = SparkSession.builder.master(
    "spark://spark-master:7077").appName('test').getOrCreate()
a = spark.range(19)
print(a.collect())
