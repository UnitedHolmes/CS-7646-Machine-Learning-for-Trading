"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def author():
    return 'yzhu94'

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000):
    # this is the function the autograder will call to test your code
    # TODO: Your code here
    df = pd.read_csv(orders_file)
    df = df.sort_values('Date', axis=0, ascending=1)   
    
    df_array = df.as_matrix()

#    operation_dates = df.Date.unique()
    operation_dates = np.unique(df_array[:,0])
    dates = pd.date_range(operation_dates[0],operation_dates[-1])
    syms_ob = df.Symbol.unique()
    syms = list(syms_ob)
    
    prices_all = get_data(syms,dates)
    prices = prices_all[syms].as_matrix()
    
    trading_dates = prices_all.index

    port_cash = np.zeros([len(trading_dates),1])
    port_stock_shares = np.zeros([len(trading_dates),len(syms)])
    port_stock_values = np.zeros([len(trading_dates),len(syms)])

#    start_val = 1000000
    k = 0

    while k < len(trading_dates):   
    #before the trading day, set the initial values from previous day
        if k == 0:
            port_cash[k] = start_val
        else:
            port_cash[k] = port_cash[k-1]
            port_stock_shares[k,:] = port_stock_shares[k-1,:]        
    
        # start the trading day updates
        kk = 0    
        while kk < df.Date.count():
        # There is operation
            if df_array[kk,0] == str(trading_dates[k].date()):
            
#                print ' \nk = ' + str(k)           

                if df_array[kk,2] == 'BUY':
#                if df.Order[kk] == 'BUY':
                    flag_port = -1
#                    print 'BUY'
                elif df_array[kk,2] == 'SELL':
#                elif df.Order[kk] == 'SELL':
                    flag_port = 1
#                    print 'SELL'
                
#                df.Symbol[kk] ---> df_array[kk,1]
#                df.Shares[kk] ---> df_array[kk,3]
                port_stock_shares[k,df_array[kk,1] == syms_ob] = port_stock_shares[k,df_array[kk,1] == syms_ob] - flag_port*df_array[kk,3]
                
                port_cash[k] = port_cash[k] + flag_port*df_array[kk,3]*prices[k,df_array[kk,1] == syms_ob]           
            
                penalties = 0.005*df_array[kk,3]*prices[k,df_array[kk,1] == syms_ob] + 9.95
#                print df_array[kk,1]
#                print penalties
                port_cash[k] = port_cash[k] - penalties
            
#                print 'kk = ' + str(kk)
            
            kk += 1
        
        # No matter if there is an operation, update port values
        for kk in range(0,len(syms)):
            port_stock_values[k,kk] = port_stock_shares[k,kk] * prices[k,kk]
            
        # Decide leverage
        leverage = np.sum(np.abs(port_stock_values[k,:]))/ (np.sum(port_stock_values[k,:]) + port_cash[k])
        if leverage > 2.0:
            if k == 0:
                port_cash[k] = start_val
                port_stock_shares[k,:] = 0
                port_stock_values[k,:] = 0
            elif k > 0:
                old_leverage = np.sum(np.abs(port_stock_values[k-1,:]))/ (np.sum(port_stock_values[k-1,:]) + port_cash[k-1])
                if old_leverage <= leverage:
                    port_cash[k] = port_cash[k-1]
                    port_stock_shares[k,:] = port_stock_shares[k-1,:]
                    port_stock_values[k,:] = port_stock_values[k-1,:]
           
        k += 1

    port_cash = port_cash.reshape([len(port_cash),1])
    port_stock_values_sum = np.sum(port_stock_values,axis=1)
    port_stock_values_sum = port_stock_values_sum.reshape([len(port_stock_values_sum),1])
    portvals = pd.Series(np.sum(np.hstack((port_cash, port_stock_values_sum)),axis=1), index=trading_dates)

    return portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-05-noleverage.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
