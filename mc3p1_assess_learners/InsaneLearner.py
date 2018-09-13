# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 15:24:19 2017

@author: NFLS_UnitedHolmes
"""

#import numpy as np
import LinRegLearner as lr
import BagLearner as bl

class InsaneLearner(object):

    def __init__(self, verbose):       
        self.my_learner = bl.BagLearner(learner = bl.BagLearner, kwargs = {'learner': bl.BagLearner, 'kwargs':{}, 'bags': 20, 'boost': False, 'verbose': False}, bags = 20, boost = False, verbose = False)
        pass # move along, these aren't the drones you're looking for

    def author(self):
        return 'yzhu94' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """               
        
#        for k in range(0, 20):
#            orders = np.random.randint(dataX.shape[0], size=dataX.shape[0])
#            trainX = dataX[orders]
#            trainY = dataY[orders]
        self.my_learner.addEvidence(dataX, dataY)               
               
    def query(self,Xtest):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """       
        
        self.my_learner.query(Xtest)

if __name__=="__main__":
    print "Glory Glory Man United!"
