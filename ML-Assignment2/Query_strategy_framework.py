#!/usr/bin/env python
# coding: utf-8

# # Uncertainty sampling - Margin

# In[1]:


from  sklearn import datasets


# In[2]:


def getModelAccuracy(X, y, model, testSize):
    x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=testSize,random_state=2)
    model.fit(x_train,y_train)
    predictions=model.predict(x_test)
    return model.predict_proba(x_test)
    


# In[3]:


def getModelPredictions(X, y, model, testSize):
    x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=testSize,random_state=2)
    model.fit(x_train,y_train)
    predictions=model.predict(x_test)
    return predictions


# In[4]:


import numpy as np

# https://modal-python.readthedocs.io/en/latest/content/query_strategies/uncertainty_sampling.html
def marSampling1(proba):
    part = np.partition(-proba, 1, axis=1)
    margin = - part[:, 0] + part[:, 1]
    return margin


# In[5]:


from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

wine=datasets.load_wine()
x=wine.data
y=wine.target
prob_dist = getModelAccuracy(x,y,RandomForestClassifier(), 0.85)
margin1 = marSampling1(prob_dist)

print(margin1)


# # Query by committee

# In[6]:


from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


# In[7]:


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


# In[8]:


wine=datasets.load_wine()
x=wine.data
y=wine.target

prob_dist = []
for classifier in classifiers:
    prob_dist.append(getModelPredictions(x,y,classifier, 0.85))


# In[9]:


instance_tmp = []
looper = len(prob_dist[0])
for i in range(looper):
    tmp = []
    for j in range(len(prob_dist)):
        tmp.append(prob_dist[j][i])
    instance_tmp.append(tmp)


# In[10]:


import math

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


# In[11]:


for i in instance_tmp:
    print(getEntropy(i,3))


# # Diversity Sampling

# In[12]:


from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.metrics import pairwise_distances
from sklearn.cluster import KMeans
import numpy as np

wine=datasets.load_wine()
x=wine.data
y=wine.target
X_train,X_test,y_train,y_test=train_test_split(x,y,test_size=0.5,random_state=2)

kmeans = KMeans(n_clusters=3, random_state=0).fit(X_train)
distances = pairwise_distances(X_train,kmeans.cluster_centers_)


# In[13]:


def getMinDistances(distances):
    for d in distances:
        tmp = []
        tmp.append(abs(d[0]-d[1]))
        tmp.append(abs(d[1]-d[2]))
        tmp = abs(tmp[0]-tmp[1])
        


# In[14]:


getMinDistances(distances)


# In[ ]:




