from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql.functions import col
import matplotlib.pyplot as plt

spark = SparkSession.builder.master("local").appName("fy").getOrCreate()
raw_df = spark.read.format("csv").option("dilimiter",",").option("header","true").load("inputData/women.csv")
df = raw_df.select([col(column).cast("float") for column in raw_df.columns[1:3]])

assemblerInput = ["height"]
assembler = VectorAssembler(inputCols=assemblerInput,outputCol="features")
model = LinearRegression(featuresCol="features",labelCol="weight")
pipeline = Pipeline(stages=[assembler,model])
pipelineModel = pipeline.fit(df)
print(pipelineModel.stages[1].coefficients)
print(pipelineModel.stages[1].intercept)

predicted = pipelineModel.transform(df)
pddf = predicted.toPandas()
fig,ax = plt.subplots(figsize=(16,8))
ax.scatter(pddf["height"],pddf["weight"],c="red")
ax.scatter(pddf["height"],pddf["prediction"],c="blue")
ax.set_xlabel("height")
ax.set_ylabel("weight")
ax.legend()
plt.show()