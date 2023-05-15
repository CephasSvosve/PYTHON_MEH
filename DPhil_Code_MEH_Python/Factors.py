#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:01:23 2023

@author: cephassvosve
"""

import numpy as np
import pandas as pd
# import seaborn as sns

# factors = pd.read_csv('/Users/cephassvosve/Desktop/DPhil Data/Factors.csv')
# column = 'SP500'
# sns.histplot(factors[column])
# print('mean',factors[column].mean())
# print('std',factors[column].std())
# print('skew',factors[column].skew())
# print('kurtosis',factors[column].kurtosis())
# # Mkt-RF	SMB	HML	RMW	CMA	SP500

allstocks = pd.read_csv('/Users/cephassvosve/Desktop/Sam Cohen Collabo/Data/allUSStocks2.csv')
print('all')
print(allstocks.head(1000))