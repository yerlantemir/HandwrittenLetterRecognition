#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 20:55:33 2019

@author: yerlan
"""

from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg



import pandas as pd
import numpy as np
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report




train_path = r'./train_set/'
test_path = r'./test_set/'


train_batches = ImageDataGenerator(rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True).flow_from_directory(train_path,target_size=(28,28),
                                   classes='ә,і,ң,ғ,ү,ұ,қ,ө,һ'.split(','))

test_batches = ImageDataGenerator(rescale=1./255).flow_from_directory(test_path,target_size=(28,28),
                                   classes='ә,і,ң,ғ,ү,ұ,қ,ө,һ'.split(','))

def rgb2gray(rgb):
    return np.dot(rgb[...,:], [0.2989, 0.5870, 0.1140])

data_list_x = []
data_list_y = []
batch_index = 0

while batch_index <= train_batches.batch_index:
    x,y = train_batches.next()
    
    for i in range(len(x)):
        img_data = rgb2gray(x[i])
        data_list_x.append(img_data)
        for k in range(y.shape[1]):
            if y[i][k] == 1:
                data_list_y.append(k)
    batch_index = batch_index + 1
    
data_list_x_1 = []
data_list_y_1 = []
batch_index = 0

while batch_index <= test_batches.batch_index:
    x,y = test_batches.next()
    
    for i in range(len(x)):
        img_data = rgb2gray(x[i])
        data_list_x_1.append(img_data)
        for k in range(y.shape[1]):
            if y[i][k] == 1:
                data_list_y_1.append(k)
    batch_index = batch_index + 1


    
train_x = np.array(data_list_x).reshape(len(data_list_x),784).astype('float32')
train_y = np.array(data_list_y).astype('int64')
test_x = np.array(data_list_x_1).reshape(len(data_list_x_1),784).astype('float32')
test_y = np.array(data_list_y_1).astype('int64')




#clf_svm = LinearSVC()
#clf_svm.fit(train_x, train_y)
#y_pred_svm = clf_svm.predict(test_x)
#acc_svm = accuracy_score(test_y, y_pred_svm)
#print ("Linear SVM accuracy: ",acc_svm)





clf_knn = KNeighborsClassifier()
clf_knn.fit(train_x, train_y)
y_pred_knn = clf_knn.predict(test_x)
acc_knn = accuracy_score(test_y, y_pred_knn)
print ("nearest neighbors accuracy: ",acc_knn)
print(classification_report(test_y,y_pred_knn))
















