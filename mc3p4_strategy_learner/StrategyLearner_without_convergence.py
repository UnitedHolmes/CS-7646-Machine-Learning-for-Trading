"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
"""

import numpy as np
import datetime as dt
import pandas as pd
import util as ut
import random
import QLearner as ql

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False):
        self.verbose = verbose
        self.states_N = 10
        self.N = 10
        
    def discretize(self, indicator_index, indicator_value):
        if indicator_index == 1:
            dis_max = self.X1_max
            dis_min = self.X1_min
        elif indicator_index == 2:
            dis_max = self.X2_max
            dis_min = self.X2_min
        elif indicator_index == 3:
            dis_max = self.X3_max
            dis_min = self.X3_min
        
        state_index = 0
        increment = (dis_max - dis_min) / self.states_N
        
        # ( indicator_value ]
        while indicator_value > dis_min + state_index * increment:
            state_index = state_index + 1
        
        if state_index == 0:
            state_index = 1
            
        return state_index - 1
            
    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000): 

        # add your code to do learning here
        position = 0 # number of share you hold
        
        # X1: Momentum, 10 days delay, M = close(i)/close(i-10)*100
        # X2: Moving average, avg(i) = mean(close(i-10+1):close(i))
        # X3: Bollinger Bands, 10 days mean & 2*std      
               
        # Create three learners, each for one position
        self.learner0 = ql.QLearner(num_states=self.states_N**3,\
            num_actions = 3, \
            alpha = 0.2, \
            gamma = 0.9, \
#            rar = 0.0, \                                        
            radr = 0, \
            dyna = 0, \
            verbose=False) #position -200
                             
        self.learner1 = ql.QLearner(num_states=self.states_N**3,\
            num_actions = 3, \
            alpha = 0.2, \
            gamma = 0.9, \
#            rar = 0, \                                        
            radr = 0, \
            dyna = 0, \
            verbose=False) #position 0
        
        self.learner2 = ql.QLearner(num_states=self.states_N**3,\
            num_actions = 3, \
            alpha = 0.2, \
            gamma = 0.9, \
#            rar = 0, \                                        
            radr = 0, \
            dyna = 0, \
            verbose=False) #position 200
        
        flag_0 = True #haven't been initiazlied yet
        flag_1 = True
        flag_2 = True
        
        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices = prices.fillna(method='ffill').fillna(method='bfill')
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        if self.verbose: print prices
        
        # start calculating three indicators
        X1_Momentum = prices.values[self.N-1:,:]/prices.values[0:-self.N+1,:] *100
#        X1_Momentum = prices.iloc[N:-1].divide(prices.iloc[0:-N-1])*100

        X2_SMA = pd.rolling_mean(prices,window=self.N)        
        X3_middle = pd.rolling_mean(prices,window=self.N)
        X3_std = pd.rolling_std(prices,window=self.N)
        X3_upper = X3_middle.add(2*X3_std)
        X3_lower = X3_middle.subtract(2*X3_std)
        
        self.X1_max = max(X1_Momentum)
        self.X1_min = min(X1_Momentum)
        self.X2_max = X2_SMA.max(axis=0).values
        self.X2_min = X2_SMA.min(axis=0).values
        self.X3_max = X3_upper.max(axis=0).values
        self.X3_min = X3_upper.min(axis=0).values
        
        training_day = 0
        while training_day < X3_upper.shape[0]:            
            
            if not np.isnan(X3_upper.iloc[training_day].values):
                
#                print X3_upper.index[training_day]
#                print X1_Momentum[training_day-N+1]
#                print X2_SMA.index[training_day]
                
                state_1 = self.discretize(1, X1_Momentum[training_day-self.N+1])
                state_2 = self.discretize(2, X2_SMA.iloc[training_day].values)
                state_3 = self.discretize(3, X3_upper.iloc[training_day].values)
#                print training_day
#                print state_1, state_2, state_3
                
                state = state_1*self.states_N**2 + state_2*self.states_N + state_3
                if position == -200:
                    if flag_0 == True:
                        flag_0 = False
                        action = self.learner0.querysetstate(state)
                        
                    r = prices.iloc[training_day].values - prices.iloc[training_day-1].values
                    r = r*position
                    action = self.learner0.query(state,r)
                    new_position = position + action*200                    
                    
                if position == 0:
                    if flag_1 == True:
                        flag_1 = False
                        action = self.learner1.querysetstate(state)
                        
                    r = prices.iloc[training_day].values - prices.iloc[training_day-1].values
                    r = r*position
                    action = self.learner1.query(state,r)
                    new_position = position + (action-1)*200
                    
                if position == 200:
                    if flag_2 == True:
                        flag_2 = False
                        action = self.learner2.querysetstate(state)
                        
                    r = prices.iloc[training_day].values - prices.iloc[training_day-1].values
                    r = r*position
                    action = self.learner2.query(state,r)
                    new_position = position + (action-2)*200
                    
                position = new_position
                
#                if training_day > 20:
#                    break
                
            if self.verbose:
                print training_day, position
            training_day = training_day + 1
  
        # example use with new colname 
#        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
#        volume = volume_all[syms]  # only portfolio symbols
#        volume_SPY = volume_all['SPY']  # only SPY, for comparison later
#        if self.verbose: print volume
#        return X3_BB_middle, X3_BB_std

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        # here we build a fake set of trades
        # your code should return the same sort of data
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        prices = prices_all[[symbol]]
        prices = prices.fillna(method='ffill').fillna(method='bfill')
        trades = prices_all[[symbol,]]  # only portfolio symbols
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later
        trades.values[:,:] = 0 # set them all to nothing
#        trades.values[3,:] = 200 # add a BUY at the 4th date
#        trades.values[5,:] = -200 # add a SELL at the 6th date 
#        trades.values[6,:] = 200 # add a SELL at the 7th date 
#        trades.values[8,:] = -400 # add a BUY at the 9th date
#        if self.verbose: print type(trades) # it better be a DataFrame!
#        if self.verbose: print trades
#        if self.verbose: print prices_all
        
        # start calculating three indicators
        X1_Momentum = prices.values[self.N-1:,:]/prices.values[0:-self.N+1,:] *100
#        X1_Momentum = prices.iloc[N:-1].divide(prices.iloc[0:-N-1])*100

        X2_SMA = pd.rolling_mean(prices,window=self.N)        
        X3_middle = pd.rolling_mean(prices,window=self.N)
        X3_std = pd.rolling_std(prices,window=self.N)
        X3_upper = X3_middle.add(2*X3_std)
        X3_lower = X3_middle.subtract(2*X3_std)
        
        self.X1_max = max(X1_Momentum)
        self.X1_min = min(X1_Momentum)
        self.X2_max = X2_SMA.max(axis=0).values
        self.X2_min = X2_SMA.min(axis=0).values
        self.X3_max = X3_upper.max(axis=0).values
        self.X3_min = X3_upper.min(axis=0).values
        
        position = 0
        my_action = 0
        testing_day = 0
        while testing_day < trades.shape[0]:
            my_action = 0
            if not np.isnan(X3_upper.iloc[testing_day].values):
                
                state_1 = self.discretize(1, X1_Momentum[testing_day-self.N+1])
                state_2 = self.discretize(2, X2_SMA.iloc[testing_day].values)
                state_3 = self.discretize(3, X3_upper.iloc[testing_day].values)
                
                state = state_1*self.states_N**2 + state_2*self.states_N + state_3
                if position == -200:
                    action = self.learner0.querysetstate(state)
#                    my_action = action*200                       
                    new_position = position + action*200
                    
                if position == 0:
                    action = self.learner1.querysetstate(state)
#                    my_action = (action-1)*200
                    new_position = position + (action-1)*200
                    
                if position == 200:
                    action = self.learner2.querysetstate(state)
#                    my_action = (action-2)*200
                    new_position = position + (action-2)*200
                    
                my_action = new_position - position
                position = new_position                
                                
            if self.verbose:
                print testing_day, position
            trades.values[testing_day+1,:] = my_action
            testing_day = testing_day + 1

        return trades

if __name__=="__main__":
    print "One does not simply think up a strategy"
