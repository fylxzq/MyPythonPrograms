from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import  BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator
from pyspark.ml.tuning import ParamGridBuilder
from pyspark.ml import Pipeline
spark = SparkSession.builder.master("local").appName("fy").getOrCreate()
raw_df = spark.read.format("csv").option("delimiter",",").option("header","true").load("inputData/InfantBirths.csv")
df = raw_df.select([col(column).cast("int") for column in raw_df.columns[0:17]])
train_df,test_df = df.randomSplit([0.7,0.3])

assemberInput = df.columns[1:17]
assembler = VectorAssembler(inputCols=assemberInput,outputCol="features")
model = LogisticRegression(featuresCol="features",labelCol="INFANT_ALIVE_AT_REPORT")
evaluator = BinaryClassificationEvaluator(labelCol="INFANT_ALIVE_AT_REPORT",rawPredictionCol="rawPrediction",metricName="areaUnderROC")
paraGrid = ParamGridBuilder().addGrid(model.maxIter,[2,5,10]).addGrid(model.regParam,[0.01,0.05,0.3]).build()
cv = CrossValidator(estimator=model,evaluator=evaluator,numFolds=3,estimatorParamMaps=paraGrid)
cvpipeline  = Pipeline(stages=[assembler,cv])

cvpipelineModel = cvpipeline.fit(train_df)
prediction = cvpipelineModel.transform(test_df)
AUC = evaluator.evaluate(prediction)
print("AUC",AUC)

