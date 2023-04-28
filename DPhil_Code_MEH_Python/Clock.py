#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:47:17 2023

@author: cephassvosve
"""


import configparser




#%%
config          = configparser.ConfigParser()
config.read('Config.ini')
#%%

    
 
#%%    
def time():
    time = config['TIME']['now']
    return int(time)
#%%





#%%
def update_time():
    now                     = config['TIME']['now']
    _next_                  = int(now) + 1
    config['TIME']['now']   = str(_next_)
   
    with open('Config.ini', 'w') as configfile:    # save
        config.write(configfile)
#%%        





#%%
def clock_settings(period, dt):
    st                      = 252
    config['TIME']['start'] = str(st)
    config['TIME']['now']   = str(st)
    config['TIME']['end']   = str(period)
    config['TIME']['dt']    = str(dt)
    
#%%





#%%
def end_time():
    return int(config['TIME']['end']) 
#%%





#%%
def reset_time(period, dt):
    config['TIME']['start'] = str(0)
    config['TIME']['now']   = str(0)
    config['TIME']['end']   = str(period)
    config['TIME']['dt']    = str(dt)
    
#%%

