from pyspark.sql import SparkSession
from  pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler,VectorIndexer
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import TrainValidationSplit,ParamGridBuilder
from pyspark.ml.regression import GBTRegressor
from pyspark.ml.tuning import CrossValidator
spark = SparkSession.builder.master('local').appName("fy").getOrCreate()
hour_df = spark.read.format("csv").option("header","true").option("delimiter",",").load("D:/studyPython/inputData/hour.csv")
hour_df = hour_df.drop("instant").drop("dteday").drop("yr").drop("casual").drop("registered")
df = hour_df.select([col(column).cast("double").alias(column) for column in hour_df.columns])
train_df,test_df = df.randomSplit([0.7,0.3])

assemmblerInputs = df.columns[:-1]
assembler = VectorAssembler(inputCols=assemmblerInputs,outputCol="afeatures")
vectorIndexer = VectorIndexer(inputCol="afeatures",outputCol="features",maxCategories=24)
model = DecisionTreeRegressor(labelCol="cnt",featuresCol="features")
pipeline = Pipeline(stages=[assembler,vectorIndexer,model])

pipelineModel = pipeline.fit(train_df)
predicted_df = pipelineModel.transform(test_df)
evaluator = RegressionEvaluator(labelCol="cnt",predictionCol="prediction",metricName="rmse")
rmse = evaluator.evaluate(predicted_df)
print(rmse)

paraGrid = ParamGridBuilder().addGrid(model.maxDepth,[5,10,15,25])\
.addGrid(model.maxBins,[25,35,45,50])\
.build()
tvs = TrainValidationSplit(estimator=model,estimatorParamMaps=paraGrid,trainRatio=0.8,evaluator=evaluator)
tvs_pipeline = Pipeline(stages=[assembler,vectorIndexer,tvs])
tvs_pipelineModel = tvs_pipeline.fit(train_df)
predicted_df1 = tvs_pipelineModel.transform(test_df)
rmse1 = evaluator.evaluate(predicted_df1)

gbt = GBTRegressor(labelCol="cnt",featuresCol="features")
parmGrid1 = ParamGridBuilder().addGrid(gbt.maxDepth,[5,10]).addGrid(gbt.maxBins,[25,40]).addGrid(gbt.maxIter,[10,50]).build()
gbt_tvs = CrossValidator(estimator=gbt,estimatorParamMaps=parmGrid1,evaluator=evaluator,numFolds=3)
gbt_tvspipeline = Pipeline(stages=[assembler,vectorIndexer,gbt_tvs])
gbt_tvspipelineModel = gbt_tvspipeline.fit(train_df)
predicted_df2 = gbt_tvspipelineModel.transform(test_df)
rmse2 = evaluator.evaluate(predicted_df2)
print(rmse2)