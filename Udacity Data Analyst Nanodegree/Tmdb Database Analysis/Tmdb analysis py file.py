
# coding: utf-8

# In[76]:


# importiing the required packages
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from datetime import datetime
get_ipython().run_line_magic('matplotlib', 'inline')


# In[77]:


# loading data from csv file
movie_data = pd.read_csv('tmdb-movies.csv')

# viewing the first few frames of the dataset
movie_data.head(20)


# In[78]:


# removing unnecessary columns by assigning them to an array and then dropping them
useless_col = [ 'id', 'imdb_id', 'popularity', 'budget_adj', 'revenue_adj', 'homepage', 'keywords', 'overview', 'production_companies', 'vote_count', 'vote_average']
movie_data = movie_data.drop(useless_col , 1)


# In[79]:


# previewing the first few frames of the new dataset
movie_data.head(20)


# In[80]:


# checking for duplicates in the given dataset
sum(movie_data.duplicated())


# In[81]:


# checking the initial datashape
movie_data.shape


# In[82]:


# dropping the duplicate dataframes
movie_data.drop_duplicates(keep = 'first' , inplace = True)


# In[83]:


# checking the new datashape
movie_data.shape


# In[84]:


# creating a seperate list of revenue and budget column so as to remove 0's from these series
change_list = ['revenue' , 'budget']

# replacing all 0's with NAN'
movie_data[change_list] = movie_data[change_list].replace(0 , np.NAN)

#dropping NAN
movie_data.dropna(subset = change_list , inplace = True)

# previewing the new datashape
movie_data.shape


# In[85]:


# replacing the 0 values of runtime column with NAN
movie_data['runtime'] = movie_data['runtime'].replace(0 , np.NAN)


# In[86]:


# Checking the datatypes of the given dataset
movie_data.dtypes


# In[87]:


# since the budget and revenue columns is in float, we will change it to int
change_dtype = ['budget' , 'revenue']

# changing the datatype to int
movie_data[change_dtype] = movie_data[change_dtype].applymap(np.int64)

# printing the new datatypes
movie_data.dtypes


# In[88]:


# calculating the profit of each movie
# for this we are going use the function insert to create a new column called profit_earned
movie_data.insert(2 , 'profit_earned' , movie_data['revenue']-movie_data['budget'])

# previewing the new dataset
movie_data.head(20)


# In[89]:


# movies which earned the highest and lowest profit
# we are going to define a function for gettig the answer to this question
def calculate_max_min(column):

    highest_profit_id = movie_data[column].idxmax()
    highest_profit_id_details = pd.DataFrame(movie_data.loc[highest_profit_id])

    lowest_profit_id = movie_data[column].idxmin()
    lowest_profit_id_details = pd.DataFrame(movie_data.loc[lowest_profit_id])

#collecting data in one frame

    show = pd.concat([highest_profit_id_details , lowest_profit_id_details] , axis = 1)
    return show

# calling the function
calculate_max_min('profit_earned')


# In[90]:


# max budgets and min budgets
calculate_max_min('budget')


# In[91]:


# most and least earned revenue
calculate_max_min('revenue')


# In[92]:


# movies with longest and shortest runtime
calculate_max_min('runtime')


# In[93]:


# calculating the average runtime of the movies
def average_run(column):
    return movie_data[column].mean()

# calling the function
average_run('runtime')


# In[105]:


# analysing the runtime using graphs
# analysis of runtime using bar graph
plt.figure(figsize = (10 , 5) , dpi = 100)
plt.xlabel('runtime')
plt.ylabel('no of movies')
plt.title('runtime of all movies')

movie_data['runtime'].hist(bins = 30)
plt.show()


# In[104]:


# analysis of runtime using boxplot
plt.figure(figsize = (10 , 5) , dpi = 100)
plt.xlabel('runtime')
plt.ylabel('no of movies')
plt.title('runtime of all movies')
plt.boxplot(movie_data['runtime'])
plt.show()


# In[96]:


# using sns(seaborn) to create a swarm plot of runtime
# using .figure() from pyplot to create a custom sized plot
plt.figure(figsize = (10 , 5) , dpi = 100)
sns.swarmplot(movie_data['runtime'] , color = 'green')
plt.show()


# In[97]:


# let's use describe function on runtime values to discover intresting values
movie_data['runtime'].describe()


# In[101]:


# year of release vs profitability
profits_earned_per_year = movie_data.groupby('release_year')['profit_earned'].sum()
plt.figure(figsize = (10 , 5) , dpi = 100)
plt.plot(profits_earned_per_year)
plt.legend()
plt.xlabel('total profits')
plt.ylabel('year of release')
plt.show()


# In[106]:


# to analyze only "most profitable" movies, we will weed out those movies which have a profit less then 40 million
most_profitable_movies = movie_data[movie_data['profit_earned'] >=40000000]
most_profitable_movies.index = range(len(most_profitable_movies))

# previewing the newly indexed data
most_profitable_movies.head(10)


# In[107]:


# average budget of most profitable movies
# we will define another function for calulating the avg. budget
def avg_profit(column):
    return most_profitable_movies[column].mean()

# calling the function
print(avg_profit('profit_earned'))


# In[108]:


# average revenue of most profitable movies
avg_profit('revenue')


# In[109]:


# average budget of most profitable movies
avg_profit('budget')


# In[110]:


# average duration of most profitable movies
avg_profit('runtime')

