#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn import datasets
from sklearn.model_selection import train_test_split
import pandas as pd
import warnings
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)


# In[2]:


#import wine dataset
wine = datasets.load_wine()


# In[3]:


X = wine.data
Y = wine.target


# In[4]:


#split data for test and train
X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.25,random_state=3)


# In[5]:


from sklearn.cluster import KMeans
import numpy as np


# In[6]:


#cluster training data


# In[7]:


c=2


# In[8]:


kmeans = KMeans(n_clusters=c, random_state=0).fit(X_train)


# In[9]:


clusters=pd.DataFrame(X_train)
clusters['labels']=kmeans.labels_
a=[]
#split data based on labels
for i in range(0,c):
    a.append(clusters[clusters['labels']==i])
   


# In[ ]:





# In[10]:


#randomly pick points to label from each cluster


# In[11]:


import random
random.seed(100) 
r=[]


# In[12]:


for i in range(0,c):
    r.append(random.sample(list(a[i].index),k=10))


# In[13]:


#quering randomly selected instances
labels=[]
l1=[]
for i in range(0,c):
    labels.append(y_train[r[i]])
    l1.append(np.bincount(labels[i]).argmax())


# In[14]:


q_index=[]
for i in range(0,c):
    q_index.append(a[i].index.isin(r[i]))


# In[15]:


a2=[]


# In[16]:


#get labels for those points from dataset(oracle)


# In[17]:



for j in range(0,c):
    a2.append(a[j].copy())
    for i in a2[j][q_index[j]].index:
         a2[j].loc[i,'labels'] = y_train[i]


# In[18]:


#assigning values for others(same as majority of those randomly chosen points)
for i in range(0,c):
    a2[i].loc[~q_index[i],'labels'] = l1[i]



# In[19]:


for i in range(1,c):
    a2[0]=pd.concat([a2[0],a2[i]],axis=0)
X_new=a2[0]
X_new=X_new.sort_index()


# In[20]:


#Number of points labelled correctly after clustering 


# In[21]:


correct=len(np.where(X_new.labels==y_train)[0])
acc=correct/len(X_new)
print("Percentage of correctly labeled with random sampling: ")
print(acc*100)


# In[22]:


#x any y values to fit classifier
X_train1=X_new.iloc[:,:13]
X_train1
y_train1=X_new['labels']
y_train1


# In[ ]:





# In[23]:


# Sampling centroids and points nearby


# In[24]:


centroids=kmeans.cluster_centers_


# In[25]:


from sklearn.metrics import pairwise_distances_argmin_min
label,distances= pairwise_distances_argmin_min(X_train,kmeans.cluster_centers_)


# In[26]:


#ditances from cluster centroids
clusters['distance']=distances


# In[27]:


a1=[]
#split data based on labels
for i in range(0,c):
    a1.append(clusters[clusters['labels']==i])
    


# In[28]:


r1=[]
for i in range(0,c):
    r1.append(a1[i].sort_values('distance').head(10).index)


# In[29]:


labels1=[]
l11=[]
for i in range(0,c):
    labels1.append(y_train[r1[i]])
    l11.append(np.bincount(labels1[i]).argmax())


# In[30]:


q_index1=[]
for i in range(0,c):
    q_index1.append(a1[i].index.isin(r1[i]))


# In[31]:


a3=[]


# In[32]:


for j in range(0,c):
    a3.append(a1[j].copy())
    for i in a3[j][q_index1[j]].index:
         a3[j].loc[i,'labels'] = y_train[i]


# In[33]:


for i in range(0,c):
    a3[i].loc[~q_index1[i],'labels'] = l11[i]



# In[34]:


for i in range(1,c):
    a3[0]=pd.concat([a3[0],a3[i]],axis=0)
X_new1=a3[0]
X_new1=X_new1.sort_index()


# In[35]:


correct=len(np.where(X_new1.labels==y_train)[0])
acc=correct/len(X_new1)
print("Percentage of correctly labeled with points near centroid: ")
print(acc*100)


# In[36]:


X_train2=X_new1.iloc[:,:13]
X_train2
y_train2=X_new1['labels']
y_train2


# In[37]:


#Fit Fully labeled data to the classifier


# In[38]:


from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
model.fit(X_train1,y_train1)
model.score(X_train1,y_train1)
y_pred1=model.predict(X_test)


# In[39]:


model1 = RandomForestClassifier()
model1.fit(X_train2,y_train2)
model1.score(X_train2,y_train2)
y_pred2=model1.predict(X_test)


# In[40]:


from sklearn import metrics
print("Accuracy with Random Sampling:")
print(metrics.accuracy_score(y_test, y_pred1)*100)
print("Accuracy with points near the centroid of the cluster")
print(metrics.accuracy_score(y_test, y_pred2)*100)


# In[ ]:





# In[ ]:




