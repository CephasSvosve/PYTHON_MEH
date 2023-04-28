#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:49:07 2023

@author: cephassvosve
"""


from Clock import *
from Utility_Functions import *
from Balance_Sheets import *
from Investment_Strategies import *
import pandas as pd


class Fund(Balance_sheets, Investment_strategies):
    def __init__(self,INVESTMENT_STRATEGY, cash, firms_pool, inventory = 0.,smaller_window= 21, larger_window= 252):
        
        self.ID_NUM              = gen_unique_id()
        self.cash                = cash
        self.inventory           = inventory
        self.firms_pool          = firms_pool
        self.INVESTMENT_STRATEGY = INVESTMENT_STRATEGY
        self.smaller_window      = smaller_window
        self.larger_window       = larger_window
        
        
        
        
        Balance_sheets.__init__(self, self.ID_NUM, INVESTMENT_STRATEGY, firms_pool)
        Investment_strategies.__init__(self, self.ID_NUM, INVESTMENT_STRATEGY, firms_pool
                                       , self.closing_balances,  self.smaller_window, self.larger_window)
       
        
        self.set_initial_balances(cash, init_inventory=self.inventory )
        
    
    
 #%%  
    
    def set_initial_parameters(self):
        self.set_initial_balances(cash, init_inventory)
        
 #%%
 
 
    def get_ID(self):
         return self.ID_NUM
     
    
#%%get data
    def demand(self):
        orders     = self.compute_demand()
        return orders
       
    