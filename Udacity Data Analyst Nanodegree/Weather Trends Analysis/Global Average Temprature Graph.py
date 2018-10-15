# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 19:28:37 2018

@author: Saurabh
"""
# importing the important libraries

import numpy as np
import pandas as pd      # for loading data into the notebook
from matplotlib import pyplot as plt # for plotting the line chart

# importing the extracted data set

data = pd.read_csv("joined_global_city_tables.csv")

# function that calculates the rolling average


output = data.rolling(window = 170, center = False, on = "city_avg_temp").mean().dropna()
    

plt.plot(output['year'], output['glob_avg_temp'], label = 'Global Average')
plt.legend()
plt.xlabel("Years")
plt.ylabel("Temprature (°C)")
plt.title("Global Average Temprature")
plt.show()



