# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 13:17:59 2018

@author: Saurabh
"""

# IMPORTING THE NEEDED LIBRARIES 
 
import numpy as py 
 
import panda as pd 
 
from matplotlib import pyplot as plt 

#IMPORTING THE EXTRACTED DATA 
 
data = pd.read_csv(“joined_global_city_tables.csv”) 
 
#I HAVE TAKEN 170 AS DEFAULT VALUE FOR THE WINDOW FOR A SMOOTHER GRAPH
 
output = data_input.rolling(window = 170, center = false, on = “city_avg_temp”).mean().dropna() 


 
#PLOTTING THE GRAPH: GLOBAL TEMPRATURES 
plt.plot(output ['year'], output ['global_avg_temp'], label = 'Global') 
plt.legend() 
plt.xlabel ("Years") 
plt.ylabel ("Temperature (°C)")  
plt.title ("Global Average Temperature")
plt.show()
