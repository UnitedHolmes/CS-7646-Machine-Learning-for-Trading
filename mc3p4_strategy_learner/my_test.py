# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 15:36:29 2017

@author: NFLS_UnitedHolmes
"""

import StrategyLearner as sl
import datetime as dt
import pandas as pd
from util import get_data, plot_data
import util as ut
import time
#from grade_strategy_learner.py import compute_portvals


def compute_portvals(df_trades, \
                     symbol = 'AAPL', \
                     sd=dt.datetime(2010,1,1), \
                     ed=dt.datetime(2011,12,31), \
                     sv=100000):
    
    syms=[symbol]
    dates = pd.date_range(sd, ed)
    prices_all = ut.get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices = prices.fillna(method='ffill').fillna(method='bfill')

#    port_value = prices_all[syms]     
#    port_value.values[:,:] = 0
#    port_value.values[0,:] = sv
    cash = sv
    
    days = -1
    position = 0
    while (days<prices.shape[0]-1):
        days = days + 1
        if abs(df_trades.iloc[days].values) < 200:
            continue
        else:
            position = position + df_trades.iloc[days].values
            penalty = 9.95 + abs(df_trades.iloc[days].values) * prices.iloc[days].values *0.005
#            penalty = 0
            cash = cash - df_trades.iloc[days].values * prices.iloc[days].values - penalty
    
    return cash + position * prices.iloc[-1].values


start_time = time.time()

learner = sl.StrategyLearner(verbose=False)
learner.addEvidence(symbol = "UNH", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000)
df_trades = learner.testPolicy(symbol = "UNH", \
                               sd=dt.datetime(2010,1,1), \
                               ed=dt.datetime(2011,12,31), \
                               sv = 100000) # testing phase
#print df_trades[df_trades.values != 0]
df_portvals = compute_portvals(df_trades, \
                               symbol = 'UNH', \
                               sd=dt.datetime(2010,1,1), \
                               ed=dt.datetime(2011,12,31), \
                               sv=100000)
print df_portvals/100000 - 1
print time.time()-start_time