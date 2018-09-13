"""
template for generating data to fool learners (c) 2016 Tucker Balch
(c) 2017 Yuanda Zhu
"""

import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regresstion than random trees
def best4LinReg(seed=19):
    np.random.seed(seed)
    no_rows = np.random.randint(10, high=1000)
    no_cols = np.random.randint(2, high=1000)
    
    X = np.zeros((no_rows,no_cols))
    YY = np.zeros((no_rows, 5))
    Y = YY[:,0] + 1    
       
    X = np.random.randint(0, high=no_rows, size=no_rows*no_cols)
    X = np.reshape(X,(no_rows,no_cols))
        
    Y = 19*X[:,0]

    return X, Y

def best4RT(seed=19):
    np.random.seed(seed)
    no_rows = np.random.randint(10, high=1000)
    no_cols = np.random.randint(2, high=1000)
    
    X = np.zeros((no_rows,no_cols))       
    YY = np.zeros((no_rows, 5))
    Y = YY[:,0]
    
    X[:,0] = np.random.randint(1, high=no_rows,size=no_rows)
    X[:,-1] = np.random.randint(1, high=no_rows,size=no_rows)    
           
    half_col = np.round(no_cols/2)
    
#    X[:,1:half_col] =  X[:,1:half_col] + X[:,0].reshape((no_rows,1))
#    X[:,half_col+1:-2] =  X[:,half_col+1:-2] + X[:,-1].reshape((no_rows,1))
    
    for current_col in range(0,half_col):        
        X[:,current_col+1] = X[:,0]
        if current_col+half_col-1 < no_cols - 1:
            X[:,current_col+half_col-1] = X[:,-1]
        
    
    Y[X[:,0]<=no_rows/2] = Y[X[:,0]<=no_rows/2] + 20060128
    Y[X[:,-1]<=no_rows/2] = Y[X[:,-1]<=no_rows/2] + 902905597
    

    return X, Y

if __name__=="__main__":
    print "Fight, win, drink, get naked!"
