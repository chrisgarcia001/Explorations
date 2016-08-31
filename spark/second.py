from os import sys
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("TestApp1")
sc = SparkContext(conf=conf)

path = sys.argv[1] if len(sys.argv) > 1 else "./"
 
docs = sc.wholeTextFiles(path)

#results = docs.map(lambda (x,y): y).reduce(lambda x,y: x + y)
# print("\n\n Results" + str(results) + "\n\n")

results = docs.map(lambda (x,y): (x, len(y))).collect()

for res in results:
	print(res)

sc.stop()

