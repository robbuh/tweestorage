#!/usr/bin/python
# -*- coding: utf-8 -*-

# Based on yanofsky tweet_dumper.py https://gist.github.com/yanofsky/5436496

import tweepy
import datetime
import logging
import os

# import twitter keys and tokens
from auth import *

# log settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')

def get_all_tweet(user_id, since_id):
  
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    user = api.get_user(user_id)                                                           
    screen_name = user.screen_name

    # initialize a list to hold all the tweepy tweet
    alltweet = []	
  
    try:
        # make initial request for most recent tweet (200 is the maximum allowed count)
        new_tweet = api.user_timeline(user_id=user_id, since_id=since_id, include_rts=True, count=200)
    
        if new_tweet:
        
            # save most recent tweet
            alltweet.extend(new_tweet)

            logging.info('-- ' + screen_name + ' -- total tweet retrieved: '+str(len(alltweet)))

            # transform the tweepy tweet into a list
            outtweet = [{'user_id_str': tweet.user.id_str, 
                          'screen_name': tweet.user.screen_name,
                          'id_str': tweet.id_str, 
                          'text': tweet.text, 
                          'created_at': str(tweet.created_at).split()[0], 
                          'favorite_count': tweet.favorite_count, 
                          'lang': tweet.lang} for tweet in alltweet]
        
            return outtweet
    
        # return None if there are no tweet 
        logging.info("No tweet for user -- " + screen_name + " -- at the moment")
        return 

    except Exception as ex:
        logging.warning('-- ' + screen_name + ' -- ' + str(ex))

        if str(ex) == 'Not authorized.':
            pass
        else:
            raise

    


