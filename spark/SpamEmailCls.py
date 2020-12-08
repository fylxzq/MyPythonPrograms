from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import HashingTF
from pyspark.ml.feature import IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline

spark = SparkSession.builder.appName("fy").master("local").getOrCreate()

raw_df_train = spark.read.format("csv").option("header","false").option("delimiter",",").load("/input/SpamEmail/SpamEmail-training.csv")
train_df = raw_df_train.select(raw_df_train["_c0"].alias("email"),raw_df_train["_c1"].alias("content"),raw_df_train["_c2"].alias("label").cast("int"))
raw_df_test = spark.read.format("csv").option("header","false").option("delimiter",",").load("/input/SpamEmail/SpamEmail-test.csv")
test_df = raw_df_test.select(raw_df_test["_c0"].alias("email"),raw_df_test["_c1"].alias("content"))

tokenizer = Tokenizer(inputCol="content",outputCol="words")
hashTF = HashingTF(inputCol="words",outputCol="rawfeatures")
idf = IDF(inputCol="rawfeatures",outputCol="features")
model = LogisticRegression(featuresCol="features",labelCol="label")
pipeline = Pipeline(stages=[tokenizer,hashTF,idf,model])

pipelineModel = pipeline.fit(train_df)
prediction = pipelineModel.transform(test_df)
prediction.select("prediction").write.csv("/output/SpamEmail",header=True,mode="overwrite")