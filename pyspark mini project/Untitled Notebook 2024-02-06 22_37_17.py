# Databricks notebook source
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,StringType,IntegerType
from pyspark.sql.functions import *

# COMMAND ----------

df=spark.read.load('/FileStore/tables/googlestore-1.csv',format='csv',sep=',',header='true',escape='"',inferschema='true')

# COMMAND ----------

df.count()

# COMMAND ----------

df.show()

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df = df.drop('Size','Content Rating','Last Updated','Android Ver','Current Ver')

# COMMAND ----------

df.show(2)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import regexp_replace,col

df = df.withColumn("Reviews",col("Reviews").cast(IntegerType()))\
    .withColumn("Installs",regexp_replace(col("Installs"),"[^0-9]",""))\
    .withColumn("Installs",col("Installs").cast(IntegerType()))\
        .withColumn("Price",regexp_replace(col("Price"),"[$]",""))\
            .withColumn("Price",col("Price").cast(IntegerType()))


# COMMAND ----------

df.show(5)

# COMMAND ----------

df.createOrReplaceTempView("apps")

# COMMAND ----------

# MAGIC %sql SELECT * FROM apps

# COMMAND ----------

# DBTITLE 1,Top Reviewed Apps by users
# MAGIC %sql SELECT App,SUM(Reviews) FROM apps GROUP BY 1 ORDER BY 2 DESC

# COMMAND ----------

# DBTITLE 1,Top 10 Installed Apps by users
# MAGIC %sql SELECT App,SUM(Installs) FROM apps GROUP BY 1 ORDER BY 2 DESC

# COMMAND ----------

# DBTITLE 1,Category wise Distribution
# MAGIC %sql SELECT Category,SUM(Installs) FROM apps
# MAGIC GROUP BY 1 ORDER BY 2 DESC

# COMMAND ----------

# DBTITLE 1,Top Paid Apps
# MAGIC %sql SELECT App,SUM(Price) FROM apps WHERE Type='Paid'
# MAGIC GROUP BY 1 ORDER BY 2 DESC

# COMMAND ----------


