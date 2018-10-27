Tweet storage
=============

An example code to store tweet and retweet in MySQL database.  Users are stored in database. 
It is also possible to store users' followers and followees (max 200 accounts per user).


Contents
-------------

| File name   | Description     |  
| --------|---------|
| auth.py  | Twitter API access keys |
| db_engine.py | Db engine to mysql database |
| insert_twuser.py | Add Twitter user in database |
|db_storage.py | Store users' tweet in database |
|tweet_dumper.py| Download tweet (max 200 tweet each time) - Based on yanofsky `tweet_dumper.py` <https://gist.github.com/yanofsky/5436496> |
|twitter.sql| Database example|

Prerequisites
-------------

- Python 2.7
- Python Virtualenv
- MySQL Server
- MySQL client
- Git

_

    $ sudo apt-get install python-setuptools python-virtualenv python-dev build-essential
    $ sudo apt-get install mysql-server
    $ sudo apt-get install libmysqlclient-dev 
    $ sudo apt-get install git


Installation
-------------

    $ git clone git@github.com:robbuh/tweestorage.git

    $ ./bootstrap.sh


Configuration
-----------------

Import database structure in MySQL database

    $ mysql -u <username> -p <databasename> < twitter.sql

Set database connection

    $ nano db_engine.py

```py
return sqlalchemy.create_engine('mysql://username:password@127.0.0.1/db_name?charset=utf8mb4')
 ```

Set twitter API access keys

    $ nano auth.py

```py
consumer_key = "consumer_key"
consumer_secret = "consumer_secret"
access_token = "access_tokenn"
access_token_secret = "access_token_secret"
```

Run script / Usage example
------------------
Add one or more Twitter user in database (one at a time)

    $ ./bin/python insert_twuser.py <screen_name>

Start to store users' tweet in database ("*ff*" option to add followers and fellowees' tweet)

    $ ./bin/python db_storage.py 
    
    # add "ff" if you want also add users' followers and fellowees' and their tweet 
    $ ./bin/python db_storage.py ff

Note: add command to your crontab to schedule new tweet storing
 
 
    
That's it! 
--------------
Check data in your database

| Database table name    | Description    |  
| --------|---------|
| users  | Twitter accounts/users |
| user_ff | Main users' followers & followees (see table users)  |
| tweet | Users, followers and followees' tweet |
