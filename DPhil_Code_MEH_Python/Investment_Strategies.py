#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:50:31 2023

@author: cephassvosve
"""
from Clock import *
from Order import *
from Firm import *
from Utility_Functions import *
import numpy as np

class Investment_strategies:
    def __init__(self, ID_NUM, INVESTMENT_STRATEGY, firms_pool, closing_balances,smaller_window= None, larger_window= None,):
        
        self.ID_NUM             = ID_NUM
        self.firms_pool         = firms_pool
        self.closing_balances   = closing_balances
        self.INVESTMENT_STRATEGY= INVESTMENT_STRATEGY
        self.noise              = None
        self.smaller_window     = smaller_window
        self.larger_window      = larger_window
    
    
    
#%%   
    def create_order(self, Asset_ID, signal):
        cash        = self.closing_balances.get('Cash')
        wealth      = self.closing_balances.get('Total_wealth')
        quote       = self.firms_pool.get(Asset_ID).get_last_quote()
        exs_demand  = (quote/200)*(wealth * signal -  self.closing_balances.get('Inventory').get(Asset_ID)*quote)
        Bid_price   = quote
        Ask_price   = quote
        qty         = (exs_demand/Bid_price) 
     
        Bid_qty     = np.max((0.,qty))
        Ask_qty     = np.min((0.,qty))
        
        
        
        orderObj = Order(self.ID_NUM, self.INVESTMENT_STRATEGY)
        return orderObj.order(Asset_ID, exs_demand, Bid_price, Bid_qty, Ask_price, Ask_qty)
        
        
        
        
        
        
      
#%%       
    def value_investor(self):
        signals      = {}
        norm_signals = {}
        orders       = {}
        for k,v in self.firms_pool.items():
            quote   = v.get_last_quote()
            value   = v.get_closing_fundamentals().get('Intrinsic_value')
           
            signal  = np.sign(-np.log(quote/value))
            
            signals.update({k:signal})
            
        
         
        
        norm_factor      = 0 if sum(np.abs(v) for v in signals.values()) < 0.001 else 1./sum(np.abs(v) for v in signals.values())
        norm_signals     = {k: v*norm_factor for k,v in signals.items()}
        orders           = {k: self.create_order(k,v) for k,v in norm_signals.items()}
        
      
       
        return orders
    
    
    
    
    
     
#%%   
    def noise_trader(self):
        if self.noise is None:
            self.noise = random_number(end_time()+1)
        
        previous_noise =  self.noise[time()]
        current_noise  =  self.noise[time()+1]
        theta          =  1 - (0.5**(1./(6*252)))
        mu             =  0.
        sig            =  0.02
        
        #Uhlenbeck Noise
        X              = previous_noise + theta*(mu-previous_noise) + sig*current_noise
        
       
        
        
        
        
        signals        = {}
        for k,v in self.firms_pool.items():
            quote           = v.get_last_quote()
            value           = v.get_closing_fundamentals().get('Intrinsic_value')
            biased_value    = 2*value * 1./(1+np.exp(-0.1*X))
            signal          = np.sign(-np.log(quote/biased_value)) 
            
            signals.update({k:signal})
            
            
        norm_factor      = 0 if sum(np.abs(v) for v in signals.values()) < 0.001 else 1./sum(np.abs(v) for v in signals.values())
        norm_signals     = {k: v*norm_factor for k,v in signals.items()}
        orders           = {k: self.create_order(k,v) for k,v in norm_signals.items()}
      
        return orders
        
        
        
        
 #%%       
    def passive_investor(self):
        signals          = {}
        assets_in_index  = 2
        for k,v in self.firms_pool.items():
            quote        = v.get_last_quote()
            market_cap   = v.get_closing_fundamentals().get('Issued_shares') * quote
            signal       = market_cap 
            
            
            signals.update({k:signal})
        
        
        # values = list(signals.values())
        # second_highest = sorted(values)[-2]
        
        # # Iterate over the dictionary and set keys with values less than the second highest to 0
        # for key in signals:
        #     if signals[key] < second_highest:
        #         signals[key] = 0
        
        
        norm_factor      = 1./sum(np.abs(v) for v in signals.values())
        norm_signals     = {k: v*norm_factor for k,v in signals.items()}
        orders           = {k: self.create_order(k,v) for k,v in norm_signals.items()}
        
        return orders
        
        
        
        
        
        
#%%       
    def trend_follower(self):
        if time()>= self.larger_window:
            signals = {}
            for k,v in self.firms_pool.items():
                ma_smaller_window   = np.mean(v.get_quote_ts(window_size = self.smaller_window))
                ma_larger_window    = np.mean(v.get_quote_ts(window_size = self.larger_window))
           
                signal              = np.sign(-np.log(ma_larger_window/ma_smaller_window))
                
                signals.update({k:signal})
                
            norm_factor      = 0 if sum(np.abs(v) for v in signals.values()) < 0.001 else 1./sum(np.abs(v) for v in signals.values())
            norm_signals     = {k: v*norm_factor for k,v in signals.items()}
            orders           = {k: self.create_order(k,v) for k,v in norm_signals.items()}
            
            return orders
        else:
            pass
    
    
    
    
    
    
#%%    
    def compute_demand(self):
        result = {}
        if self.INVESTMENT_STRATEGY == 'value':
            result = self.value_investor()
            
            
        elif self.INVESTMENT_STRATEGY == 'passive':
            result = self.passive_investor()
            
        elif self.INVESTMENT_STRATEGY == 'trend':
            result = self.trend_follower()
            
        elif self.INVESTMENT_STRATEGY == 'noise':
            result = self.noise_trader()
        
        return result