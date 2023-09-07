from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import desc, row_number, monotonically_increasing_id
from pyspark.sql.window import Window
from pymongo import *

import time
kafka_topic_name = "weather"
kafka_bootstrap_servers = "localhost:9092"
working_directory = 'jars/*'
spark = SparkSession \
        .builder \
        .appName("Structured Streaming Pkt") \
        .master("local") \
        .config("spark.mongodb.input.uri", "mongodb://localhost:27017/test.weather") \
        .config("spark.mongodb.output.uri", "mongodb://localhost:27017/test.weather") \
        .config('spark.driver.extraClassPath', working_directory) \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
        .getOrCreate()

    #.master("local") \
logger = spark._jvm.org.apache.log4j
logger.LogManager.getRootLogger().setLevel(logger.Level.FATAL)

spark.sparkContext.setLogLevel("ERROR")
# Construct a streaming DataFrame that reads from topic
tweet_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic_name) \
        .option("includeHeaders", "true") \
        .option("startingOffsets", "latest") \
        .option("spark.streaming.kafka.maxRatePerPartition", "50") \
        .load()

tweet_df.printSchema()

def write_row_in_mongo(df,epoch_id):
    mongoURL = "mongodb+srv://chakrika:chakku1234@cluster0.iqhrywt.mongodb.net/weather.weather" \
               "?retryWrites=true&w=majority"
    df.write.format("mongo").mode("append").option("uri", mongoURL)
    pass

df11 = tweet_df.selectExpr("CAST(value AS STRING)")

df11.createOrReplaceTempView("temp")
temp_text = spark.sql("SELECT * FROM temp")
temp_write_stream = temp_text.writeStream.outputMode("append").format("memory").queryName("testedTable5").start()

temp_write_stream.awaitTermination(20)
    
df = spark.sql("SELECT * FROM testedTable5")


df = df.withColumn('time', row_number().over(Window.orderBy(monotonically_increasing_id())))
df.show()

from pyspark.ml.feature import VectorAssembler
assembler = VectorAssembler(inputCols=["time"], outputCol="time_vector")
df1 = assembler.transform(df)
df1.show()

df1 = df1.selectExpr("CAST(value AS DOUBLE)","time_vector","time")

df1.select(count("value")).show()

df1.select(avg("value")).show()

from pyspark.ml.regression import *
train_data,test_data=df1.randomSplit([0.75,0.25])
regressor=LinearRegression(featuresCol="time_vector", labelCol="value")
regressor=regressor.fit(train_data)
regressor.coefficients
pred_results=regressor.evaluate(test_data)
results = pred_results.predictions.selectExpr("CAST(value AS DOUBLE)","time","prediction")


import pyspark.pandas as pd
pandasDF = results.toPandas()
print(pandasDF)


import pymongo 
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["test"]
mycol = mydb["weather"]

dict1 = pandasDF.to_dict('split')
print(dict1)

x = mycol.insert_one(dict1)
print(x)








































