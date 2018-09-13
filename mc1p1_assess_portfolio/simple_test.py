# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 14:10:46 2018

@author: UnitedHolmes
"""
import numpy as np
import pandas as pd

df = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar',
                          'foo', 'bar', 'foo', 'foo'],
                       'B' : ['one', 'one', 'two', 'three',
                        'two', 'two', 'one', 'three']})
#                   'C' : np.random.randn(8),
#                    'D' : np.random.randn(8)})
print(df.loc())
grouped = df.groupby('A')

for name, group in grouped:
    print(name)
    print(group)
    
my_list = list(grouped)
print(grouped)