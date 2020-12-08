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
row_df = spark.read.format("csv").option("header","true").option("delimiter","\t").load("inputData/train.tsv")
def replcae_question(x):
    return ("0" if x=="?" else x)
replcae_question = udf(replcae_question)
df = row_df.select(["url","alchemy_category"]+[replcae_question(col(column)).cast("double").alias(column) for column in row_df.columns[4:]])
train_df,test_df = df.randomSplit([0.7,0.3])
print(df)
# stringIndexer = StringIndexer(inputCol="alchemy_category",outputCol="alchemy_category_indexer")
# encoder = OneHotEncoder(inputCol="alchemy_category_indexer",outputCol="alchemy_category_indexer_vec")
# assemblerInputs = ["alchemy_category_indexer_vec"] + row_df.columns[4:-1]
# assembler = VectorAssembler(inputCols=assemblerInputs,outputCol="features")
# model = DecisionTreeClassifier(labelCol="label",featuresCol="features",maxDepth=10,impurity="gini",maxBins=14)
# pipeline = Pipeline(stages=[stringIndexer,encoder,assembler,model])
#
# pipelineModel = pipeline.fit(train_df)
# predicted = pipelineModel.transform(test_df)
# evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction",labelCol="label",metricName="areaUnderROC")
# AUC1 = evaluator.evaluate(predicted)
#
# paraGrid = ParamGridBuilder().addGrid(model.impurity,["gini","entropy"]).addGrid(model.maxBins,[10,15,20]).\
#     addGrid(model.maxDepth,[5,10,15]).build()
# tvs = TrainValidationSplit(estimator=model,evaluator=evaluator,estimatorParamMaps=paraGrid,trainRatio=0.8)
# tvs_pipeline = Pipeline(stages=[stringIndexer,encoder,assembler,model,tvs])
# tvs_pipelineModel = tvs_pipeline.fit(train_df)
# bestModel = tvs_pipelineModel.stages[3].bestModel
# predictions = tvs_pipelineModel.transform(test_df)
# AUC2 = evaluator.evaluate(predictions)



