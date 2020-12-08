from pyspark import SparkContext,SparkConf
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.evaluation import RegressionMetrics
import numpy as np
conf = SparkConf().setMaster("local[*]").setAppName("fy")
sc = SparkContext(conf=conf)
rawData = sc.textFile("D:/百度网盘/下载/data/train.csv")
header = rawData.first()
data = rawData.filter(lambda x:x != header).map(lambda x:x.split(","))

label = data.map(lambda x:int(x[-1]))
labelPointRDD  = data.map(lambda x:(x[-1],x[1:-1])).map(lambda x:(x[0],[float(y) for y in x[1]])).map(lambda x:LabeledPoint(x[0],Vectors.dense(x[1])))
(train,test) = labelPointRDD.randomSplit([0.7,0.3])
model = DecisionTree.trainRegressor(train,categoricalFeaturesInfo={},maxDepth=10)

prediction = model.predict(test.map(lambda x:x.features)).collect()
trueValue = test.map(lambda x:x.label).collect()
scoreAndLabel = [[pre,tValue] for pre,tValue in zip(prediction,trueValue)]
rdd_scoreAndLable = sc.parallelize(scoreAndLabel)
ev = RegressionMetrics(rdd_scoreAndLable)

rmse = np.sqrt(ev.meanSquaredError)
print("rmse的值为:",rmse)
