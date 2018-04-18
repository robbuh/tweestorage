#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import tweepy

import datetime
import logging
import os
import sys

from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

from db_engine import Engines
from tweet_dumper import get_all_tweet

# import twitter keys and tokens
from auth import *


# log settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')

# get arguments
try:
    ff = sys.argv[1]
except:
    ff = False

Base = declarative_base()


class TweetTable(Base):
    __tablename__ = 'tweet'
    id_user = Column(String)
    id_tweet = Column(String, primary_key=True)
    text = Column(String)
    created_at = Column(Date)
    favorite_count = Column(Integer)
    lan = Column(String)


class FolloweesTable(Base):
    __tablename__ = 'user_ff'
    id = Column(String, primary_key=True)
    tw_user_id = Column(String)
    type = Column(String)
    name = Column(String)
    screen_name = Column(String)
    created_at = Column(String)
    description = Column(String)
    lang = Column(String)
    location = Column(String)
    time_zone = Column(String)


def db_storage(ff=ff):

    # create engine
    engine = Engines().db_twitter()
    
    # create session for bulk action
    Session = sessionmaker(bind=engine)
    s = Session()

    # db connection
    try:
        db = engine.connect()
    except exc.SQLAlchemyError:
        raise

    # get users you want to check 
    sql_users = "SELECT id FROM user"
    tw_users = db.execute(sql_users).fetchall()
    tw_users = [int(x[0]) for x in tw_users]


    # get all user's followers and followees 
    sql_ff = "SELECT id FROM user_ff"
    ff_users = db.execute(sql_ff).fetchall()
    ff_users = [int(x[0]) for x in ff_users]

    if len(tw_users + ff_users) == 0:
        logging.error('No users in database. Please insert at least one user >>> ./bin/python insert_twuser.py <screen_name>')
    

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)


    # get list of users and users' followers and followees (if option "ff" is True)
    for tw in tw_users:
        try:
            
            # users
            users = []
            users.append(tw)

            if (ff):
                # get followers and followees
                user = api.get_user(tw)

                # get max 200 followers and 200 followes
                followers = user.followers(count=200).ids()
                followees = user.friends(count=200).ids()
    
                # ddd followers and followees in users list
                users.extend(followers)
                users.extend(followees) 

            # make users list unique
            users = list(set(users))

            for user in users:

                # add users in user_ff table
                # ---------------------------------------------------------------

                # check if user allready exist in "user" or "user_ff" db table
                if int(user) not in tw_users + ff_users:
                    user_ff = api.get_user(user)  
    
                    id_string = user_ff.id_str

                    if int(id_string) in followers:
                        type='follower' 
                    elif int(id_string) in followees:
                        type='followee'

                    name = user_ff.name
                    screen_name = user_ff.screen_name
                    created_at = user_ff.created_at
                    description = user_ff.description
                    lang = user_ff.lang
                    location = user_ff.location
                    time_zone = user_ff.time_zone
    
                    try:
                        # list of users for bulk action       
                        followees_users_objects = [FolloweesTable(
                                                        id=id_string,
                                                        tw_user_id=tw,
                                                        type=type,
                                                        name=name,
                                                        screen_name=screen_name, 
                                                        created_at=created_at,
                                                        description=description,
                                                        lang=lang,
                                                        location=location,
                                                        time_zone=time_zone)]
                                    
                        # insert records in database
                        s.bulk_save_objects(followees_users_objects)
                        s.commit()
                    except Exception as ex:
                        logging.error(ex)
                        s.rollback()
                        continue
    
    
    
                # add tweet in database
                # ---------------------------------------------------------------
                user_id = user
        
                # select last inserted tweet in DB
                #  -- "created_at" condition to avoid id_tweet duplicate key error 
                sql_last_tweet = """SELECT MAX(id_tweet) FROM tweet
                                    WHERE id_user = '%s' 
                                    AND created_at = (SELECT MAX(created_at) FROM tweet WHERE id_user = '%s')""" %(user_id, user_id)
        
                since_id = db.execute(sql_last_tweet).fetchone()

                # get user's tweet
                tweet = get_all_tweet(user_id, since_id[0])
                
                try:
                    # list of tweet for bulk action       
                    if tweet:
                        objects = [TweetTable(
                                        id_user=x['user_id_str'],
                                        id_tweet=x['id_str'],
                                        text=x['text'],
                                        created_at=x['created_at'],
                                        favorite_count=x['favorite_count'],
                                        lan=x['lang']) for x in tweet]
                        
                        # insert records in database
                        s.bulk_save_objects(objects)
                        s.commit()
                except Exception as ex:
                    logging.error(ex)
                    s.rollback()
                    continue

                # Refresh connection and delete cached data
                db.invalidate()
        
        except tweepy.TweepError, error:
            num = 15
            logging.warning('On hold, restart within '+str(num)+' minutes...')
            time.sleep(60*num)
            continue
        except StopIteration:
            break

    s.close()
    db.close()


if __name__ == '__main__':
    db_storage()
