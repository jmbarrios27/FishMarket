# -*- coding: utf-8 -*-
"""Fish-Market.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1phdFxySpQ_mkbPBrp-M8EEI27dYiKiDE
"""

#importing libraries
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import io

#importing dataset
from google.colab import files
uploaded = files.upload()

#transforming it into panda´s dataframe
df = pd.read_csv(io.BytesIO(uploaded['Fish.csv']))
df.head()

#Observing data
df.describe()

"""Meanings of the Columns:

Species: Species name of fish

Weight: Weight of fish in gram

Length1: Vertical length in cm

Length2: Diagonal length in cm

Length3: Cross length in cm

Height: Height in cm

Width: Diagonal width in cm
"""

#counting fish species
plt.title('Fish Species Count')
sns.countplot(data=df,x='Species')

sns.heatmap(df.corr(),annot=True)

sns.pairplot(df, kind='scatter', hue='Species');

"""## **MACHINE LEARNNG MODEL**"""

# Dependant (Target) Variable:
y = df['Weight']
# Independant Variables:
X = df.iloc[:,2:7]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

print('Checking the Data Partition for train and test set')
print('X_train: ', np.shape(X_train))
print('y_train: ', np.shape(y_train))
print('X_test: ', np.shape(X_test))
print('y_test: ', np.shape(y_test))

from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg.fit(X_train,y_train)

# My model's parameters:
print('Model intercept: ', reg.intercept_)
print('Model coefficients: ', reg.coef_)

#Predictions from the Train dataset
y_head = reg.predict(X_train)
y_head

#checking the accuracy of the model
from sklearn.metrics import r2_score
r2_score(y_train,y_head)

from sklearn.model_selection import cross_val_score
cross_val_score_train = cross_val_score(reg, X_train, y_train, cv=10, scoring='r2')
print(cross_val_score_train)

y_pred = reg.predict(X_test)
y_pred

plt.scatter(X_test['Length3'], y_test, color='black', alpha=0.4)
plt.scatter(X_test['Length3'], y_pred, color='green', alpha=0.4)
plt.xlabel('Cross Length in cm')
plt.ylabel('Weight of the fish')
plt.title('Linear Regression Model for Weight Estimation');

y_pred1 = pd.DataFrame(y_pred, columns=['Estimated Weight'])
y_pred1.head()

y_test1 = pd.DataFrame(y_test)
y_test1 = y_test1.reset_index(drop=True)
y_test1.head()

ynew = pd.concat([y_test1, y_pred1], axis=1)
ynew

df.columns

import statsmodels.formula.api as sm
model = sm.ols(formula='Weight~Length1+Length2+Length3+Height+Width',data=df)
fitted = model.fit()
fitted.summary()

sns.residplot(y_test, y_pred)

#residuas
res = fitted.resid
#Normality of residuals
res.hist()
plt.title('Normalidad de Los Residuos')