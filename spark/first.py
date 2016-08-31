from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("TestApp1")
sc = SparkContext(conf=conf)

#distFile = sc.textFile("news20/20_newsgroup/rec.motorcycles/72052")
distFile = sc.textFile("news20/20_newsgroup/rec.motorcycles")
print("\n\n---Success!!!!!!!!!!!!!!!!!!!!!!!---\n\n")
lineLengths = distFile.map(lambda s: len(s))
totalLength = lineLengths.reduce(lambda a, b: a + b)
print("\n\nTotal Length: " + str(totalLength) + "\n\n")
