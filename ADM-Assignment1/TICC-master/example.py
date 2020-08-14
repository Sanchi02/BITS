

import numpy as np
import sys
from pyspark import SparkConf
from pyspark import SparkContext,SparkFiles


#sys.path.insert(0,SparkFiles.getRootDirectory())
#HDFS_MASTER = '172.18.16.108'

conf = SparkConf()
#conf.setMaster('yarn-client')
conf.setAppName('spark-TICC')
#conf.set('spark.executor.instances', 2)
sc = SparkContext(conf=conf)

sc.addPyFile("TICC-master/TICCsolver.py")

from TICCsolver import TICC

fname = "example_data.txt"
ticc = TICC(window_size=1, number_of_clusters=8, lambda_parameter=11e-2, beta=600, maxIters=50, threshold=2e-5,
            write_out_file=False, prefix_string="output_folder/", num_proc=1)


(cluster_assignment, cluster_MRFs) = ticc.fit(input_file=fname,sc=sc)


print(cluster_assignment)
# print("The tuple in xample.py")
# print(len(cluster_MRFs))
# print(type(cluster_MRFs))
# for key, value in cluster_MRFs.items() :
#     print(key)
#     print(value)
#     print(len(value))
np.savetxt('Results.txt', cluster_assignment, fmt='%d', delimiter=',')
