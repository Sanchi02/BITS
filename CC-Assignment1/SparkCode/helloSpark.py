import pyspark
from pyspark.sql import *
import time
from copy import deepcopy
import json

def havingProcessor(x):
    # print("in hving processor f2op={}, f2Val={}, x[1]={}".format(f2op,f2Val,x[1]))
    if(f2op == '<'):
        return (int(x[1]) < int(f2Val))
    elif(f2op == '>'):
        return (int(x[1]) > int(f2Val))
    elif(f2op == '='):
        return (int(x[1]) == int(f2Val))
    return False

# def havingProcessorCat(x):
#     if(f2op == '<'):
#         return (int(x[1]) < int(f2Val))
#     elif(f2op == '>'):
#         return (int(x[1]) > int(f2Val))
#     elif(f2op == '='):
#         return (int(x[1]) == int(f2Val))


def havingPreProcessor(x):
    if(opMeta=='COUNT'):
        return(x[0],1)
    else:
        return (x[0],int(x[1][1]))

def selectProcessor(x):
    # print("colsTBDisplayed=^{}^,f1op=^{}^,f1Col=^{}^".format(colsTBDisplayed,f1op,f1Col))
    colMapper = {"ASIN":0, "ProductID":1, "categories":2, "reviews":3, "salesrank":4, "similar":5, "title":6}
    arrToVal = []
    for c in colsTBDisplayed:
        # print(c)
        if(c not in colMapper):
            arrToVal.append(x[0])
        else:
            arrToVal.append(x[1][colMapper.get(c)])

    if(f1Col in colMapper):
        arrToVal.append(x[1][colMapper.get(f1Col)])
    else:
        arrToVal.append(x[0])
    return (x[0], arrToVal)

def whereClauseProcessorCat(x):
    # print(x[2])
    if(str(conditionVal) in x[2]):
        return True
    return False

def groupByProcessor(x):
    # groupByCol
    colMapper = {"ASIN":0, "ProductID":1, "categories":2, "group":3, "reviews":4, "salesrank":5, "similar":6, "title":7}
    indexG = colMapper.get(groupByCol)
    tmp = x[0:indexG] + x[indexG+1:]
    return (x[indexG], tmp)

def whereClauseProcessor(x):
    # conditionCol,op,conditionVal
    # print(conditionCol)
    colMapper = {"ASIN":0, "ProductID":1, "categories":2, "group":3, "reviews":4, "salesrank":5, "similar":6, "title":7}
    indexCol = colMapper.get(conditionCol)
    # print("In where clause processor conditionVal={}, indexCol={}, op={}".format(conditionVal, indexCol, op))
    # print(x)
    if(op == '<'):
        return(int(x[indexCol]) < int(conditionVal))
    elif(op == '>'):
        return (int(x[indexCol]) > int(conditionVal))
    elif(op == '='):
        if(conditionVal.isNumeric()):
            return (int(x[indexCol]) == int(conditionVal))
        else:
            return (x[indexCol] == conditionVal)
    return False


sc = pyspark.SparkContext('local[*]')
spark= SparkSession.builder.getOrCreate()

rddProd = spark.read.json('/home/subh/cctemp/spark/product_modified_7500.json')
rddProd = rddProd.rdd.map(list)

# Query processor
queryFile = open('/home/subh/cctemp/query.txt','r')
query = queryFile.read()
# print(query)
colsTBDisplayed = query[7:query.index('FROM')-1].split(',')
function1 = colsTBDisplayed.pop()
condition = query[query.index('WHERE')+6:query.index('GROUP BY')-1]
groupByCol = query[query.index('GROUP BY')+9:query.index('HAVING')-1]
function2 = query[query.index(' HAVING')+7:]

flag = False
if(condition.count('categories')>0):
    flag = True
# print("colsTBDisplayed = {}, function1 = {}, condition = {}, groupByCol = {}, function2 = {}".format(colsTBDisplayed,function1,condition,groupByCol,function2))

op = ['<','>','=']
for o in op:
    if(condition.count(o)>0):
        op = o
        break

breaker = condition.index(op)
conditionCol = condition[:breaker-1]
conditionVal = condition[breaker+2:]

# print("ConditionCol =ab{}ab, op={}, condtionVal =ab{}ab".format(conditionCol,op,conditionVal))
opMeta = ['COUNT','MIN','MAX','SUM']
for o in opMeta:
    if(function1.count(o)>0):
        opMeta = o
        break

breaker1 = function1.index('(')
colName = function1[breaker1+1:len(function1)-1]
# print("function name = ^{}^, functionCol=^{}^".format(op,colName))
f1op,f1Col = opMeta,colName
# print(f1op)
# print("function2 = {}".format(function2))
op2 = ['<','>','=']
for o in op2:
    if(function2.count(o)>0):
        op2 = o
        break

f2op, f2Val = op2,function2[function2.index(op2)+1:]
# print("Function name for having f2op = {}, f2Val={} ".format(f2op,f2Val))

if(flag):
    conditionCol = condition[:breaker]
    conditionVal = condition[breaker+2:len(condition)]
    #print(conditionCol)
    #print(conditionVal)

if(flag==False):
    if(opMeta=='COUNT'  or opMeta=="SUM"):
        start_time = time.time()
        pairs = rddProd.filter(whereClauseProcessor).map(groupByProcessor).map(selectProcessor).map(havingPreProcessor)
        intermediate = pairs.take(pairs.count())
        pairs = pairs.reduceByKey(lambda x, y: x + y).filter(havingProcessor)
    elif(opMeta=='MAX'):
        start_time = time.time()
        pairs = rddProd.filter(whereClauseProcessor).map(groupByProcessor).map(selectProcessor).map(havingPreProcessor)
        intermediate = pairs.take(pairs.count())
        pairs = pairs.reduceByKey(lambda x, y: max(x,y)).filter(havingProcessor)
    elif(opMeta=='MIN'):
        start_time = time.time()
        pairs = rddProd.filter(whereClauseProcessor).map(groupByProcessor).map(selectProcessor).map(havingPreProcessor)
        intermediate = pairs.take(pairs.count())
        pairs = pairs.reduceByKey(lambda x, y: min(x,y)).filter(havingProcessor)
else:
    if(opMeta=='COUNT' or opMeta=="SUM"):
        start_time = time.time()
        pairs = rddProd.filter(whereClauseProcessorCat).map(groupByProcessor).map(selectProcessor).map(havingPreProcessor)
        intermediate = pairs.take(pairs.count())
        pairs = pairs.reduceByKey(lambda x, y: x + y).filter(havingProcessor)
    elif(opMeta=='MAX'):
        start_time = time.time()
        pairs = rddProd.filter(whereClauseProcessorCat).map(groupByProcessor).map(selectProcessor).map(havingPreProcessor)
        intermediate = pairs.take(pairs.count())
        pairs = pairs.reduceByKey(lambda x, y: max(x,y)).filter(havingProcessor)
    elif(opMeta=='MIN'):
        start_time = time.time()
        pairs = rddProd.filter(whereClauseProcessorCat).map(groupByProcessor).map(selectProcessor).map(havingPreProcessor)
        intermediate = pairs.take(pairs.count())
        pairs = pairs.reduceByKey(lambda x, y: min(x,y)).filter(havingProcessor)

#print(pairs.count())
#print(pairs.take(pairs.count()))
timeToE = time.time() - start_time
#print(timeToE)

jsonFileOp = open("/home/subh/cctemp/spark/sparkop.json","w")
outputJson = {"timeToE":timeToE, "output":str(pairs.take(pairs.count())), "intermediateOp":str(intermediate)}
JSONdump = json.dumps(outputJson)
jsonFileOp.write(JSONdump)
jsonFileOp.close()

