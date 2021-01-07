import json
from datetime import datetime
from copy import deepcopy

def fileCleaner(filePtrs):
	for f in filePtrs:
		#f.write(']')
		f.close()

def JSONWriter(data,filePtr):		
	JSONdump = json.dumps(data)
	filePtr.write(JSONdump)
	filePtr.write('\n')
	
def reviewsExtractor(reviews):
	reviewArr = []
	reviewsMetaData = reviews[0]
	reviews = reviews[1:]
	# start = reviewsMetaData.index('al:')
	# end = reviewsMetaData.index('down')
	# numReviews = int(reviewsMetaData[start+4:end])
	for r in reviews:
		reviewItem = {}
		if(len(r)> 5):
			custInd = r.index("cutomer")
			dateR = r[5:custInd-2]
			ratingIndex = r.index("rating")
			customer = r[custInd+9:ratingIndex-2]
			votesIndex = r.index("votes")
			rating = r[ratingIndex+8:votesIndex-2]
			helpfulIndex = r.index("helpful")
			votes = r[votesIndex+9:helpfulIndex-2]
			helpful = r[helpfulIndex+11:]

			reviewItem = {"date":dateR, "customer":customer, "rating":rating, "votes":votes, "helpful":helpful}
			reviewArr.append(reviewItem)
	return reviewArr


def categoryParser(catArr):
	categories = []
	for c in catArr:
		tmp = c
		while(tmp.count('|') > 0):
			startLoc = tmp.index('|')
			endLoc = tmp.index('[')
			cat = tmp[startLoc+1:endLoc]
			if cat not in categories:
				categories.append(cat)
			tmp = tmp[endLoc+2:]
	return categories

def prodExtracter(prod,jsonFileProd):
	data = prod.splitlines()
	itemDict = {}
	
	if(len(data) > 4): #else Discontinued prod
		itemDict.update({"ProductID":int(data[0][3:])})
		itr = 1
		itemDict.update({"ASIN":data[itr].split(":")[1]})
		itr += 1
		itemDict.update({"title":data[itr].split(":")[1]})
		itr += 1
		itemDict.update({"group":data[itr].split(":")[1]})
		itr += 1
		itemDict.update({"salesrank":data[itr].split(":")[1]})
		itr += 1
		tmp = data[itr].split(":")[1]
		tmp = tmp.split("  ")[1:]
		itemDict.update({"similar":tmp})
		itr += 1
		
		#Processing categories
		numCat = int(data[itr].split(":")[1])
		itr += 1
		catArr = []
		for _ in range(numCat):
			catArr.append(data[itr])
			itr += 1
		categories = categoryParser(catArr)
		itemDict.update({"categories":categories})
		reviews = reviewsExtractor(data[itr:])
		itemDict.update({"reviews":reviews})
		JSONWriter(itemDict,jsonFileProd)

file_name = "metaModified7500.txt"
nextProdFlag = False
product = ""

jsonFileProd = open("product_modified_7500_hadoop.json","a")
#jsonFileProd.write('[')

with open(file_name,errors='ignore') as f:
	for line in f:
		if(line.count("Id:")>0 and len(line)<16):
			nextProdFlag = True
		else:
			nextProdFlag = False

		if(nextProdFlag == True):
			prodExtracter(product,jsonFileProd)
		if(nextProdFlag==False):
			product += line
		else:
			product = line
		
	prodExtracter(product,jsonFileProd)

fileCleaner([jsonFileProd])



