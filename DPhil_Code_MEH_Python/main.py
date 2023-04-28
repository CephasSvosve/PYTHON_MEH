#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 15:32:29 2023

@author: cephassvosve
"""

from Clock import * 
from Fund import *
from Market_Clearer import *
import time as t
import sys
import pandas as pd




#%%
def to_csv(funds, firms, allocators = None):
    for k,v in funds.items():
        v.to_csv()
        
        
    for k,v in firms.items():
        v.to_csv()
        
        
    if len(allocators())>0:
       for k,v in allocators.items():
           v.to_csv
    



#%%
def run(period,allocation):
    
 
    #set clock
    clock_settings(period, 1)
    reset_id_generator()
    
    
    
    
    #set firms
    num_firms   = 3
    firms       = {}
    for n_firms in range(num_firms):
        firm = Firm( capital = 10000., issued_shares = 5000.)
        firms[firm.get_ID()] = firm
        
    
   
#%%input data
    header_list     = list(firms.keys())
    fundamentals_df = pd.read_csv('Fundamentals.csv', header = None)
    payout_ratios   = pd.read_csv('Payout_ratios.csv', header = None)
    
    
    
    fundamentals_df.columns = header_list
    payout_ratios.columns   = header_list
    
   
    
#%%associating firms with input data
    for ID, firm in firms.items():
        firm.set_initial_fundamentals(fundamentals_df, payout_ratios)
        firm.set_initial_attributes()
        
        
       
        
    
    
    
   
#%%set funds
    
    funds        = {}
    wealth_share = {}
    if allocation[0]>0:
        funds['passive']        =  Fund('passive', cash = 0., firms_pool = firms)
        wealth_share['passive'] =  allocation[0]
    if allocation[1]>0:
        funds['noise']          =  Fund('noise',   cash = 0., firms_pool = firms)
        wealth_share['noise']   =  allocation[1]
    if allocation[2]>0:
        funds['value']          =  Fund('value',   cash = 0., firms_pool = firms)
        wealth_share['value']   =  allocation[2]
    if allocation[3]>0:
        funds['trend']          =  Fund('trend',   cash = 0., firms_pool = firms)
        wealth_share['trend']   =  allocation[3]
    
    
    
    
    #set allocaters
    
    
    #set market clearer
    mm               = Market_clearer('mm', cash = 0., firms_pool = firms, inventory = 0.)
    
    
   
#%% time the program and run the model

    program_starts = t.time()
    
    
    total_wealth = 30000.
    opening_wealth_vector = {}
    closing_wealth_vector = {}
    returns_vector        = {}
    
    for ID,fund in funds.items():
        returns_vector[ID] = 1
    while(time() < end_time()):
        
        
        
        
       
        #Replenish wealth
        for ID,fund in funds.items():
            allocated_wealth = total_wealth * wealth_share[ID]/100.
            fund.set_wealth(allocated_wealth)
            opening_wealth_vector[ID] = allocated_wealth
        
        
        total_wealth = 0.
        value, quotes  = mm.clear_stock_markets(funds)
        
        
        
        for ID,fund in funds.items():
            closing_wealth_vector[ID] = fund.get_closing_balances().get('Total_wealth')
            total_wealth              += fund.get_closing_balances().get('Total_wealth')
       
        if time()>252:
            for ID, wealth in closing_wealth_vector.items():
                returns              = wealth/opening_wealth_vector.get(ID)
                returns_vector[ID]  *=  returns
                
       
        print('day',time())
        update_time()
        
        
    for fund, agg_ret in returns_vector.items(): 
        returns_vector[fund] = agg_ret**(252/(period-252)) -1
        
    
    
    
    
    now = t.time()
    print("took {0}sec to complete the run!".format(now - program_starts))
    
    for ID, firm in firms.items():
        firm.plot_price_vs_value()
     
    return returns_vector
    

data = {}
scale = 100
df = pd.DataFrame()
for i in range(scale):
    if i > 50:
        for j in range(scale):
            for k in range(scale):
               if ((100-i)**2) + (j**2)+(k**2)+((scale-(i+j+k))**2) < (scale**2):
                    wealth_allocation = [100-i,j,k,scale-(100-i+j+k)]
                   
                    returns = run(1512,wealth_allocation)
                    print('returns',returns)
                    alloc_dict  = {'0':i,'1':j,'2':k,'3':scale-(i+j+k)}
                    alloc_dict.update(returns)
                    df = df.append(alloc_dict,ignore_index=True)
                    print('result_dict',alloc_dict)
                    df.to_csv('current_output1.csv')
                    print(returns)
                     
         
     
    
                
       
    

                
print('done!')       
        
        #get funds' wealths
        #find wealthiest fund
        #allocate wealth to poorer funds to restore distribution
        
       
