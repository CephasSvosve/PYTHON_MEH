#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:53:21 2023

@author: cephassvosve
"""
from Clock import * 
from Utility_Functions import *
from Fund import *
from Firm import *
from Allocator import *
from scipy.optimize import minimize

#%%
class Market_clearer(Fund):
    def __init__(self, INVESTMENT_STRATEGY, cash, firms_pool, inventory = 0):
        
        
        self.ID_NUM              = gen_unique_id()
        self.INVESTMENT_STRATEGY = INVESTMENT_STRATEGY
        self.firm_pool           = firms_pool
        
        Fund.__init__(self, INVESTMENT_STRATEGY, cash, firms_pool, inventory)
    
 
    
 
 #%%   
    def update_agents(self, funds, firms, executed_orders = None, allocators = None):
        for k,v in funds.items():
            if executed_orders is None:
                v.update_wealth()
            else:
                v.update_inventory(executed_orders.get(k))
              
            
            
        for k,v in firms.items():
            v.update_fundamentals()
           
            
            
        if allocators is None:
            pass
        else:
           for k,v in allocators.items():
               v.update_fundamentals()
               v.update_attributes() 


    
   #%%
   
    def search(self, p, funds, k, depth = 1.00):
       self.firms_pool.get(k).set_quote(p)
       excess_demand, orders_dict  = self.excess_demand(funds, self.firms_pool)
       
       if depth == 0.0001 or np.abs(excess_demand.get(k)) < 0.0001:
           return p,orders_dict
       else:
           ed1    = excess_demand.get(k)
           sign1  = np.sign(ed1)*depth
           sign2 = sign1
           ed2 = ed1
           while( (np.abs(ed2) <= np.abs(ed1)) & (sign1==sign2)):
                p = p + sign1
                
                if p < 0.:
                    p = 0.00001
                
                self.firms_pool.get(k).set_quote(p)
                excess_demand, orders_dict  = self.excess_demand(funds, self.firms_pool)
                ed2                         = excess_demand.get(k)
                sign2                       = np.sign(ed2)*depth
                
                if np.abs(ed2) < 0.1:
                    break
                print('ed11',ed1)
                print('ed21',ed2)
            
           
           p2 = (p + p + sign2)/2 
           if p2 < 0.:
               p2 = 0.00001
           print('p21',p2)
           # if (p2 == p) or (p2 < 0):
           #     while( (np.abs(ed2) <= np.abs(ed1)) & (sign1==sign2)):
           #          p = p - sign1
                    
           #          if p < 0.:
           #              p = 0.00001
           #          self.firms_pool.get(k).set_quote(p)
           #          excess_demand, orders_dict  = self.excess_demand(funds, self.firms_pool)
           #          ed2                         = excess_demand.get(k)
           #          sign2                       = np.sign(ed2)*depth
                    
           #          if np.abs(ed2) < 0.1:
           #              break
           #          print('ed12',ed1)
           #          print('ed22',ed2)
           
           # p2 = (p + p + sign2)/2 
           # print('p22',p2)
           depth2 = depth * 1./10
           return self.search(p2, funds, k, depth = depth2)
       
        
       
       
#%%
    def excess_demand(self,*params):
        funds, firms_pool   = params
        demand_list         = []
        excess_demand       = {}
        orders_dict         = {}
        Q                   = {}
        W                   = {}
        
        #work out the quantity supplied, Q (negative wealth/cost of goods)
        #work out the wealth available to make the purchase ( positive wealth)
        #send out demand and supply
        for ID,fund in funds.items():
            if  fund.closing_balances.get('Total_wealth') > 0.:
                
               
                orders          = fund.demand()  
                
                
               
                for k, v in orders.items():
                    if k in orders_dict.keys():
                        orders_dict[k][ID] = v.get('Exs_demand')
                    else:
                        orders_dict[k]     = {}
                        orders_dict[k][ID] = v.get('Exs_demand')
                        
                        
                    if k in excess_demand.keys():
                        excess_demand[k]  += v.get('Exs_demand')
                    else:
                        excess_demand[k]   = v.get('Exs_demand')
                       
            else:
                fund.reset_wealth()
                print(ID, ' is bankrupt')
        
        return excess_demand, orders_dict
    
    









#%%
# clear by matching submitted demand
    # def clear_stock_markets(self, funds):
    
    #     excess_demand, orders_dict = self.excess_demand(funds, self.firms_pool)

    #     funds_orders                = {}
    #     value                       = {}
    #     quotes                      = {}
    #     executed_orders             = {}
        
        
   
    #     #update number of shares
    #     for odered_asset, orders_submitted in orders_dict.items():
    #         abs_sum = 0
    #         for trading_agent, order_size in orders_submitted.items():
    #             abs_sum += abs(order_size) 
                
    
    #         if abs(sum(orders_submitted.values())) < abs_sum: #|D(1) +D(2)| < |D(1)| +|D(2)|
            
    #             sum_neg_orders          = abs(sum(size_ for _,size_ in orders_submitted.items() if size_ <0.))
    #             sum_pos_orders          = abs(sum(size_ for _,size_ in orders_submitted.items() if size_ >0.))
    #             exchanged_shares        = 0.5*(abs_sum - abs(sum(orders_submitted.values())))
    #             for trading_agent, order_size in orders_submitted.items():
    #                 if trading_agent in executed_orders.keys():
    #                     executed_orders[trading_agent][odered_asset] = (order_size /sum_neg_orders)*exchanged_shares if order_size<0. else (order_size /sum_pos_orders)*exchanged_shares
                      
    #                 else:
    #                     executed_orders[trading_agent] = {}
    #                     executed_orders[trading_agent][odered_asset] = (order_size /sum_neg_orders)*exchanged_shares if order_size<0. else (order_size /sum_pos_orders)*exchanged_shares
                      
                        
    #             self.update_agents(funds,self.firms_pool,executed_orders)
      
    #     for k,v in self.firms_pool.items():
    #         market_cap              = v.attributes.get('Market_cap')
    #         market_cap             += excess_demand.get(k)
    #         new_quote               = market_cap / v.attributes.get('Issued_shares') 
            
            
    #         v.set_quote(new_quote)
    #         v.set_market_cap(market_cap)
    #         quotes.update({k: new_quote})
    #         value.update({k:v.get_closing_fundamentals().get('Intrinsic_value')})
    #         v.update_attributes(new_quote,new_quote)
       
      
    #     self.update_agents(funds,self.firms_pool)
       
        
    #     return value, quotes
#%%    
# clear by matching submitted demand
    def clear_stock_markets(self, funds):
    
        excess_demand, orders_dict  = self.excess_demand(funds, self.firms_pool)

        funds_orders                = {}
        value                       = {}
        quotes                      = {}
        executed_orders             = {}
        
        
    
        
        for k,v in self.firms_pool.items():
            market_cap              = v.attributes.get('Market_cap')
            market_cap             += excess_demand.get(k)
            new_quote               = market_cap / v.attributes.get('Issued_shares') 
            print('Issued shares',v.attributes.get('Issued_shares') )
            
            v.set_quote(new_quote)
            v.set_market_cap(market_cap)
            quotes.update({k: new_quote})
            value.update({k:v.get_closing_fundamentals().get('Intrinsic_value')})
            v.update_attributes(new_quote,new_quote)
            
            for fund, order in orders_dict.get(k).items():
                executed_orders[fund]    = {}
                executed_orders[fund][k] = orders_dict[k][fund]
                self.update_agents(funds,self.firms_pool, executed_orders)
                
      
        self.update_agents(funds,self.firms_pool, executed_orders = None)
       
        
        return value, quotes


  
#%%   
  

#     def objective(self, estimates, funds):
#         for ID, firm in self.firms_pool.items():
#                 firm.set_quote(estimates[int(ID)])
                
            
                                    
#         excess_demand, orders_dict  = self.excess_demand(funds, self.firms_pool)
#         excess_demand               = {k:(v**2) for k,v in excess_demand.items()}
        
#         return sum(excess_demand.values())
    
    
    
    
    
    

#%%
#     def optimization_clearer(self, funds):
       
#         init_estimates              = []
        
#         for ID, firm in self.firms_pool.items():
#             init_estimates.append(firm.attributes.get('Mid_price'))
        
        
        
#         bounds = ((0., None), (0., None), (0., None))
#         res = minimize(self.objective, init_estimates, args = (funds),method='SLSQP', bounds=bounds)

#         print('res', res)
#         for k,v in self.firms_pool.items():
#             new_quote               = res[k]
#             v.set_quote(new_quote)
#             quotes.update({k:new_quote})
#             value.update({k:v.get_closing_fundamentals().get('Intrinsic_value')})
            
#             print('inventory', inventory)
#             od = Order(self.ID_NUM, self.INVESTMENT_STRATEGY)
#             mm_orders.update({k:od.order(k, previous_quote, max(0,-inventory_supply), previous_quote, min(0,-inventory_supply))})
            
#         self.update_balances(mm_orders)  
#         self.update_agents(funds,self.firms_pool,orders_dict)
        
#         return value, quotes

#%%#%%
    def objective(self, estimate, *params):
        funds,k = params
        self.firms_pool.get(k).set_quote(estimate)
                
            
                                    
        excess_demand, orders_dict  = self.excess_demand(funds, self.firms_pool)
        
        
        return (excess_demand.get(k))
    
    
    
    
    
    

#%%
    def optimization_clearer(self, funds):
        mm_orders                   = {}
        value                       = {}
        quotes                      = {}
        
        
        
        for k,v in self.firms_pool.items():
            init_estimate              = v.attributes.get('Mid_price')
            
            bounds = [(0., None)]
            res = minimize(self.objective, init_estimate, args = (funds,k),method='SLSQP', bounds=bounds)

            
            new_quote               = res.x
            quotes.update({k:new_quote}) 
            v.set_quote(init_estimate)
            
        for k,v in self.firms_pool.items(): 
              v.set_quote(quotes.get(k))
              value.update({k:v.get_closing_fundamentals().get('Intrinsic_value')})
               
        excess_demand, orders_dict  = self.excess_demand(funds, self.firms_pool)
        self.update_agents(funds,self.firms_pool,orders_dict)
        
        
        return excess_demand, quotes, value
    
    
    
    
    #%%Aymeric's clearing
        # def excess_demand(self,*params):
        #     funds, firms_pool   = params
        #     demand_list         = []
        #     demand              = {}
        #     inventory           = {}
        #     orders_dict         = {}
            
        #     for ID,fund in funds.items():
                
        #         orders          = fund.demand() if fund.closing_balances.get('Total_wealth') > 0 else None
        #         orders_dict[ID] = {}
        #         print('fund',ID)
                
        #         for k, v in orders.items():
        #             orders_dict[ID][k] = v
                    
        #             if k in demand:
        #                 demand[k]     += v.get('Wealth_allocation')
        #                 inventory[k]  += fund.closing_balances.get('Inventory').get(k)
        #             else:
        #                 demand[k]      = v.get('Wealth_allocation')
        #                 inventory[k]   = fund.closing_balances.get('Inventory').get(k)
                
            
        #     return demand, inventory, orders_dict
        
        

    #%%  Market Maker  
    #     def clear_stock_markets(self, funds):
    #         excess_demand, orders_dict  = self.excess_demand(funds, self.firms_pool)
    #         print('excess_demand', excess_demand)
    #         mm_orders                   = {}
    #         value                       = {}
    #         quotes                      = {}
            
    #         for k,v in self.firms_pool.items():
    #             previous_quote          = v.get_last_quote()
    #             inventory_supply        = excess_demand.get(k)
    #             inventory               = max(0,self.closing_balances.get('Inventory').get(k))
    #             new_quote               = previous_quote * inventory/(inventory - inventory_supply)
    #             v.set_quote(new_quote)
    #             quotes.update({k:new_quote})
    #             value.update({k:v.get_closing_fundamentals().get('Intrinsic_value')})
                
    #             print('inventory', inventory)
    #             od = Order(self.ID_NUM, self.INVESTMENT_STRATEGY)
    #             mm_orders.update({k:od.order(k, previous_quote, max(0,-inventory_supply), previous_quote, min(0,-inventory_supply))})
                
    #         self.update_balances(mm_orders)  
    #         self.update_agents(funds,self.firms_pool,orders_dict)
            
    #         return value, quotes
      
        
      
        
    #%%









    #%%    
        # def clear_stock_markets(self, funds):
        #     wealth_alloc, inventory, orders_dict  = self.excess_demand(funds, self.firms_pool)
        #     print('inventory', inventory)
        #     mm_orders                   = {}
        #     value                       = {}
        #     quotes                      = {}
            
        #     for k,v in self.firms_pool.items():
                
        #         new_quote               = wealth_alloc.get(k)/ inventory.get(k)
                
        #         v.set_quote(new_quote)
        #         quotes.update({k:new_quote})
        #         value.update({k:v.get_closing_fundamentals().get('Intrinsic_value')})
                
                
        
        #     self.update_agents(funds,self.firms_pool,orders_dict)
            
        #     return value, quotes
      
        