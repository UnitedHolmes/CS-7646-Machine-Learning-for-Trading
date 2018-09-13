# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 23:53:58 2017

@author: NFLS_UnitedHolmes
test to make report, part 2
"""

import util
import numpy as np
import math
import RTLearner as rt
import BagLearner as bl
import sys
import matplotlib.pyplot as plt

datafile = 'Istanbul.csv'

with util.get_learner_data_file(datafile) as f:
    alldata = np.genfromtxt(f,delimiter=',')
    # Skip the date column and header row if we're working on Istanbul data

    if datafile == 'Istanbul.csv':
        alldata = alldata[1:,1:]
    datasize = alldata.shape[0]
    cutoff = int(datasize*0.6)
    
    my_list = range(0, 51, 1)
    
    rmse_in_sample = np.zeros((len(my_list),5))
    rmse_out_sample = np.zeros((len(my_list),5))
    ind = -1
    
    for my_leaf in my_list:
        ind += 1
        for trials in range(0,5):          
    
            permutation = np.random.permutation(alldata.shape[0])
            col_permutation = np.random.permutation(alldata.shape[1]-1)
            train_data = alldata[permutation[:cutoff],:]
            # trainX = train_data[:,:-1]
            trainX = train_data[:,col_permutation]
            trainY = train_data[:,-1]
            test_data = alldata[permutation[cutoff:],:]
            # testX = test_data[:,:-1]
            testX = test_data[:,col_permutation]
            testY = test_data[:,-1]
    
#            learner = rt.RTLearner(leaf_size = my_leaf, verbose = False) # constructor
            learner = bl.BagLearner(learner = rt.RTLearner, kwargs = {"leaf_size":my_leaf}, bags = 20, boost = False, verbose = False)
            learner.addEvidence(trainX, trainY) # training step
        
            predY = learner.query(trainX) # get the predictions
            rmse_in_sample[ind, trials] = np.sqrt(((trainY - predY)**2).mean())             
#            rmse_in_sample(trials, ind) = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
            
            predY = learner.query(testX) # get the predictions
            rmse_out_sample[ind, trials] = np.sqrt(((testY - predY)**2).mean())
#            rmse_out_sample(trials, ind) = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
           

    plt.figure(0)
    plt.plot(my_list,np.mean(rmse_in_sample, axis = 1), '--', label = 'In Sample RMSE')
    plt.plot(my_list,np.mean(rmse_out_sample, axis = 1), label = 'Out of Sample RMSE')
    plt.legend(loc='lower right')
    plt.title('Leaf size vs RMSE')
    plt.show()
    
    
#    plt.figure(0)
#    plt.plot(range(0,10),rmse_in_sample[0,:], '--', label = 'In Sample RMSE')
#    plt.plot(range(0,10),rmse_out_sample[0,:], label = 'Out of Sample RMSE')
#    plt.legend(loc='center right')
#    plt.title('Leaf size = 1')
#    plt.show()
#    
#    plt.figure(1)
#    plt.plot(range(0,10),rmse_in_sample[1,:], '--', label = 'In Sample RMSE')
#    plt.plot(range(0,10),rmse_out_sample[1,:], label = 'Out of Sample RMSE')
#    plt.legend(loc='center right')
#    plt.title('Leaf size = 5')
#    plt.show()
#    
#    plt.figure(2)
#    plt.plot(range(0,10),rmse_in_sample[2,:], '--', label = 'In Sample RMSE')
#    plt.plot(range(0,10),rmse_out_sample[2,:], label = 'Out of Sample RMSE')
#    plt.legend(loc='center right')
#    plt.title('Leaf size = 10')
#    plt.show()

    rmse_in_mean = np.mean(rmse_in_sample, axis = 1)
    rmse_out_mean = np.mean(rmse_out_sample, axis = 1)
    rmse_sum_mean = np.mean(rmse_in_sample, axis = 1) + np.mean(rmse_out_sample, axis = 1)
    
    print np.mean(rmse_in_sample, axis = 1)
    print np.mean(rmse_out_sample, axis = 1)
    print np.mean(rmse_in_sample, axis = 1) + np.mean(rmse_out_sample, axis = 1)