#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:50:01 2023

@author: cephassvosve
"""



from Firms_Master_File import *
import matplotlib.pyplot as plt



#%%
class Firm(Firms_master_file):
    def __init__(self, capital, issued_shares):
        self.ID_NUM = gen_unique_id()
        
        Firms_master_file.__init__(self, self.ID_NUM, capital, issued_shares)
       
        
    
       
    
    
    
#%%    
    def dividend_paid_out(self):
        return self.get_closing_fundamentals().get('DPS')
    
    
    
    
    
    
    
#%%      
    def merge_fundamentals(self):
        df = pd.merge(self.attributes_df, self.fundamentals_ts)
        return df
    
    
    
    

    
#%%      
    def set_quote(self, new_quote):
        self.attributes['Bid_price'] = new_quote
        self.attributes['Ask_price'] = new_quote
        self.attributes['Mid_price'] = new_quote
       
    
     
#%%      
    def set_market_cap(self, market_cap):
        self.attributes['Market_cap'] = market_cap
        
       
       
    
    
    
   
    
    
#%%      
    def get_last_quote(self):
        return self.attributes.get('Mid_price')
    
    
    
    
    
     
#%%     
    def get_t_minus_n_quote(self, n = 1):
        quote = self.attributes_df.Mid_price.tail(n)[:1].item()
        return quote
    
    
    
    
     
#%%     
    def get_quote_ts(self, window_size = 21):
        return self.attributes_df.Mid_price.tail(window_size)
    
    
    
    
    
#%%      
    def get_market_cap(self):
        return self.attributes.get('Market_cap')
    
    



    
#%%      
    def get_ID(self):
        return self.ID_NUM
    
 



  #%%      
    def plot_price_vs_value(self, start = 0):
        df = self.merge_fundamentals()
        df = df.tail(df.shape[0]-start)
        plt.scatter(df['Mid_price'], df['Intrinsic_value'], marker = '.',linewidths=0.01,c = 'black')
        plt.xlabel('Price')
        plt.ylabel('Value')
        plt.show()
        
        df['Date'] = df['Date'].astype(int)
        df         = df.set_index('Date')
        
        plt.plot(df[['Mid_price','Intrinsic_value']])
        # plt.xticks(range(df.index.min(), df.index.max()+1))
    
        plt.xlabel('date')
        plt.ylabel('USD')
        plt.legend(['Price','Intrinsic_value'],loc='lower right')
        plt.show()
         
        # plt.plot(df['Mid_price'])
        # # plt.xticks(range(df.index.min(), df.index.max()+1))
    
        # plt.xlabel('date')
        # plt.ylabel('USD')
        # plt.legend(['Price'],loc='lower right')
        # plt.show()
         
          
          
        
    
    
#%%      
    def to_csv(self):
        self.merge_fundamentals().to_csv('Firms_data.csv')
        
    