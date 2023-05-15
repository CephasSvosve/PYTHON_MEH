#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 20:13:10 2023

@author: cephassvosve
"""

import numpy as np
import pandas as pd
from scipy.stats import skewnorm
import math


def cumprod(lst):
    results = []
    cur = 1
    for n in lst:
        cur *= n
        results.append(cur)
    return results


df = pd.DataFrame()
normal = list(skewnorm.rvs(-5.2,loc = 1.012, scale = 0.01,size = 10000)) # (np.random.normal(1.012,0.012,10000,))
normal = cumprod(normal)
normal2 = [100*v for v in normal]

df['price'] = normal2
print(df.head())
for num in range(1,15):
    df[num]     =  np.log(df.price) -  np.log(df.price.shift(num))
    
df.to_csv('/Users/cephassvosve/Desktop/DPhil Data/dfout.csv')