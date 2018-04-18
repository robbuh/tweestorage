import sqlalchemy
import codecs

class Engines(object):
    """ Database engines list """

    # make python understand 'utf8mb4' as an alias for 'utf8'
    codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)

    def db_twitter(self):
        return sqlalchemy.create_engine('mysql://username:password@127.0.0.1/db_name?charset=utf8mb4')
