
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
import tweepy
import json
import re
import matplotlib.pyplot as plt
import warnings


# In[6]:


# Read in csv file as a Pandas DataFrame
twitter_archive = pd.read_csv('twitter-archive-enhanced.csv')


# In[3]:


# Use requests library to download tsv file from a website
url="https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv"
response = requests.get(url)

with open('image_predictions.tsv', 'wb') as file:
    file.write(response.content)

# Read in tsv file as a Pandas DataFrame    
image_predictions = pd.read_csv('image_predictions.tsv', sep='\t')


# In[9]:


# Personal API keys, secrets, and tokens have been replaced with placeholders
consumer_key = 'fRyyQvnzL0JlNXv7BNSENVqWg'
consumer_secret = 's5eGF18nUGHPQzdYt5vPd7WExfBbq8iP3wwwhcaLgTIZU1LX2j'
access_token = '143318530-tSRUys3Hnr7I7EE24H3ItwbT4ZnRTTKHFF9JaWUQ'
access_secret = '3SmwwnZwR3LJlLtSyGt8WU1yl3KNkK5Y0SDFcjS0f2XQg'


# In[10]:


# Variables created for tweepy query
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)


# In[11]:


# For loop which will add each available tweet to a new line of tweet_json.txt
with open('tweet_json.txt', 'a', encoding='utf8') as f:
    for tweet_id in twitter_archive['tweet_id']:
        try:
            tweet = api.get_status(tweet_id, tweet_mode='extended')
            json.dump(tweet._json, f)
            f.write('\n')
        except:
            continue


# In[12]:


# For loop to append each tweet into a list
tweets_data = []

tweet_file = open('tweet_json.txt', "r")

for line in tweet_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
        
tweet_file.close()


# In[13]:


# Create tweet_info DataFrame
tweet_info = pd.DataFrame()


# In[14]:


# Add selected variables to tweet_info DataFrame
tweet_info['id'] = list(map(lambda tweet: tweet['id'], tweets_data))
tweet_info['retweet_count'] = list(map(lambda tweet: tweet['retweet_count'], tweets_data))
tweet_info['favorite_count'] = list(map(lambda tweet: tweet['favorite_count'], tweets_data))


# # Assess

# In[15]:


# View first 20 rows of twitter_archive DataFrame
twitter_archive.head(20)


# In[16]:


# View info of twitter_archive DataFrame
twitter_archive.info()


# In[17]:


# View descriptive statistics of twitter_archive DataFrame
twitter_archive.describe()


# In[18]:


# View first 5 rows of image_predictions DataFrame
image_predictions.head()


# In[19]:


# View last 5 rows of image_predictions DataFrame
image_predictions.tail()


# In[20]:


# View info of image_predictions DataFrame
image_predictions.info()


# In[21]:


# View descriptive statistics of image_predictions DataFrame
image_predictions.describe()


# In[22]:


# View first 5 rows of tweet_info DataFrame
tweet_info.head()


# In[23]:


# View last 5 rows of tweet_info DataFrame
tweet_info.tail()


# In[24]:


# View info of tweet_info DataFrame
tweet_info.info()


# In[25]:


# View descriptive statistics of tweet_info DataFrame
tweet_info.describe()


# In[26]:


# View rows in twitter_archive which contain '&amp;' instead of '&' in 'text' column
twitter_archive[twitter_archive.text.str.contains('&amp;')]


# In[27]:


# Sort values of 'name' column alphabetically - lowercase values appear at the bottom
twitter_archive.name.sort_values()


# In[28]:


# View number of entries for each source
twitter_archive.source.value_counts()


# In[29]:


# View rows where the value of 'name' is lowercase - indicates that it is not an actual name
twitter_archive.loc[(twitter_archive['name'].str.islower())]


# In[30]:


# View rows where the value of 'name' is lowercase and the word 'named' appears in the 'text' column which indicates 
# there is an actual dog name in the text
twitter_archive.loc[(twitter_archive['name'].str.islower()) & (twitter_archive['text'].str.contains('named'))]


# In[31]:


# View row where dog name is 'O' but we can see in the 'text' column that the dog's name is actually 'O'Malley' 
twitter_archive[twitter_archive.name == "O"]


# In[32]:


#disable warnings
warnings.simplefilter('ignore')


# In[33]:


# View rows where text column contains #.#/# indicating a decimal for the rating numerator, 
# however they do not appear in the 'rating_numerator' column
twitter_archive[twitter_archive.text.str.contains(r"(\d+\.\d*\/\d+)")]


# In[34]:


# View row of specific tweet using tweet_id of a tweet that doesn't have a rating 
twitter_archive[twitter_archive.tweet_id == 810984652412424192]


# # Quality
# Tweets with no images
# 
# Dataset contains retweets
# 
# Contents of 'text' cutoff
# 
# Incorrect dog names
# 
# Missing values in 'name' and dog stages showing as 'None'
# 
# Rating numerators with decimals not showing full float
# 
# Tweet with more than one #/# sometimes have the first occurence erroneously used for the rating numerators and denominators 
# 
# Tweet ID# 810984652412424192 doesn't contain a rating
# 
# Extra characters after '&'
# 
# Sources difficult to read
# 
# Erroneous datatypes (timestamp, source, dog stages, tweet_id, in_reply_to_status_id, in_reply_to_user_id) 
# 
# 

# # #Tidiness
# Dog "stage" variable in four columns: doggo, floofer, pupper, puppo
# 
# Join 'tweet_info' and 'image_predictions' to 'twitter_archive'

# # Cleaning

# In[35]:


# Create copies of original DataFrames to work off of
twitter_archive_clean = twitter_archive.copy()
image_predictions_clean = image_predictions.copy()
tweet_info_clean = tweet_info.copy()


# # define
Create dog stage variable and remove individual dog stage columns.
# # code

# In[36]:


# Create 'dog_stage' variable which is made by extracting the dog stage variables from the text column when available 
twitter_archive_clean['dog_stage'] = twitter_archive_clean['text'].str.extract('(puppo|pupper|floofer|doggo)', expand=True)


# In[37]:


# Create variable of columns that are no longer needed and drop them from the DataFrame 
columns = ['doggo', 'floofer', 'pupper', 'puppo']
twitter_archive_clean = twitter_archive_clean.drop(columns, axis=1)


# # testing

# In[38]:


# testing
twitter_archive_clean.head(20)


# # Define
# Add tweet_info and image_predictions to twitter_archive table.

# # code

# In[39]:


twitter_archive_clean = pd.merge(left=twitter_archive_clean, right=tweet_info_clean, left_on='tweet_id', right_on='id', how='inner')


# In[40]:


twitter_archive_clean = twitter_archive_clean.merge(image_predictions_clean, on='tweet_id', how='inner')


# In[41]:


twitter_archive_clean = twitter_archive_clean.drop('id', axis=1)


# # testing

# In[42]:


# testing
twitter_archive_clean.info()


# # Define
# Remove rows where there are no images (expanded_urls).

# # code

# In[43]:


twitter_archive_clean = twitter_archive_clean.dropna(subset=['expanded_urls'])


# # testing

# In[44]:


# test
sum(twitter_archive_clean['expanded_urls'].isnull())


# # Define
# Remove retweets.

# In[45]:


# Select rows where 'retweeted_status_id' is null to save to twitter_archive_clean
twitter_archive_clean = twitter_archive_clean[twitter_archive_clean['retweeted_status_id'].isnull()]


# In[46]:


twitter_archive_clean.info()


# # Define
# Remove retweeted columns.

# In[47]:


# Update columns variable and drop columns related to retweets
columns = ['retweeted_status_id', 'retweeted_status_user_id', 'retweeted_status_timestamp']
twitter_archive_clean = twitter_archive_clean.drop(columns, axis=1)


# In[48]:


twitter_archive_clean.info()


# # Define
# Display full content of 'text' column.

# # code

# In[49]:


# Set column width to infinite so entire content of 'text' column is displayed
pd.set_option('display.max_colwidth', -1)


# In[50]:


twitter_archive_clean.sample(5)


# # Define
# Change incorrect dog names.

# # code

# In[51]:


# Save locations where 'name' column is lowercase, lowercase and 'text' column contains 'named' and lowercase and 'text'
# column contains the words 'name is'
named_to_replace = twitter_archive_clean.loc[(twitter_archive_clean['name'].str.islower()) & (twitter_archive_clean['text'].str.contains('named'))]
name_is_to_replace = twitter_archive_clean.loc[(twitter_archive_clean['name'].str.islower()) & (twitter_archive_clean['text'].str.contains('name is'))]
not_named_to_replace = twitter_archive_clean.loc[(twitter_archive_clean['name'].str.islower())]

# Save these locations as lists
named_to_replace_list = named_to_replace['text'].tolist()
name_is_to_replace_list = name_is_to_replace['text'].tolist()
not_named_to_replace_list = not_named_to_replace['text'].tolist()

# For loop to iterate through locations where name is lowercase and the words 'named' appear in 'text' and set the 'name' 
# value to be the word that appears after 'named'
for entry in named_to_replace_list:
    mask = twitter_archive_clean.text == entry
    name_column = 'name'
    twitter_archive_clean.loc[mask, name_column] = re.findall(r"named\s(\w+)", entry)

# For loop to iterate through locations where name is lowercase and the words 'name is' appear in 'text' and set the 'name' 
# value to be the word that appears after 'name is'    
for entry in name_is_to_replace_list:
    mask = twitter_archive_clean.text == entry
    name_column = 'name'
    twitter_archive_clean.loc[mask, name_column] = re.findall(r"name is\s(\w+)", entry)    

# For loop to iterate through locations where name is lowercase and replace the name value with the word "None"
for entry in not_named_to_replace_list:
    mask = twitter_archive_clean.text == entry
    name_column = 'name'
    twitter_archive_clean.loc[mask, name_column] = "None"


# In[52]:


# Replace the occurence of "O" with "O'Malley"
twitter_archive_clean.name = twitter_archive_clean.name.replace("O", "O'Malley")


# # testing

# In[53]:


# test
twitter_archive_clean.name.sort_values()


# In[54]:


twitter_archive_clean.loc[(twitter_archive_clean['name'].str.islower())]


# In[55]:


twitter_archive_clean[twitter_archive_clean.name == "O'Malley"]


# # Define
# Change missing values in 'name' from 'None' to NaN (dog stages already covered).

# # code

# In[56]:


twitter_archive_clean['name'] = twitter_archive_clean['name'].replace('None', np.NaN)


# # testing

# In[57]:


# test
twitter_archive_clean.info()


# # Define
# Fix rating numerator and denominators that are not actually ratings.

# # code

# In[58]:


# View all occurences where there are more than one #/# in 'text' column
twitter_archive_clean[twitter_archive_clean.text.str.contains( r"(\d+\.?\d*\/\d+\.?\d*\D+\d+\.?\d*\/\d+\.?\d*)")]


# In[59]:


# Save the text where the rating numerator and denominators were incorrectly extracted
ratings_to_fix = ['After so many requests, this is Bretagne. She was the last surviving 9/11 search dog, and our second ever 14/10. RIP https://t.co/XAVDNDaVgQ', 
 'Happy 4/20 from the squad! 13/10 for all https://t.co/eV1diwds8a', 
 'This is Bluebert. He just saw that both #FinalFur match ups are split 50/50. Amazed af. 11/10 https://t.co/Kky1DPG4iq', 
 'This is Darrel. He just robbed a 7/11 and is in a high speed police chase. Was just spotted by the helicopter 10/10 https://t.co/7EsP8LmSp5',
 'This is an Albanian 3 1/2 legged  Episcopalian. Loves well-polished hardwood flooring. Penis on the collar. 9/10 https://t.co/d9NcXFKwLv']


# In[60]:


# Loop through the list of ratings to fix and extract the second occurence of #/ to save as the rating numerator. As all the
# occurences of the actual ratings in the ratings to fix list have a denominator of 10, we will set that value for each 
#entry instead of extracting it.
for entry in ratings_to_fix:
    mask = twitter_archive_clean.text == entry
    column_name1 = 'rating_numerator'
    column_name2 = 'rating_denominator'
    twitter_archive_clean.loc[mask, column_name1] = re.findall(r"\d+\.?\d*\/\d+\.?\d*\D+(\d+\.?\d*)\/\d+\.?\d*", entry)
    twitter_archive_clean.loc[mask, column_name2] = 10


# # testing

# In[61]:


# test
twitter_archive_clean[twitter_archive_clean.text.isin(ratings_to_fix)]


# # Define
# Fix rating numerator that have decimals.

# # code

# In[62]:


# View tweets with decimals in rating in 'text' column
twitter_archive_clean[twitter_archive_clean.text.str.contains(r"(\d+\.\d*\/\d+)")]


# In[63]:


# Change datatype of rating_numerator and denominator to float
twitter_archive_clean['rating_numerator'] = twitter_archive_clean['rating_numerator'].astype('float')
twitter_archive_clean['rating_denominator'] = twitter_archive_clean['rating_denominator'].astype('float')


# In[64]:


# Set correct numerators for specific tweets
twitter_archive_clean.loc[(twitter_archive_clean['tweet_id'] == 883482846933004288) & (twitter_archive_clean['rating_numerator'] == 5), ['rating_numerator']] = 13.5
twitter_archive_clean.loc[(twitter_archive_clean['tweet_id'] == 786709082849828864) & (twitter_archive_clean['rating_numerator'] == 75), ['rating_numerator']] = 9.75
twitter_archive_clean.loc[(twitter_archive_clean['tweet_id'] == 778027034220126208) & (twitter_archive_clean['rating_numerator'] == 27), ['rating_numerator']] = 11.27
twitter_archive_clean.loc[(twitter_archive_clean['tweet_id'] == 680494726643068929) & (twitter_archive_clean['rating_numerator'] == 26), ['rating_numerator']] = 11.26


# # testing

# In[66]:


# test
twitter_archive_clean[twitter_archive_clean.text.str.contains(r"(\d+\.\d*\/\d+)")]


# # Define
# Remove tweet without rating.

# # code

# In[67]:


twitter_archive_clean = twitter_archive_clean[twitter_archive_clean.tweet_id != 810984652412424192]


# # testing

# In[68]:


# test
twitter_archive_clean[twitter_archive_clean.tweet_id == 810984652412424192]


# # Define
# Remove extra characters after '&' in twitter_archive_clean['text'].

# # code

# In[69]:


twitter_archive_clean['text'] = twitter_archive_clean['text'].str.replace('&amp;', '&')


# # testing

# In[70]:


# test
twitter_archive_clean[twitter_archive_clean.text.str.contains('&amp;')]


# # Define
# Change sources to more readable categories

# # code

# In[71]:


# Remove url from sources
twitter_archive_clean['source'] = twitter_archive_clean['source'].str.replace('<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', 'Twitter for iPhone')
twitter_archive_clean['source'] = twitter_archive_clean['source'].str.replace('<a href="http://vine.co" rel="nofollow">Vine - Make a Scene</a>', 'Vine')
twitter_archive_clean['source'] = twitter_archive_clean['source'].str.replace('<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>', 'Twitter Web Client')
twitter_archive_clean['source'] = twitter_archive_clean['source'].str.replace('<a href="https://about.twitter.com/products/tweetdeck" rel="nofollow">TweetDeck</a>', 'TweetDeck')


# In[72]:


# Change datatype to category
twitter_archive_clean['source'] = twitter_archive_clean['source'].astype('category')


# # testing

# In[73]:


# test
twitter_archive_clean.source.value_counts()


# In[74]:


twitter_archive_clean.info()


# # Define
# Change datatypes of timestamp to datetime, dog_stage to categorical, and tweet_id, in_reply_to_status_id, and in_reply_to_user_id to strings.

# # code

# In[75]:


twitter_archive_clean['dog_stage'] = twitter_archive_clean['dog_stage'].astype('category')
twitter_archive_clean['timestamp'] = pd.to_datetime(twitter_archive_clean['timestamp'])
twitter_archive_clean['tweet_id'] = twitter_archive_clean['tweet_id'].astype('str')
twitter_archive_clean['in_reply_to_status_id'] = twitter_archive_clean['in_reply_to_status_id'].astype('str')
twitter_archive_clean['in_reply_to_user_id'] = twitter_archive_clean['in_reply_to_user_id'].astype('str')


# # testing

# In[76]:


# test
twitter_archive_clean.info()


# In[77]:


# Save clean DataFrame to csv file
twitter_archive_clean.to_csv('twitter_archive_master.csv')


# # Analyze

# In[78]:


# Create copy of twitter_archive_clean to work off of using only my variables of interest
time_df = twitter_archive_clean[['timestamp', 'retweet_count', 'favorite_count', 'rating_numerator', 'rating_denominator']].copy()


# In[79]:


# Set the index to be the timestamp so time is displayed properly in plots
time_df.set_index('timestamp', inplace=True)


# In[80]:


# Create rating_ration variable by dividing the rating numerator by the deonominator to normalize scores which are not 
# out of 10
time_df['rating_ratio'] = time_df['rating_numerator']/time_df['rating_denominator']


# In[87]:


# plotting
plt.figure(figsize = (10 , 10))
time_df['retweet_count'].plot(color = 'red', label='Retweets')
time_df['favorite_count'].plot(color = 'blue', label='Favorites')
plt.style.use('seaborn-darkgrid')
plt.legend(loc='upper left')
plt.xlabel('Tweet timestamp')
plt.ylabel('Count')
plt.title('Retweets and favorites over time')
plt.savefig('retweets_favorites.png')
plt.show()


# In[84]:


# plotting
plt.figure(figsize = (10 , 10))
time_df['rating_ratio'].plot()
plt.style.use('seaborn-darkgrid')
plt.xlabel('Time')
plt.ylabel('Ratio')
plt.title('Rating ratio over time')
plt.savefig('ratio.png')
plt.show()


# In[86]:


# Limit y axis to zoom in on data and ignore outliers
plt.figure(figsize = (10 , 10))
time_df['rating_ratio'].plot()
plt.ylim(-1, 3)
plt.style.use('seaborn-darkgrid')
plt.xlabel('Time')
plt.ylabel('Ratio')
plt.title('Rating ratio over time')
plt.savefig('ratio_zoom.png')
plt.show()

