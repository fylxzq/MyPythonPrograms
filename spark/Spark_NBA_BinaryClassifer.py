from pyspark import SparkContext,SparkConf
from  pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.functions import col
from pyspark.ml.feature import StringIndexer,OneHotEncoder,VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import ParamGridBuilder,TrainValidationSplit
from pyspark.ml.tuning import CrossValidator

conf = SparkConf().setAppName("fy").setMaster("local[*]")
sc = SparkContext(conf=conf)
spark = SparkSession.builder.master('local').appName('test').getOrCreate()

row_df = spark.read.format("csv").option("header","true").option("delimiter",",").option('inferschema','true').load("inputData/machine_data.csv")
train_df,test_df = row_df.randomSplit([0.7,0.3])

assemblerInputs = train_df.columns[1:-1]
print(assemblerInputs)
assemblers = VectorAssembler(inputCols=assemblerInputs,outputCol='features')
model = DecisionTreeClassifier(featuresCol='features',labelCol='label')
pipeline = Pipeline(stages=[assemblers,model])
pipelineModel = pipeline.fit(train_df)
predicted = pipelineModel.transform(test_df)
evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction",labelCol="label",metricName="areaUnderROC")
AUC1 = evaluator.evaluate(predicted)
print(AUC1)
paraGrid = ParamGridBuilder().addGrid(model.impurity,["gini","entropy"]).addGrid(model.maxBins,[10,15,20]).\
     addGrid(model.maxDepth,[5,10,15]).build()
tvs = TrainValidationSplit(estimator=model,evaluator=evaluator,estimatorParamMaps=paraGrid,trainRatio=0.8)
tvs_pipeline = Pipeline(stages=[assemblers,model,tvs])
print(train_df.show(5))
tvs_pipelineModel = tvs_pipeline.fit(train_df)
bestModel = tvs_pipelineModel.stages[1].bestModel
predictions = tvs_pipelineModel.transform(test_df)
AUC2 = evaluator.evaluate(predictions)
print(AUC2)