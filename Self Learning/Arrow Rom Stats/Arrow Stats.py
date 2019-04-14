
# coding: utf-8

# In[21]:


# Loading required libraries
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# # The latest stats are grabbed everytime the code executes

# In[22]:


# loading tables 
tables = pd.read_html("https://stats.arrowos.net/")

print(tables[1])


# # the stats are saved to a csv file on the local directory

# In[23]:


# saving this table to a csv file
tables[1].to_csv("stats by device.csv", index=False)


# In[24]:


# loading the data back into dataframe
stats_device = pd.read_csv("stats by device.csv")


# In[25]:


# dropping the NaN column
stats_device = stats_device.drop('Unnamed: 4' ,axis = 1)
stats_device_top10 = stats_device[0:10]


# # Top 10 devices by install base in Pie

# In[26]:


# Pie chart for pie installs
plt.figure(figsize = (10 ,10))
labels = stats_device_top10['Codename']
sizes = stats_device_top10['Pie Installs']
#colors
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
 
fig1, ax1 = plt.subplots()
ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90)
#draw circle
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
# Equal aspect ratio ensures that pie is drawn as a circle
ax1.axis('equal')  
plt.tight_layout()
plt.show()


# In[28]:


# bar charts for pie installs
plt.figure(figsize = (10 ,10))
height = stats_device_top10['Pie Installs']
bars = stats_device_top10['Codename']
y_pos = np.arange(len(bars))
 
# Create bars
plt.bar(y_pos, height)
 
# Rotation of the bars names
plt.xticks(y_pos, bars, rotation=90)
 
# Custom the subplot layout
plt.subplots_adjust(bottom=0.4, top=0.99)
 
# Show graphic
plt.show()


# # Top 10 devices by install base in Oreo

# In[29]:


# pie chart for oreo installs
plt.figure(figsize = (10 ,10))
labels = stats_device_top10['Codename']
sizes = stats_device_top10['Oreo Installs']
#colors
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
 
fig1, ax1 = plt.subplots()
ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90)
#draw circle
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
# Equal aspect ratio ensures that pie is drawn as a circle
ax1.axis('equal')  
plt.tight_layout()
plt.show()


# In[27]:


# Bar charts for oreo installs
plt.figure(figsize = (10 ,10))
height = stats_device_top10['Oreo Installs']
bars = stats_device_top10['Codename']
y_pos = np.arange(len(bars))
 
# Create bars
plt.bar(y_pos, height)
 
# Rotation of the bars names
plt.xticks(y_pos, bars, rotation=90)
 
# Custom the subplot layout
plt.subplots_adjust(bottom=0.4, top=0.99)
 
# Show graphic
plt.show()


