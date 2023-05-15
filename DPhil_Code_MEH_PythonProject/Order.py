#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:48:21 2023

@author: cephassvosve
"""

from Clock import *
from Utility_Functions import *

class Order:
    def __init__(self, ID_NUM, INVESTMENT_STRATEGY):
        
        self.order_message = {'Date'        : None,
                      'Traders_ID'          : ID_NUM,
                      'INVESTMENT_STRATEGY' : INVESTMENT_STRATEGY,
                      'Asset_ID'            : None,
                      'Exs_demand'          : None,
                      'Bid_price'           : None,
                      'Bid_qty'             : None,
                      'Ask_price'           : None,
                      'Ask_qty'             : None,
                      'Net_demand'          : None
                      }
        
 #%%   
    def order(self, Asset_ID, exs_demand = 0., Bid_price=0., Bid_qty=0., Ask_price=0., Ask_qty=0.):
        self.order_message['Date']                  = time()
        self.order_message['Asset_ID']              = Asset_ID
        self.order_message['Exs_demand']            = exs_demand
        self.order_message['Bid_price']             = Bid_price
        self.order_message['Bid_qty']               = Bid_qty
        self.order_message['Ask_price']             = Ask_price
        self.order_message['Ask_qty']               = Ask_qty
        self.order_message['Net_demand']            = Bid_qty + Ask_qty
        self.order_message['Wealth_allocation']     = (Bid_qty*Bid_price) + (Ask_qty*Ask_price)
        
        return self.order_message