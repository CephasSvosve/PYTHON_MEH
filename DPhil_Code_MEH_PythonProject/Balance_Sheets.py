#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:49:42 2023

@author: cephassvosve
"""
from Clock import *
import pandas as pd

class Balance_sheets:
    def __init__(self,ID_NUM, INVESTMENT_STRATEGY, firms_pool):
        self.firms_pool           = firms_pool
        self.INVESTMENT_STRATEGY  = INVESTMENT_STRATEGY
        self.df                   = pd.DataFrame()
        self.initial_inventory    = {}
        self.dividend             = 0.
        
        
        
        self.opening_balances    = {'Date'        : 0,
                                    'ID_NUM'      : ID_NUM,
                                    'Cash'        : None,
                                    'Inventory'   : {},
                                    'Total_wealth': None,
                                    'Div_received': None
                                    }
        
        
        self.closing_balances =  self.opening_balances 
    
    
  
    
#%%record data to an external file
    
 
    def record_balance(self):
        self.df = self.df.append(self.closing_balances, ignore_index = True)
   
        

    def to_csv(self):
        self.df.to_csv(INVESTMENT_STRATEGY, index=False)
        
        
        
        
    def set_wealth(self,inventory = 0., cash = 0.):
        inventory = inventory/3.
        # for k, v in self.firms_pool.items():
        #     self.closing_balances['Inventory'][k] = 0.
        self.opening_balances['Cash']           = self.opening_balances['Cash'] + cash
        self.opening_balances['Total_wealth']   = self.opening_balances['Total_wealth']   + cash 
        
        
        self.closing_balances['Cash']           = self.closing_balances['Cash'] + cash
        self.closing_balances['Total_wealth']   = self.closing_balances['Total_wealth']   + cash 
        
        for ID, firm in self.firms_pool.items():
            self.opening_balances['Inventory'][ID]  = inventory/firm.get_last_quote()
            self.opening_balances['Total_wealth']   = self.opening_balances['Total_wealth'] + inventory*firm.get_last_quote()
        
            self.closing_balances['Inventory'][ID]  = inventory/firm.get_last_quote()
            self.closing_balances['Total_wealth']   = self.closing_balances['Total_wealth'] + inventory
        
        
        
        
        
    def add_cash(self,cash):
        # for k, v in self.firms_pool.items():
        #     self.closing_balances['Inventory'][k] = 0.
        self.opening_balances['Cash']           = self.opening_balances['Cash'] + cash
        self.opening_balances['Total_wealth']   = self.opening_balances['Total_wealth']   + cash 
        
        
        self.closing_balances['Cash']           = self.closing_balances['Cash'] + cash
        self.closing_balances['Total_wealth']   = self.closing_balances['Total_wealth']   + cash 
        



 #%%   
    def receive_dividend(self):
        if time()%63 == 0:
            current_cash                           = self.closing_balances['Cash']
            self.closing_balances['Cash']          = current_cash + self.dividend
            self.closing_balances['Total_wealth'] += self.dividend
            self.closing_balances['Div_received']  = self.dividend
            self.dividend        = 0.
        else:
            
            for k,v in self.closing_balances.get('Inventory').items():
                self.dividend    += v * self.firms_pool.get(k).dividend_paid_out()
                
         
        self.closing_balances['Div_received']  = 0.#push this statement inside to allow for dividend payment
        
            
        




        
#%%setters
    def set_initial_balances(self, cash, init_inventory):
        self.opening_balances['Date']             = 0
        self.opening_balances['Cash']             = cash
        
        total_wealth = cash
        for k, v in self.firms_pool.items():
            self.initial_inventory[k]             = init_inventory
            self.opening_balances['Inventory'][k] = init_inventory
            total_wealth                         += init_inventory * v.attributes.get('Bid_price')
        
        
        self.opening_balances['Total_wealth']     = total_wealth
        self.opening_balances['Div_received']     = 0.
        self.closing_balances                     = self.opening_balances

        
        self.record_balance()
        
    
    
    
    
 #%%   
    def update_inventory(self, executed_orders):
        self.receive_dividend()
       
        self.opening_balances                     = self.closing_balances
        self.closing_balances['Date']             = time()
        cash                                      = self.closing_balances['Cash'] 
        cash_spending                             = 0.
   
        
      
        if executed_orders is not None:
            for k, v in executed_orders.items():
              
                self.closing_balances['Inventory'][k] += v/self.firms_pool.get(k).get_last_quote()
                cash_spending                         += -1 * v
     
            
        
        self.closing_balances['Cash']              =  self.closing_balances['Cash'] + cash_spending
        

#%%setters   


    def update_wealth(self):
        cash            = self.closing_balances['Cash'] 
        total_wealth    = 0.
        inventory_wealth= 0.
        
        
        for k,v in self.closing_balances.get('Inventory').items():
            inventory_wealth += v*self.firms_pool.get(k).get_last_quote()
            
        self.closing_balances['Total_wealth']  = total_wealth + cash + inventory_wealth 
        self.record_balance()  
        
            
            
        
        
    def reset_wealth(self):
        self.closing_balances['Total_wealth'] = 0.
        self.closing_balances['Cash']         = 0.
        self.closing_balances['Div_received'] = 0.
        
        for k,v in self.firms_pool.items():
            self.closing_balances['Inventory'][k]    = 0.
        
        
        
        




#%%getters    
    def get_opening_balances(self):
        return self.opening_balances    

    def get_closing_balances(self):
        return self.closing_balances
   
#%%getters