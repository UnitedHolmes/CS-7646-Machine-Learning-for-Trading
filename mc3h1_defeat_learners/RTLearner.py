"""
Random Tree Learner.  (c) 2017 Yuanda Zhu
"""

import numpy as np

class RTLearner(object):

    def __init__(self, leaf_size = 1, verbose = False):
        self.my_leaf_size = leaf_size
        self.tree = []
        pass # move along, these aren't the drones you're looking for

    def author(self):
        return 'yzhu94' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """        
        
        # To detetermine if all values in Y are the same
        all_same = True
        for yy in dataY:
            if yy != dataY[0]:
                all_same = False
                break
        
        # If only one sample in this branch or Y values are the same
        if (dataX.shape[0] <= self.my_leaf_size) or all_same :          
            
            new_leaf = np.array([-1, np.mean(dataY), np.nan, np.nan])
#            print new_leaf
            return new_leaf
        
        # Else, it's necessary to make new sub-branches
        else:
            # Determine random feature i to split
            i = np.random.random_integers(0,dataX.shape[1]-1)
            
#            self.factor[ind] = i
            # Determine random samples to deal with
            row_1 = np.random.random_integers(0,dataX.shape[0]-1)
            row_2 = np.random.random_integers(0,dataX.shape[0]-1)
            
            # Repick if the same row is selected, or same Y value is selected
            while (row_1 == row_2) or (dataY[row_1] == dataY[row_2]):
                row_2 = np.random.random_integers(0,dataX.shape[0]-1)
            
            # Corner condition
            trials_row2 = 0
            while (dataX[row_1,i] == dataX[row_2,i]):
                row_2 = np.random.random_integers(0,dataX.shape[0]-1)
                while (row_1 == row_2):
                    row_2 = np.random.random_integers(0,dataX.shape[0]-1)
                
                trials_row2 = trials_row2 + 1
                # Too many trails for repicking row 2, then repick i
                if trials_row2 >= 10:
                    new_leaf = np.array([-1, np.mean(dataY), np.nan, np.nan])
                    return new_leaf
                    
            splitVal = (dataX[row_1,i] + dataX[row_2,i])/2
            
            # Build left and right tree
#            print 'left'
            left_tree = self.addEvidence(dataX[dataX[:,i]<=splitVal], dataY[dataX[:,i]<=splitVal])
#            print 'right'
            right_tree = self.addEvidence(dataX[dataX[:,i]>splitVal], dataY[dataX[:,i]>splitVal])
            
            if left_tree.shape[0] == left_tree.size:
                root = np.array([i, splitVal, 1, 1+1])
            else:
                root = np.array([i, splitVal, 1, left_tree.shape[0]+1])
#            print root
            
            self.tree = np.vstack((root, left_tree, right_tree))
#            print self.tree
            
            return self.tree

#        # slap on 1s column so linear regression finds a constant term
#        newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1])
#        newdataX[:,0:dataX.shape[1]]=dataX
#
#        # build and save the model
#        self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY)
        
    def query(self,Xtest):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        if Xtest.shape[0] == Xtest.size:
            Y_pred = np.zeros(1)
        else:
            Y_pred = np.zeros(Xtest.shape[0])
        for row_X in range(0,Xtest.shape[0]):
            
            row_ind = 0
            
            while self.tree[row_ind,0] != -1:
                Xtest_col = int(self.tree[row_ind,0])
                if (Xtest[row_X,Xtest_col] <= self.tree[row_ind, 1]):
                    row_ind = row_ind + int(self.tree[row_ind,2])
                else:
                    row_ind = row_ind + int(self.tree[row_ind,3])
                if row_ind >= self.tree.shape[0]:
                    print 'error!'
            
            Y_pred[row_X] = self.tree[row_ind,1]
        
        return Y_pred

if __name__=="__main__":
    print "Glory Glory Man United!"
