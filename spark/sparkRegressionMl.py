from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.ml.evaluation import RegressionEvaluator
spark = SparkSession.builder.master("local").getOrCreate()
rawdata = spark.read.format("csv").option("header","true").load("/input/Reg/train.csv")
data = rawdata.select(rawdata.city.cast("double"),rawdata.hour.cast("int"),
                      rawdata.is_workday.cast("int"),rawdata.weather.cast("int"),
                      rawdata.temp_1.cast("double"),rawdata.temp_2.cast("double"),
                      rawdata.wind.cast('int'),rawdata.y.cast('int'))
assebler = VectorAssembler(inputCols=['city', 'hour', 'is_workday', 'weather', 'temp_1', 'temp_2', 'wind'],
                           outputCol="features")
output = assebler.transform(data)
label_features = output.select("features","y").toDF("features","label")
model = DecisionTreeRegressor(maxDepth=10)
(trainData,testData) = label_features.randomSplit([0.7,0.3])
model = model.fit(trainData)
predictions = model.transform(testData)
evaluator = RegressionEvaluator(predictionCol="prediction",labelCol="label",metricName="rmse")
rmse = evaluator.evaluate(predictions)
print(rmse)
prerdd = predictions.rdd
prerdd.saveAsTextFile("/output/Reg")
