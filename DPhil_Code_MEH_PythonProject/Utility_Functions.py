#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:48:31 2023

@author: cephassvosve
"""
import configparser
import numpy as np




#%%
config          = configparser.ConfigParser()
config.read('Config.ini')
#%%






#%%
def gen_unique_id():
    _id_ = config['UNIQUE_IDENTIFIER']['ID'] 
    _id_ = int(_id_) + 1
    
    
    config['UNIQUE_IDENTIFIER']['ID'] = str(_id_)
    
    with open('Config.ini', 'w') as configfile:    # save
        config.write(configfile)
        
    return _id_
#%%




#%%
def reset_id_generator():
    _id_ = -1
    
    
    config['UNIQUE_IDENTIFIER']['ID'] = str(_id_)
    
    with open('Config.ini', 'w') as configfile:    # save
        config.write(configfile)
        
    return _id_
#%%




#%%
def random_number(sample_size, _seed_ = 12345):
    np.random.seed(_seed_)
    return np.random.normal(0.,1.,size = sample_size)
#%%  