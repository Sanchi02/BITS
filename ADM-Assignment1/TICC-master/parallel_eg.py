from pyspark import SparkConf
from pyspark import SparkContext,SparkFiles

#sys.path.insert(0,SparkFiles.getRootDirectory())
HDFS_MASTER = '172.18.16.108'

conf = SparkConf()
#conf.setMaster('yarn-client')
conf.setAppName('spark-wordcount')
#conf.set('spark.executor.instances', 2)
sc = SparkContext(conf=conf)

sc.addPyFile("TICC-master/TICC_solver_1.py")

from TICC_solver import TICC
import numpy as np
import sys
distFile = sc.textFile('file:////usr/local/spark/example_data.txt'.format(HDFS_MASTER)) #file:///


ticc = TICC(window_size=1, number_of_clusters=8, lambda_parameter=11e-2, beta=600, maxIters=100, threshold=2e-5,
            write_out_file=False, prefix_string="output_folder/", num_proc=1)

squares = distFile.map(ticc.predict_clusters)
print("Number of partitions: {}".format(squares.getNumPartitions()))
print("Partitioner: {}".format(squares.partitioner))
print("Partitions structure: {}".format(squares.glom().collect()))
result = squares.collect()
print(result)