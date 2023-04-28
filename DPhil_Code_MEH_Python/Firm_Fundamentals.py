#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:52:04 2023

@author: cephassvosve
"""

from Clock import *
from Utility_Functions import *
import pandas as pd

class Firm_fundamentals:
    def __init__(self, ID_NUM, capital, issued_shares):
        
        self.ID_NUM                 = ID_NUM
        self.capital                = capital
        self.issued_shares          = issued_shares
        self.fundamentals_ts        = pd.DataFrame()
        self.fundamentals_df        = None
        self.payout_ratios          = None
        
        self.opening_fundamentals   = {'Date'           : None,
                                       'ID_NUM'         : self.ID_NUM,
                                       'EPS'            : None,
                                       'Payout_ratio'   : None,
                                       'DPS'            : None,
                                       'Issued_shares'  : self.issued_shares,
                                       'Capital'        : self.capital,
                                       'Total_earnings' : None,
                                       'Total_div'      : None,
                                       'Book_value'     : None,
                                       'Intrinsic_value': None
                                        }
        
        self.closing_fundamentals   = self.opening_fundamentals
        
        
        
#%%    
   
    def associate_fundamnetals(self, fundamentals_df, payout_ratios):
        self.fundamentals_df        = fundamentals_df
        self.payout_ratios          = payout_ratios
        
#%%

    def record_fundamentals(self):
        self.fundamentals_ts = self.fundamentals_ts.append(self.closing_fundamentals, ignore_index= True)
    
    def get_fundamentals_ts(self):
       return self.fundamentals_ts 
        
#%% 
    def set_initial_fundamentals(self, fundamentals_df, payout_ratios):
        self.associate_fundamnetals(fundamentals_df, payout_ratios)
        self.opening_fundamentals['Date']               = 0
        self.opening_fundamentals['EPS']                = self.fundamentals_df.iloc[0][self.ID_NUM].item()
        self.opening_fundamentals['Payout_ratio']       = self.payout_ratios.iloc[0][self.ID_NUM].item()
        self.opening_fundamentals['DPS']                = self.opening_fundamentals.get('EPS') * self.opening_fundamentals.get('Payout_ratio')/self.opening_fundamentals.get('Issued_shares')
        self.opening_fundamentals['Issued_shares']      = self.issued_shares
        self.opening_fundamentals['Capital']            = self.capital
        self.opening_fundamentals['Total_earnings']     = self.opening_fundamentals.get('EPS') * self.opening_fundamentals.get('Issued_shares')
        self.opening_fundamentals['Total_div']          = self.opening_fundamentals.get('DPS') * self.opening_fundamentals.get('Issued_shares')
        self.opening_fundamentals['Book_value']         = self.capital + self.opening_fundamentals.get('Total_earnings')
        self.opening_fundamentals['Intrinsic_value']    = self.opening_fundamentals.get('EPS')#self.opening_fundamentals.get('Book_value')/self.opening_fundamentals.get('Issued_shares')
        self.closing_fundamentals                       = self.opening_fundamentals
        self.record_fundamentals()
        
#%%        
    
    
        
    def update_fundamentals(self):
        self.opening_fundamentals                       = self.closing_fundamentals 
        self.closing_fundamentals['Date']               = time()
        self.closing_fundamentals['EPS']                = self.fundamentals_df.iloc[time()][self.ID_NUM].item()
        self.closing_fundamentals['Payout_ratio']       = self.opening_fundamentals.get('Payout_ratio')
        self.closing_fundamentals['DPS']                = self.closing_fundamentals.get('EPS') * self.closing_fundamentals.get('Payout_ratio')/self.opening_fundamentals.get('Issued_shares')
        self.closing_fundamentals['Issued_shares']      = self.opening_fundamentals.get('Issued_shares')
        self.closing_fundamentals['Capital']            = self.capital
        self.closing_fundamentals['Total_earnings']     = self.closing_fundamentals.get('EPS') * self.opening_fundamentals.get('Issued_shares')
        self.closing_fundamentals['Total_div']          = self.closing_fundamentals.get('DPS') * self.opening_fundamentals.get('Issued_shares')
        self.closing_fundamentals['Book_value']         = self.opening_fundamentals.get('Book_value') + self.closing_fundamentals.get('Total_earnings')
        self.closing_fundamentals['Intrinsic_value']    = self.opening_fundamentals.get('EPS')#self.closing_fundamentals.get('Book_value')/self.closing_fundamentals.get('Issued_shares')
        self.closing_fundamentals                       = self.opening_fundamentals
        self.record_fundamentals()
    
#%%getters
    def get_closing_fundamentals(self):
        return self.closing_fundamentals 
    
    
    
    
    def get_opening_fundamnetals(self):
        return self.opening_fundamentals

        
#%%getters  