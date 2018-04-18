#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import tweepy
import json
import logging
from auth import *
from sqlalchemy import exc
from db_engine import Engines

# log settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')

# get arguments
try:
    user = sys.argv[1]
except:
    logging.error('Please specify a user id >>> ./bin/python insert_twuser.py <screen_name>')
    
def insert_tw_user(user=user):

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # get user object
    user = api.get_user(user)

    # user properties 
    id = user.id_str
    screen_name = user.screen_name
    name = user.name
    created_at = user.created_at
    description = user.description
    lang = user.lang
    location = user.location
    time_zone = user.time_zone

    # create engine
    engine = Engines().db_twitter()

    # insert user into db
    try:
        db = engine.connect()

        sql_insert_user = "INSERT INTO user " \
                          "VALUES ('%s', '%s', '%s', '%s','%s', '%s', '%s' ,'%s')" \
                                            %(id, screen_name, name, created_at, description, lang, location, time_zone)
        db.execute(sql_insert_user)
        db.close()

        logging.info('Got it! ' + screen_name + ' is now stored in database')

    except exc.SQLAlchemyError as e:
        if 'Duplicate entry' in str(e):
            logging.warning('An account ' + screen_name + ' is already in database')
        else:
            raise

    
if __name__ == '__main__':
    insert_tw_user()
