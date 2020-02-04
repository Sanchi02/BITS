#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

wine=datasets.load_wine();
X=wine.data
Y=wine.target


# In[13]:


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=42)
selection = np.random.choice(X_train.shape[0], size=3, replace=False)
X1=pd.DataFrame(X_train)
Y1=pd.DataFrame(y_train)
X2=X1.iloc[selection,:]
Y2=Y1.iloc[selection,:]
X1=X1.drop(X1.index[selection])
Y1=Y1.drop(Y1.index[selection])

model=RandomForestClassifier()
model.fit(X2,Y2)
model.score(X_test,y_test)


# In[14]:


def marSampling1(proba):
    part = np.partition(-proba, 1, axis=1)
    margin = - part[:, 0] + part[:, 1]
    return margin


# In[15]:


from sklearn.metrics import accuracy_score


# In[16]:


def uncer(x):
 prob_dist = model.predict_proba(x)
 margin1 = marSampling1(prob_dist)
 marg=pd.DataFrame(margin1)
 c=marg.nsmallest(4,0) 
 sel=list(c.index)
 return sel
 
i=0
while i<=2:
    newset=uncer(X1)
    nx=X1.iloc[newset,:]
    ny=Y1.iloc[newset,:]
    X2=X2.append(nx)
    Y2=Y2.append(ny)
    X1=X1.drop(X1.index[newset])
    Y1=Y1.drop(Y1.index[newset])
    model.fit(X2,Y2)
    i=i+1
    


# In[17]:


model.score(X_test,y_test)


# # Query by committee

# In[18]:


from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from  sklearn import datasets
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import math
import numpy as np
import pandas as pd

def getModelPredictions(X, y, model, testSize):
    x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=testSize,random_state=2)
    model.fit(x_train,y_train)
    predictions=model.predict(x_test)
    return predictions

classifiers = [
    KNeighborsClassifier(3),
    NuSVC(probability=True),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    AdaBoostClassifier(),
    GradientBoostingClassifier(),
    GaussianNB(),
    LinearDiscriminantAnalysis(),
    QuadraticDiscriminantAnalysis()]

wine=datasets.load_wine()
x=wine.data
y=wine.target

prob_dist = []
for classifier in classifiers:
    prob_dist.append(getModelPredictions(x,y,classifier, 0.85))
    
instance_tmp = []
looper = len(prob_dist[0])
for i in range(looper):
    tmp = []
    for j in range(len(prob_dist)):
        tmp.append(prob_dist[j][i])
    instance_tmp.append(tmp)

def getEntropy(votes, classes):
    total_votes = []
    voters = len(votes)
    val_sub = 0
    for i in range(classes):
        if(votes.count(i)==0):
            break
        tmp = (votes.count(i))/voters
        tmp = math.log(tmp)*tmp
        val_sub += tmp
    val_sub = 1 - val_sub
    return val_sub

for i in instance_tmp:
    print(getEntropy(i,3))
    


# In[19]:


X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.30, random_state=42)
selection = np.random.choice(X_train.shape[0], size=3, replace=False)
X1=pd.DataFrame(X_train)
Y1=pd.DataFrame(y_train)
X2=X1.iloc[selection,:]
Y2=Y1.iloc[selection,:]
X1=X1.drop(X1.index[selection])
Y1=Y1.drop(Y1.index[selection])

model=RandomForestClassifier()
model.fit(X2,Y2)
model.score(X_test,y_test)


# In[23]:


def getIndex(x):
    prob_dist = model.predict_proba(x)
    margin1 = marSampling1(prob_dist)
    marg=pd.DataFrame(margin1)
    c=marg.nlargest(5,0) 
    sel=list(c.index)
    return sel
 
for i in range(3):
    newset=getIndex(X1)
    nx=X1.iloc[newset,:]
    ny=Y1.iloc[newset,:]
    X2=X2.append(nx)
    Y2=Y2.append(ny)
    X1=X1.drop(X1.index[newset])
    Y1=Y1.drop(Y1.index[newset])
    model.fit(X2,Y2)

model.score(X_test,y_test)


# # Diversity sampling

# In[114]:


from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.metrics import pairwise_distances
from sklearn.cluster import KMeans
import numpy as np
from random import seed
from random import randint
import pandas as pd

seed(5)
def getMinDistances(distances):
    dist = []
    for d in distances:
        tmp = []
        tmp.append(abs(d[0]-d[1]))
        tmp.append(abs(d[1]-d[2]))
        tmp = abs(tmp[0]-tmp[1])
#         print(tmp)
        dist.append(tmp)
    return dist
    

wine=datasets.load_wine()
x=wine.data
y=wine.target
X_train,X_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=2)

selection = np.random.choice(X_train.shape[0], size=3, replace=False)
X1=pd.DataFrame(X_train)
Y1=pd.DataFrame(y_train)
X2=X1.iloc[selection,:]
Y2=Y1.iloc[selection,:]
X1=X1.drop(X1.index[selection])
Y1=Y1.drop(Y1.index[selection])

model=RandomForestClassifier()
model.fit(X2,Y2)
model.score(X_test,y_test)

kmeans = KMeans(n_clusters=3, random_state=0).fit(X1)
distances = pairwise_distances(X1,kmeans.cluster_centers_)
# X_trainDF = X1.copy()
d = getMinDistances(distances)
# print(d)
X1['Diversity'] =d
# X_trainDF['Diversity'] = d
# X_trainDF = X_trainDF.sort_values('Diversity')
# print(X_trainDF)
X1.sort_values('Diversity')
def diversity_index(X_trainDF):
    lenDF = len(X_trainDF)
    lenDF = lenDF//3
    indexes=[]
    start = 0
    last = lenDF
    indexesToTrain = []
    for i in range(3):
        r = randint(0,lenDF-1)
        tmpDF = X_trainDF.iloc[start:last,:]
        start = last
        last += lenDF
        indexesToTrain.append((tmpDF.iloc[r:r+1,:]).index[0])
        r = randint(0,lenDF-1)
        indexesToTrain.append((tmpDF.iloc[r:r+1,:]).index[0])
    return indexesToTrain

print(X1.columns)
# X1.drop('Diversity')
X1 = X1.iloc[:,0:13]
print(X1)


# In[115]:



for i in range(3):
    newset=diversity_index(X1)
    nx=X1.iloc[newset,:]
    ny=Y1.iloc[newset,:]
    X2=X2.append(nx)
    Y2=Y2.append(ny)
    X1=X1.drop(X1.index[newset])
    Y1=Y1.drop(Y1.index[newset])
    model.fit(X2,Y2)

model.score(X_test,y_test)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




