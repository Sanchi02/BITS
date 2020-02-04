#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
wine=datasets.load_wine();
X=wine.data
Y=wine.target
#print(X.shape)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=4)
#print(X_train.shape)
X_train1, X_test1, y_train1, y_test1 = train_test_split(X_train, y_train, test_size=0.98, random_state=4)
#print(X_train1.shape)
#print(y_train1.shape)


# In[2]:


from sklearn.ensemble import RandomForestClassifier
model=RandomForestClassifier()
model.fit(X_train1,y_train1)


# In[3]:


X_n=[]
Y_n=[]
i=0
while i<X_train1.shape[0]:
    X_n.append(X_train1[i])
    Y_n.append(y_train1[i])
    i=i+1


# In[4]:


def marSampling1(proba):
    part = np.partition(-proba, 1, axis=1)
    margin = - part[:, 0] + part[:, 1]
    return margin


# In[5]:


from sklearn.metrics import accuracy_score
def marg_samp(x):
 #print("In marg samp")
 #print(x.shape)
 prob_dist = model.predict_proba(x)
 margin1 = marSampling1(prob_dist)
 return margin1


# In[6]:


model.score(X_test,y_test)


# In[10]:


i=0
cnt=0
accura=0
#print(X_test1.shape)
while accura<0.80 and i<X_test1.shape[0]:
    x=X_test1[i]
    #print("x is ",x)
    #print(type(x))
    x = x.reshape(1,-1)
    accr=marg_samp(x)
    #print("accr is {}".format(accr))
    if accr[0]<0.5:
        X_n.append(X_test1[i])
        Y_n.append(y_test1[i])
        new_x=np.asarray(X_n)
        new_y=np.asarray(Y_n)
        model.fit(new_x,new_y)
        accura=model.score(X_test,y_test)
        cnt=cnt+1
    i=i+1
#print(cnt)


# In[11]:


model.score(X_test,y_test)


# In[ ]:





# In[ ]:





# In[ ]:




