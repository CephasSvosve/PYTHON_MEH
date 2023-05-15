#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:49:23 2023

@author: cephassvosve
"""

from Clock import *
from Firm_Fundamentals import *
import pandas as pd
import numpy as np


class Firms_master_file(Firm_fundamentals):
    def __init__(self, ID_NUM, capital, issued_shares):
       
        
        self.ID_NUM         = ID_NUM
        self.issued_shares  = issued_shares
        
        self.attributes     = {'Date'           : None,
                               'ID_NUM'         : self.ID_NUM,
                               'Bid_price'      : None,
                               'Ask_price'      : None,
                               'Mid_price'      : None,
                               'Market_cap'     : None,
                               'Issued_shares'  : self.issued_shares,
                                }
        
        self.attributes_df  = pd.DataFrame(columns = list(self.attributes.keys()))
        Firm_fundamentals.__init__(self, self.ID_NUM, capital, issued_shares)

#%%        
    def record_attributes(self):
        self.attributes_df = self.attributes_df.append(self.attributes, ignore_index= True)
        
        
        
    def set_initial_attributes(self, init_price = None):
        self.attributes['Date']      = 0
        self.attributes['Bid_price'] = self.opening_fundamentals.get('Intrinsic_value') 
        self.attributes['Ask_price'] = self.opening_fundamentals.get('Intrinsic_value') 
        self.attributes['Mid_price'] = np.mean(np.array([self.attributes.get('Bid_price'), self.attributes.get('Ask_price')]))
        self.attributes['Market_cap']= self.attributes.get('Mid_price') * self.issued_shares
        self.record_attributes()
        
        
        
    def update_attributes(self, bid, ask):
        self.attributes['Date']      = time()
        self.attributes['Bid_price'] = bid
        self.attributes['Ask_price'] = ask
        self.attributes['Mid_price'] = np.mean(np.array([self.attributes.get('Bid_price'), self.attributes.get('Ask_price')]))
        self.attributes['Market_cap']= self.attributes.get('Mid_price') * self.issued_shares
        self.record_attributes()
       
        
        
    def get_attributes(self):
        return self.attributes
    
    
    def reset_market_cap(self):
        self.attributes['Market_cap'] = 0.
        
#%%        
         
         