#!/usr/bin/env python
# coding: utf-8

# Final combined and documented code.

# In[59]:

#Rollno 2019H1030519P 2019H1030520P 2019H1030521P


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn import metrics
import random
from scipy import fftpack


# In[60]:


data = pd.read_csv("qsar_fish_toxicity.csv",sep=';', 
                  names=["CIC0", "SM1_Dz","GATS1i", "NdsCH", "NdssC","MLOGP","LC50"])
data.head(10)


# In[61]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six

def render_mpl_table(data, col_width=3.5, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax

render_mpl_table(data.head(11), header_columns=0)


# In[62]:


linear_regression = linear_model.LinearRegression()


# In[63]:


X=data.drop(columns="LC50")
Y=data['LC50']


# In[64]:


#comparison measures
labels = []
rmse_values=[]
mae_values=[]
model_scores=[]


# In[65]:


test1 = 0.15
test2 = 0.25
test3 = 0.4


# In[66]:


# Simple Linear Regression -- Quantitative 25% test data
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test1, random_state=42)
model_linear_regression=linear_regression.fit(X_train, y_train)
pred = model_linear_regression.predict(X_test)

#score of model
print(linear_regression.score(X_train,y_train))

#coefficient of model
print(linear_regression.coef_)
#coefficient RMSE
print(np.sqrt(metrics.mean_squared_error(y_test,pred)))
print(metrics.mean_absolute_error(y_test,pred))
labels.append('Linear Regression' + str(test1) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,pred))
model_scores.append(linear_regression.score(X_train,y_train))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,pred)))
print(len(labels))


# In[67]:


def plotter(model_name, test, pred, split):
    fig, ax = plt.subplots()
    ax.scatter(test, pred)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    ax.title.set_text(model_name +'-' + str(split) + '%')
    plt.show()


# In[68]:


plotter("Linear Regression", y_test, pred, test1)


# In[69]:


fig, ax = plt.subplots()
ax.scatter(y_test, pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Linear Regression-' + str(test1) + '%')
plt.show()


# In[70]:


# Simple Linear Regression -- Quantitative 50% test data
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test2, random_state=42)
model_linear_regression=linear_regression.fit(X_train, y_train)
pred = model_linear_regression.predict(X_test)

#score of model
print(linear_regression.score(X_train,y_train))

#coefficient of model
print(linear_regression.coef_)
#coefficient RMSE
print(np.sqrt(metrics.mean_squared_error(y_test,pred)))
print(metrics.mean_absolute_error(y_test,pred))
labels.append('Linear Regression' + str(test2) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,pred))
model_scores.append(linear_regression.score(X_train,y_train))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,pred)))


# In[71]:


fig, ax = plt.subplots()
ax.scatter(y_test, pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured', fontweight='bold')
ax.set_ylabel('Predicted',fontweight='bold')
ax.title.set_text('Linear Regression-' + str(test2) + '%')
plt.show()


# In[72]:


# Simple Linear Regression -- Quantitative 75% test data
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test3, random_state=42)
model_linear_regression=linear_regression.fit(X_train, y_train)
pred = model_linear_regression.predict(X_test)

#score of model
print(linear_regression.score(X_train,y_train))

#coefficient of model
print(linear_regression.coef_)
#coefficient RMSE
print(np.sqrt(metrics.mean_squared_error(y_test,pred)))
print(metrics.mean_absolute_error(y_test,pred))
labels.append('Linear Regression-' + str(test3) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,pred))
model_scores.append(linear_regression.score(X_train,y_train))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,pred)))


# In[73]:


fig, ax = plt.subplots()
ax.scatter(y_test, pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Linear Regression-' + str(test3) + '%')
plt.show()


# In[74]:


#Polynomial basis 
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
poly_model = make_pipeline(PolynomialFeatures(3),linear_regression)
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test1, random_state=42)
poly_model.fit(X_train,y_train)
y_pred=poly_model.predict(X_test)
print(poly_model.score(X_train,y_train))

print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Polynomial basis Deg 3-' + str(test1) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
model_scores.append(poly_model.score(X_train,y_train))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))


# In[75]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Polynomial Regression Deg 3-' + str(test1) + '%')
plt.show()


# In[76]:


#Polynomial basis 
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
poly_model = make_pipeline(PolynomialFeatures(3),linear_regression)
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test2, random_state=42)
poly_model.fit(X_train,y_train)
y_pred=poly_model.predict(X_test)
print(poly_model.score(X_train,y_train))

print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Polynomial basis Deg 3-' + str(test2) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
model_scores.append(poly_model.score(X_train,y_train))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))


# In[77]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Polynomial Regression Deg 3-' + str(test2) + '%')
plt.show()


# In[78]:


#Polynomial basis 
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
poly_model = make_pipeline(PolynomialFeatures(3),linear_regression)
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test3, random_state=42)
poly_model.fit(X_train,y_train)
y_pred=poly_model.predict(X_test)
print(poly_model.score(X_train,y_train))

print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Polynomial basis Deg 3-' + str(test3) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
model_scores.append(poly_model.score(X_train,y_train))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))


# In[79]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Polynomial Regression Deg 3-' + str(test3) + '%')
plt.show()


# In[80]:


def gaussian_basis_function(x, mu, sigma=0.1):
    return np.exp(-0.5 * (x - mu) ** 2 / sigma ** 2)


# In[81]:


#Gaussian basis
n=np.transpose(X.values)
X_new=[]
for i in range(0,len(n)):
    n[i]=gaussian_basis_function(n[i],0.05*(i+1),0.5*(i+1))
    #print(n)
    X_new.append(n[i])
X_new=np.array(X_new)
X_new=pd.DataFrame(np.transpose(X_new))
X_train, X_test, y_train, y_test = train_test_split(X_new,Y, test_size = test1, random_state=42)
gauss_model=linear_regression.fit(X_train,y_train)
y_pred=gauss_model.predict(X_test)
print(gauss_model.score(X_train,y_train))
print(gauss_model.coef_)
print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Gaussian basis-' + str(test1) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
model_scores.append(gauss_model.score(X_train,y_train))


# In[82]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Gaussian Basis-' + str(test1) + '%')
plt.show()


# In[83]:


#Gaussian basis
n=np.transpose(X.values)
X_new=[]
for i in range(0,len(n)):
    n[i]=gaussian_basis_function(n[i],0.05*(i+1),0.5*(i+1))
    #print(n)
    X_new.append(n[i])
X_new=np.array(X_new)
X_new=pd.DataFrame(np.transpose(X_new))
X_train, X_test, y_train, y_test = train_test_split(X_new,Y, test_size = test2, random_state=42)
gauss_model=linear_regression.fit(X_train,y_train)
y_pred=gauss_model.predict(X_test)
print(gauss_model.score(X_train,y_train))
print(gauss_model.coef_)
print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Gaussian basis-' + str(test2) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
model_scores.append(gauss_model.score(X_train,y_train))


# In[84]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Gaussian Basis-' + str(test2) + '%')
plt.show()


# In[85]:


#Gaussian basis
n=np.transpose(X.values)
X_new=[]
for i in range(0,len(n)):
    n[i]=gaussian_basis_function(n[i],0.05*(i+1),0.5*(i+1))
    #print(n)
    X_new.append(n[i])
X_new=np.array(X_new)
X_new=pd.DataFrame(np.transpose(X_new))
X_train, X_test, y_train, y_test = train_test_split(X_new,Y, test_size = test3, random_state=42)
gauss_model=linear_regression.fit(X_train,y_train)
y_pred=gauss_model.predict(X_test)
print(gauss_model.score(X_train,y_train))
print(gauss_model.coef_)
print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Gaussian basis-' + str(test3) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
model_scores.append(gauss_model.score(X_train,y_train))


# In[86]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Gaussian Basis-' + str(test3) + '%')
plt.show()


# In[87]:


def sigmoid_basis(x,mu, sigma=0.1):
    a=(x-mu)/sigma
    return (1 / (1 + np.exp(-a)))


# In[88]:


n2=np.transpose(X.values)
X1=[]
for i in range(0,len(n2)):
    n2[i]=sigmoid_basis(n2[i],0.05*i,1)
    #print(n)
    X1.append(n2[i])
X1=np.array(X1)
X1=pd.DataFrame(np.transpose(X1))
X_train, X_test, y_train, y_test = train_test_split(X1,Y, test_size = test1, random_state=42)
sigmoid_model=linear_regression.fit(X_train,y_train)
y_pred=sigmoid_model.predict(X_test)
print(sigmoid_model.score(X_train,y_train))
print(sigmoid_model.coef_)
print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Sigmoid basis-' + str(test1) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
model_scores.append((sigmoid_model.score(X_train,y_train)))


# In[89]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Sigmoid Basis-' + str(test1) + '%')
plt.show()


# In[90]:


n2=np.transpose(X.values)
X1=[]
for i in range(0,len(n2)):
    n2[i]=sigmoid_basis(n2[i],0.05*i,1)
    #print(n)
    X1.append(n2[i])
X1=np.array(X1)
X1=pd.DataFrame(np.transpose(X1))
X_train, X_test, y_train, y_test = train_test_split(X1,Y, test_size = test2, random_state=42)
sigmoid_model=linear_regression.fit(X_train,y_train)
y_pred=sigmoid_model.predict(X_test)
print(sigmoid_model.score(X_train,y_train))
print(sigmoid_model.coef_)
print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Sigmoid basis-' + str(test2) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
model_scores.append((sigmoid_model.score(X_train,y_train)))


# In[91]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Sigmoid Basis-' + str(test2) + '%')
plt.show()


# In[92]:


n2=np.transpose(X.values)
X1=[]
for i in range(0,len(n2)):
    n2[i]=sigmoid_basis(n2[i],0.05*i,1)
    #print(n)
    X1.append(n2[i])
X1=np.array(X1)
X1=pd.DataFrame(np.transpose(X1))
X_train, X_test, y_train, y_test = train_test_split(X1,Y, test_size = test3, random_state=42)
sigmoid_model=linear_regression.fit(X_train,y_train)
y_pred=sigmoid_model.predict(X_test)
print(sigmoid_model.score(X_train,y_train))
print(sigmoid_model.coef_)
print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Sigmoid basis-' + str(test3) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
model_scores.append((sigmoid_model.score(X_train,y_train)))


# In[93]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Sigmoid Basis-' + str(test3) + '%')
plt.show()


# In[94]:


#x_ff=fftpack.dct(X.values)
x_ff=np.fft.hfft(X.values)
X_train, X_test, y_train, y_test = train_test_split(x_ff,Y, test_size = test1, random_state=42)
fourier_model=linear_regression.fit(X_train,y_train)
y_pred=fourier_model.predict(X_test)
print(fourier_model.score(X_train,y_train))
print(fourier_model.coef_)
print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Fourier basis-' + str(test1) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
model_scores.append((fourier_model.score(X_train,y_train)))


# In[95]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Fourier Basis-' + str(test1) + '%')
plt.show()


# In[96]:


#x_ff=fftpack.dct(X.values)
x_ff=np.fft.hfft(X.values)
X_train, X_test, y_train, y_test = train_test_split(x_ff,Y, test_size = test2, random_state=42)
fourier_model=linear_regression.fit(X_train,y_train)
y_pred=fourier_model.predict(X_test)
print(fourier_model.score(X_train,y_train))
print(fourier_model.coef_)
print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Fourier basis-' + str(test2) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
model_scores.append((fourier_model.score(X_train,y_train)))


# In[97]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Fourier Basis-' + str(test2) + '%')
plt.show()


# In[98]:


#x_ff=fftpack.dct(X.values)
x_ff=np.fft.hfft(X.values)
X_train, X_test, y_train, y_test = train_test_split(x_ff,Y, test_size = test3, random_state=42)
fourier_model=linear_regression.fit(X_train,y_train)
y_pred=fourier_model.predict(X_test)
print(fourier_model.score(X_train,y_train))
print(fourier_model.coef_)
print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Fourier basis-' + str(test3) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
model_scores.append((fourier_model.score(X_train,y_train)))


# In[99]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Fourier Basis-' + str(test3) + '%')
plt.show()
# print(labels)
print(len(labels))
# print(rmse_values)
print(len(rmse_values))
# print(mae_values)
print(len(mae_values))
# print(model_scores)
print(len(model_scores))


# In[100]:


#Polynomial basis 
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
poly_model = make_pipeline(PolynomialFeatures(2),linear_regression)
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test1, random_state=42)
poly_model.fit(X_train,y_train)
y_pred=poly_model.predict(X_test)
print(poly_model.score(X_train,y_train))

print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Polynomial basis Deg 2-' + str(test1) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
model_scores.append(poly_model.score(X_train,y_train))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))


# In[101]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Polynomial Regression Deg 2-' + str(test1) + '%')
plt.show()


# In[102]:


#Polynomial basis 
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
poly_model = make_pipeline(PolynomialFeatures(2),linear_regression)
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test2, random_state=42)
poly_model.fit(X_train,y_train)
y_pred=poly_model.predict(X_test)
print(poly_model.score(X_train,y_train))

print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Polynomial basis Deg 2-' + str(test2) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
model_scores.append(poly_model.score(X_train,y_train))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))


# In[103]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Polynomial Regression Deg 2-' + str(test2) + '%')
plt.show()


# In[104]:


#Polynomial basis 
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
poly_model = make_pipeline(PolynomialFeatures(2),linear_regression)
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test3, random_state=42)
poly_model.fit(X_train,y_train)
y_pred=poly_model.predict(X_test)
print(poly_model.score(X_train,y_train))

print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))
print(metrics.mean_absolute_error(y_test,y_pred))
labels.append('Polynomial basis Deg 2-' + str(test3) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
model_scores.append(poly_model.score(X_train,y_train))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))


# In[105]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Polynomial Regression Deg 3-' + str(test3) + '%')
plt.show()


# In[106]:
#Bayesian code

# Pandas and numpy for data manipulation
import pandas as pd
import numpy as np
print("Done importing data manipulation dependencies")

# Matplotlib and seaborn for visualization
import matplotlib.pyplot as plt
import seaborn as sns
print("Done importing data visualization dependencies")

# Linear Regression to verify implementation
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
print("Done importing regression dependencies")

# Scipy for statistics
import scipy
from scipy import stats
print("Done importing scipy")

# PyMC3 for Bayesian Inference
import pymc3 as pm
print("Done importing Bayesian Inference dependencies")

# Takes a matrix of features (with intercept as first column) 
# and response vector and calculates linear regression coefficients
# def linear_regression(X, y):
#     # Equation for linear regression coefficients
#     beta = np.matmul(np.matmul(np.linalg.inv(np.matmul(X.T, X)), X.T), y)
#     return beta

fish_toxicity = pd.read_csv('qsar_fish_toxicity_f.csv', sep=';')
# print(fish_toxicity.head())
# df = fish_toxicity[fish_toxicity.isna().any(axis=1)]
# print(df)
# fish_toxicity = fish_toxicity[fish_toxicity.columns].astype(float)
corr = fish_toxicity.corr()['quant_response'].sort_values()

print(corr)
X = fish_toxicity.iloc[:,:]
print(X.head())
Y = fish_toxicity.iloc[:,6:]
print(Y.head())
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = 0.25, random_state=42)
# sns.heatmap(corr)
# sns.PairGrid(fish_toxicity)
# plt.show()

# Calculate correlation coefficient
def corrfunc(x, y, **kws):
    r, _ = stats.pearsonr(x, y)
    ax = plt.gca()
    ax.annotate("r = {:.2f}".format(r),
                xy=(.1, .6), xycoords=ax.transAxes,
               size = 24)
    
cmap = sns.cubehelix_palette(light=1, dark = 0.1,
                             hue = 0.5, as_cmap=True)

sns.set_context(font_scale=2)

# Pair grid set up
g = sns.PairGrid(X_train)

# Scatter plot on the upper triangle
g.map_upper(plt.scatter, s=10, color = 'red')

# Distribution on the diagonal
g.map_diag(sns.distplot, kde=False, color = 'red')

# Density Plot and Correlation coefficients on the lower triangle
g.map_lower(sns.kdeplot, cmap = cmap)
g.map_lower(corrfunc)
# plt.show()


# Calculate mae and rmse
def evaluate_predictions(predictions, true):
    mae = np.mean(abs(predictions - true))
    rmse = np.sqrt(np.mean((predictions - true) ** 2))
    return mae, rmse

# Naive baseline is the median
median_pred = X_train['quant_response'].median()
median_preds = [median_pred for _ in range(len(X_test))]
true = X_test['quant_response']

# Display the naive baseline metrics
mb_mae, mb_rmse = evaluate_predictions(median_preds, true)
print('Median Baseline  MAE: {:.4f}'.format(mb_mae))
print('Median Baseline RMSE: {:.4f}'.format(mb_rmse))


lr = LinearRegression()
lr.fit(X_train.drop(columns='quant_response'), y_train)
print(X_train.head())
print(X_train.shape)
ols_formula = 'quant_response = %0.2f +' % lr.intercept_
for i, col in enumerate(X_train.columns[:-1]):
    print("i={}, col={}".format(i,col))
    print("lr.coef_[i] = {}".format(lr.coef_))
    ols_formula += ' %0.2f * %s +' %(lr.coef_[0][i], col)
    
tmp = ' '.join(ols_formula.split(' ')[:-1])
print(tmp)

# Formula for Bayesian Linear Regression (follows R formula syntax
formula = 'quant_response ~ ' + ' + '.join(['%s' % variable for variable in X_train.columns[:-1]])
print(formula)

# Context for the model
with pm.Model() as normal_model:
    
#     # The prior for the model parameters will be a normal distribution
    family = pm.glm.families.Normal()
    
#     # Creating the model requires a formula and data (and optionally a family)
    pm.GLM.from_formula(formula, data = X_train, family = family)
    
#     # Perform Markov Chain Monte Carlo sampling
    normal_trace = pm.sample(draws=2000, chains = 2, tune = 500)
    

    
df1 =pd.DataFrame(pm.summary(normal_trace))
print(df1)


# In[107]:


df1=pd.DataFrame(df1, index = ['CIC0','SM1_Dz','GATS1i','NdsCH','NdssC','MLOGP'])
df1['Label']=['CIC0','SM1_Dz','GATS1i','NdsCH','NdssC','MLOGP']
print(df1)


# In[108]:


from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
# Import pandas library 
import pandas as pd 

# initialize list of lists 
# #data = [['CIC0', 0.469606],['SM1_Dz', 1.313303],['GATS1i', -0.736089],['NdsCH', 0.360664],
#         ['NdssC', 0.027475],['MLOGP', 0.362830]]
# val = 1.957809
# # Create the pandas DataFrame 
# df = pd.DataFrame(data, columns = ['Label','Mean']) 
  
# # print dataframe. 
# df 

X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = 0.15, random_state=42)
y_actual = pd.DataFrame(y_test)
print(y_actual.shape)
y_actual.head()
# iterate through each row and select  
# 'Name' and 'Stream' column respectively.
y_pred = []
val = 1.957809
tmp_outer = 0
for ind in X_test.index:
    tmp_outer = 0
    for ind_inner in df1.index:
        tmp = X_test[df1['Label'][ind_inner]][ind] * df1['mean'][ind_inner]
        tmp_outer += tmp
    tmp_outer += val
    y_pred.append(tmp_outer)
# print(y_pred)
y_pred = pd.DataFrame(y_pred)
print(y_pred.shape)
y_pred.head()

labels.append('Bayesian-'+str(0.15)+'%')
mae_values.append(metrics.mean_absolute_error(y_actual,y_pred))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_actual,y_pred)))
# To be changed
model_scores.append(0.00)

# print(labels)
print(len(labels))
# print(rmse_values)
print(len(rmse_values))
# print(mae_values)
print(len(mae_values))
# print(model_scores)
print(len(model_scores))

# print(np.sqrt(metrics.mean_squared_error(y_actual,y_pred)))


# In[109]:


from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
# Import pandas library 
import pandas as pd 

# initialize list of lists 
data = [['CIC0', 0.469606],['SM1_Dz', 1.313303],['GATS1i', -0.736089],['NdsCH', 0.360664],
        ['NdssC', 0.027475],['MLOGP', 0.362830]]
val = 1.957809
# Create the pandas DataFrame 
df = pd.DataFrame(data, columns = ['Label','Mean']) 
  
# print dataframe. 
df 

X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test1, random_state=42)
y_actual = pd.DataFrame(y_test)
print(y_actual.shape)
y_actual.head()
# iterate through each row and select  
# 'Name' and 'Stream' column respectively.
y_pred = []
tmp_outer = 0
for ind in X_test.index:
    tmp_outer = 0
    for ind_inner in df.index:
        tmp = X_test[df['Label'][ind_inner]][ind] * df['Mean'][ind_inner]
        tmp_outer += tmp
    tmp_outer += val
    y_pred.append(tmp_outer)
# print(y_pred)
y_pred = pd.DataFrame(y_pred)
print(y_pred.shape)
y_pred.head()

labels.append('Bayesian-'+str(test1)+'%')
mae_values.append(metrics.mean_absolute_error(y_actual,y_pred))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_actual,y_pred)))
# To be changed
model_scores.append(0.00)

# print(labels)
print(len(labels))
# print(rmse_values)
print(len(rmse_values))
# print(mae_values)
print(len(mae_values))
# print(model_scores)
print(len(model_scores))

# print(np.sqrt(metrics.mean_squared_error(y_actual,y_pred)))


# In[110]:


plotter("Bayesian Regression", y_actual, y_pred, test1)


# In[111]:


from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
# Import pandas library 
import pandas as pd 

# initialize list of lists 
data = [['CIC0', 0.469606],['SM1_Dz', 1.313303],['GATS1i', -0.736089],['NdsCH', 0.360664],
        ['NdssC', 0.027475],['MLOGP', 0.362830]]
val = 1.957809
# Create the pandas DataFrame 
df = pd.DataFrame(data, columns = ['Label','Mean']) 
  
# print dataframe. 
df 

X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test2, random_state=42)
y_actual = pd.DataFrame(y_test)
print(y_actual.shape)
y_actual.head()

y_pred = []
tmp_outer = 0
for ind in X_test.index:
    tmp_outer = 0
    for ind_inner in df.index:
        tmp = X_test[df['Label'][ind_inner]][ind] * df['Mean'][ind_inner]
        tmp_outer += tmp
    tmp_outer += val
    y_pred.append(tmp_outer)
y_pred = pd.DataFrame(y_pred)
y_pred.head()

labels.append('Bayesian-'+str(test2)+'%')
mae_values.append(metrics.mean_absolute_error(y_actual,y_pred))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_actual,y_pred)))
# To be changed
model_scores.append(0.00)


# In[112]:


plotter("Bayesian Regression", y_actual, y_pred, test2)


# In[113]:


from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
# Import pandas library 
import pandas as pd 

# initialize list of lists 
data = [['CIC0', 0.469606],['SM1_Dz', 1.313303],['GATS1i', -0.736089],['NdsCH', 0.360664],
        ['NdssC', 0.027475],['MLOGP', 0.362830]]
val = 1.957809
# Create the pandas DataFrame 
df = pd.DataFrame(data, columns = ['Label','Mean']) 
  
# print dataframe. 
df 

X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test3, random_state=42)
y_actual = pd.DataFrame(y_test)
print(y_actual.shape)
y_actual.head()
# iterate through each row and select  
# 'Name' and 'Stream' column respectively.
y_pred = []
tmp_outer = 0
for ind in X_test.index:
    tmp_outer = 0
    for ind_inner in df.index:
        tmp = X_test[df['Label'][ind_inner]][ind] * df['Mean'][ind_inner]
        tmp_outer += tmp
    tmp_outer += val
    y_pred.append(tmp_outer)
# print(y_pred)
y_pred = pd.DataFrame(y_pred)
print(y_pred.shape)
y_pred.head()

labels.append('Bayesian-'+str(test3)+'%')
mae_values.append(metrics.mean_absolute_error(y_actual,y_pred))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_actual,y_pred)))
# To be changed
model_scores.append(0.00)

# print(labels)
print(len(labels))
# print(rmse_values)
print(len(rmse_values))
# print(mae_values)
print(len(mae_values))
# print(model_scores)
print(len(model_scores))

# print(np.sqrt(metrics.mean_squared_error(y_actual,y_pred)))


# In[114]:


plotter("Bayesian Regression", y_actual, y_pred, test3)


# In[115]:


#Polynomial basis 
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
poly_model = make_pipeline(PolynomialFeatures(4),linear_regression)
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test1, random_state=42)
poly_model.fit(X_train,y_train)
y_pred=poly_model.predict(X_test)

print("Mean absolute error : {}".format(metrics.mean_absolute_error(y_test,y_pred)))
print("Model Score : {}".format(poly_model.score(X_train,y_train)))
print("Root mean square error : {}".format(np.sqrt(metrics.mean_squared_error(y_test,y_pred))))
labels.append('Polynomial basis Deg 4-' + str(test1) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
model_scores.append(poly_model.score(X_train,y_train))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))


# In[116]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Polynomial Regression Deg 4-' + str(test1) + '%')
plt.show()


# In[117]:


#Polynomial basis 
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
poly_model = make_pipeline(PolynomialFeatures(4),linear_regression)
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test2, random_state=42)
poly_model.fit(X_train,y_train)
y_pred=poly_model.predict(X_test)

print("Mean absolute error : {}".format(metrics.mean_absolute_error(y_test,y_pred)))
print("Model Score : {}".format(poly_model.score(X_train,y_train)))
print("Root mean square error : {}".format(np.sqrt(metrics.mean_squared_error(y_test,y_pred))))
labels.append('Polynomial basis Deg 4-' + str(test2) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
model_scores.append(poly_model.score(X_train,y_train))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))


# In[118]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Polynomial Regression Deg 4-' + str(test2) + '%')
plt.show()


# In[119]:


#Polynomial basis 
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
poly_model = make_pipeline(PolynomialFeatures(4),linear_regression)
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = test3, random_state=42)
poly_model.fit(X_train,y_train)
y_pred=poly_model.predict(X_test)

print("Mean absolute error : {}".format(metrics.mean_absolute_error(y_test,y_pred)))
print("Model Score : {}".format(poly_model.score(X_train,y_train)))
print("Root mean square error : {}".format(np.sqrt(metrics.mean_squared_error(y_test,y_pred))))
labels.append('Polynomial basis Deg 4-' + str(test3) + '%')
mae_values.append(metrics.mean_absolute_error(y_test,y_pred))
model_scores.append(poly_model.score(X_train,y_train))
rmse_values.append(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))


# In[120]:


fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
ax.title.set_text('Polynomial Regression Deg 4-' + str(test3) + '%')
plt.show()


# In[ ]:





# In[121]:


# print(labels)
print(len(labels))
# print(rmse_values)
print(len(rmse_values))
# print(mae_values)
print(len(mae_values))
# print(model_scores)
print(len(model_scores))


# In[122]:


import copy
data = []
for i in range(len(labels)):
    tmp = []
    tmp.append(labels[i])
    tmp.append(rmse_values[i])
    tmp.append(mae_values[i])
    tmp.append(model_scores[i])
    data.append(copy.copy(tmp))
    
# print(data)
# Create the pandas DataFrame 
df = pd.DataFrame(data, columns = ['Basis function', 'RMSE', 'MAE', 'Model Score']) 
  
# print dataframe. 
df 

# Degree 4 leads to overfitting and high error (Can be added)


# In[ ]:





# In[123]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six

def render_mpl_table(data, col_width=5.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax

render_mpl_table(df, header_columns=0)


# In[124]:


labels = labels[:-3]
rmse_values = rmse_values[:-3]
mae_values = mae_values[:-3]
model_scores = model_scores[:-3]


# In[125]:


import copy
data = []
for i in range(len(labels)):
    tmp = []
    tmp.append(labels[i])
    tmp.append(rmse_values[i])
    tmp.append(mae_values[i])
    tmp.append(model_scores[i])
    data.append(copy.copy(tmp))
    
# print(data)
# Create the pandas DataFrame 
df = pd.DataFrame(data, columns = ['Basis function', 'RMSE', 'MAE', 'Model Score']) 
  
# print dataframe. 
df 

# Degree 4 leads to overfitting and high error (Can be added)


# In[127]:


fig = plt.figure()
ax1 = df.plot(kind='barh',x='Basis function',y='RMSE',color='#F43838', title='RMSE Comparison')
ax2 = df.plot(kind='barh',x='Basis function',y='MAE',color='#2FE9E9', title='MAE Comparison')
ax3 = df.plot(kind='barh',x='Basis function',y='Model Score',color='#110CA1', title='Model Score Comparison')
plt.show()


