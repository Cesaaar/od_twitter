
# coding: utf-8

# In[18]:

# https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/

# Libreria teewpy

import os
import tweepy
import sys
from tweepy.streaming import StreamListener
from tweepy import Stream

config = {} 
config_path = os.path.join(os.path.abspath('..')) 
config_name = r'config.py' 
config_file = os.path.join(config_path,config_name) 
exec(open(config_file).read(),config)


# Key and Secret
consumer_key=config['TWITTER_KEY']
consumer_secret=config['TWITTER_SECRET']
access_token=config['TOKEN']
access_token_secret=config['TOKEN_SECRET']

#HashTag to Check
hashtag = 'trump'


# In[9]:

# Authentication

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# In[10]:

# Data Extraction - Stream
# https://dev.twitter.com/streaming/overview

class MyListener(StreamListener):
    
    tweet_number=0   # class variable
    
    def __init__(self,max_tweets):
        self.max_tweets=max_tweets # max number of tweets
 
    def on_data(self, data):
        self.tweet_number+=1 
        try:
            with open(hashtag+'.json', 'a') as f:
                f.write(data)
        except BaseException as e:
            print('Error on_data: %s' % str(e))
            
        if self.tweet_number>=self.max_tweets:
            sys.exit('Limit of '+str(self.max_tweets)+' tweets reached.')
 
    def on_error(self, status):
        print(status)
        return True


# In[19]:

# Read Stream of tweets based on HashTag
twitter_stream = Stream(auth, MyListener(10000))
twitter_stream.filter(track=['#'+hashtag],languages=['en'])

