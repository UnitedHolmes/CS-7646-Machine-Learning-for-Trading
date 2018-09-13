# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 14:16:37 2017

@author: NFLS_UnitedHolmes
"""

import numpy as np
import BagLearner as bl
import InsaneLearner as it
import RTLearner as rt
import LinRegLearner as lr

class BagLearner(object):

    def __init__(self, learner, kwargs, bags, boost, verbose):        
        self.my_learner = learner
        self.my_kwargs = kwargs
        self.my_bags = bags
        self.my_boost = boost
        self.my_verbose = verbose
        pass # move along, these aren't the drones you're looking for

    def author(self):
        return 'yzhu94' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """        
        self.learners = []
        
#        if self.my_kwargs['BagLearners'] > 0:
#            self.my_kwargs['BagLearners'] -= 1            
        
        for k in range(0, self.my_bags):  
            self.learners.append(self.my_learner(**self.my_kwargs))
            
        if self.my_learner == rt.RTLearner:
            for current_learner in self.learners:                
                orders = np.random.randint(dataX.shape[0], size=dataX.shape[0])
                trainX = dataX[orders]
                trainY = dataY[orders]            
                current_learner.addEvidence(trainX, trainY)
        
        if self.my_learner == lr.LinRegLearner:
            for current_learner in self.learners:                
                orders = np.random.randint(dataX.shape[0], size=dataX.shape[0])
                trainX = dataX[orders]
                trainY = dataY[orders]            
                current_learner.addEvidence(trainX, trainY)

        return self.learners
        
        
        
    def query(self,Xtest):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """     
                     
        if self.my_learner == rt.RTLearner:
            Y_pred = []      
            for current_learner in self.learners:
                Y_pred.append(current_learner.query(Xtest))
                
            mean_Y_pred = np.mean(Y_pred, axis=0)

        if self.my_learner == lr.LinRegLearner:
            Y_pred = []      
            for current_learner in self.learners:
                Y_pred.append(current_learner.query(Xtest))
                
            mean_Y_pred = np.mean(Y_pred, axis=0)
            
        # else:
        #     while self.my_learner == bl.BagLearner:
        #         self.my_learner = bl.BagLearner(learner = self.my_learner, kwargs = self.my_kwargs, bags = self.my_bags, boost = False, verbose = False)
               
        return mean_Y_pred

if __name__=="__main__":
    print "Glory Glory Man United!"
