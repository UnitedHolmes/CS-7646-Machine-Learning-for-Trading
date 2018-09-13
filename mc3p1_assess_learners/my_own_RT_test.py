# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 00:02:24 2017

@author: NFLS_UnitedHolmes
My own test on RTLeaner
"""

import numpy as np
import RTLearner as rt

my_data = []
my_data = np.array([[0.885,0.330,9.100,4.000], [0.725,0.390,10.900,5.000], [0.560,0.500,9.400,6.000]])
my_data = np.append(my_data, [[0.735,0.570,9.800,5.000], [0.610,0.630,8.400,3.000]], axis=0)

my_data = np.append(my_data, [[0.260,0.630,11.800,8.000], [0.500,0.680,10.500,7.000], [0.320,0.780,10.000,6.000]],axis=0)

Xtrain = my_data[:,:-1]
Ytrain = my_data[:,-1]

Xtest = my_data[:,:-1]

#print Xtrain

learner = rt.RTLearner(leaf_size = 1, verbose = False) # constructor
my_matrix = learner.addEvidence(Xtrain, Ytrain) # training step
Y = learner.query(Xtest) # query