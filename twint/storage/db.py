
import pymysql
import hashlib
import json
import logging
import sqlite3
import sys
import time
import typing
from datetime import datetime

LOGGER = logging.getLogger(__name__)


def Conn(config):
    if config.Database:
        print("[+] Inserting into Database mysql: " + str(config.Database))
        conn = init(config.Database, config.Batch, config.YYYYMMDD)
        #if isinstance(conn, str):
        #    print(str)
        #    sys.exit(1)
    else:
        conn = ""

    return conn

def init(db, batch, YYYYMMDD):
    conn = pymysql.connect(host="xxx.xxx.xxx.xxx",user="root",password="xxxx",db=db)
    cursor = conn.cursor()
    if batch:
        table_tweets_batch = f"""
                CREATE TABLE IF NOT EXISTS
                    tweets_disney_{YYYYMMDD}(
                        id integer not null,
                        id_str text not null,
                        tweet text default '',
                        conversation_id text not null,
                        created_at integer not null,
                        date text not null,
                        time text not null,
                        timezone text not null,
                        place text default '',
                        replies_count integer,
                        likes_count integer,
                        retweets_count integer,
                        user_id integer not null,
                        user_id_str text not null,
                        screen_name text not null,
                        name text default '',
                        link text,
                        mentions text,
                        hashtags text,
                        cashtags text,
                        urls text,
                        photos text,
                        quote_url text,
                        video integer,
                        geo text,
                        near text,
                        source text,
                        time_update integer not null,
                        `translate` text default '',
                        trans_src text default '',
                        trans_dest text default '',
                        PRIMARY KEY (id)
                    );
            """
        cursor.execute(table_tweets_batch)
    try:
        table_users = """
            CREATE TABLE IF NOT EXISTS
                users(
                    id integer not null,
                    id_str text not null,
                    name text,
                    username text not null,
                    bio text,
                    location text,
                    url text,
                    join_date text not null,
                    join_time text not null,
                    tweets integer,
                    following integer,
                    followers integer,
                    likes integer,
                    media integer,
                    private integer not null,
                    verified integer not null,
                    profile_image_url text not null,
                    background_image text,
                    hex_dig  text not null,
                    time_update integer not null,
                    CONSTRAINT users_pk PRIMARY KEY (id, hex_dig)
                );
            """
        cursor.execute(table_users)

        table_tweets = """
            CREATE TABLE IF NOT EXISTS
                tweets(
                    id integer not null,
                    id_str text not null,
                    tweet text default '',
                    conversation_id text not null,
                    created_at integer not null,
                    date text not null,
                    time text not null,
                    timezone text not null,
                    place text default '',
                    replies_count integer,
                    likes_count integer,
                    retweets_count integer,
                    user_id integer not null,
                    user_id_str text not null,
                    screen_name text not null,
                    name text default '',
                    link text,
                    mentions text,
                    hashtags text,
                    cashtags text,
                    urls text,
                    photos text,
                    quote_url text,
                    video integer,
                    geo text,
                    near text,
                    source text,
                    time_update integer not null,
                    `translate` text default '',
                    trans_src text default '',
                    trans_dest text default '',
                    PRIMARY KEY (id)
                );
        """
        cursor.execute(table_tweets)

        table_retweets = """
            CREATE TABLE IF NOT EXISTS
                retweets(
                    user_id integer not null,
                    username text not null,
                    tweet_id integer not null,
                    retweet_id integer not null,
                    retweet_date integer not null,
                    CONSTRAINT retweets_pk PRIMARY KEY(user_id, tweet_id),
                    CONSTRAINT user_id_fk FOREIGN KEY(user_id) REFERENCES users(id),
                    CONSTRAINT tweet_id_fk FOREIGN KEY(tweet_id) REFERENCES tweets(id)
                );
        """
        cursor.execute(table_retweets)

        table_reply_to = """
            CREATE TABLE IF NOT EXISTS
                replies(
                    tweet_id integer not null,
                    user_id integer not null,
                    username text not null,
                    CONSTRAINT replies_pk PRIMARY KEY (user_id, tweet_id),
                    CONSTRAINT tweet_id_fk FOREIGN KEY (tweet_id) REFERENCES tweets(id)
                );
        """
        cursor.execute(table_reply_to)

        table_favorites =  """
            CREATE TABLE IF NOT EXISTS
                favorites(
                    user_id integer not null,
                    tweet_id integer not null,
                    CONSTRAINT favorites_pk PRIMARY KEY (user_id, tweet_id),
                    CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users(id),
                    CONSTRAINT tweet_id_fk FOREIGN KEY (tweet_id) REFERENCES tweets(id)
                );
        """
        cursor.execute(table_favorites)

        table_followers = """
            CREATE TABLE IF NOT EXISTS
                followers (
                    id integer not null,
                    follower_id integer not null,
                    CONSTRAINT followers_pk PRIMARY KEY (id, follower_id),
                    CONSTRAINT id_fk FOREIGN KEY(id) REFERENCES users(id),
                    CONSTRAINT follower_id_fk FOREIGN KEY(follower_id) REFERENCES users(id)
                );
        """
        cursor.execute(table_followers)

        table_following = """
            CREATE TABLE IF NOT EXISTS
                following (
                    id integer not null,
                    following_id integer not null,
                    CONSTRAINT following_pk PRIMARY KEY (id, following_id),
                    CONSTRAINT id_fk FOREIGN KEY(id) REFERENCES users(id),
                    CONSTRAINT following_id_fk FOREIGN KEY(following_id) REFERENCES users(id)
                );
        """
        cursor.execute(table_following)

        table_followers_names = """
            CREATE TABLE IF NOT EXISTS
                followers_names (
                    user text not null,
                    time_update integer not null,
                    follower text not null,
                    PRIMARY KEY (user, follower)
                );
        """
        cursor.execute(table_followers_names)

        table_following_names = """
            CREATE TABLE IF NOT EXISTS
                following_names (
                    user text not null,
                    time_update integer not null,
                    follows text not null,
                    PRIMARY KEY (user, follows)
                );
        """
        cursor.execute(table_following_names)
        return conn
    except Exception as e:
        return str(e)

def fTable(Followers):
    if Followers:
        table = "followers_names"
    else:
        table = "following_names"
    return table

def uTable(Followers):
    if Followers:
        table = "followers"
    else:
        table = "following"
    return table

def follow(conn, Username, Followers, User):
    try:
        time_ms = round(time.time()*1000)
        cursor = conn.cursor()
        entry = (User, time_ms, Username,)
        table = fTable(Followers)
        query = f"INSERT INTO {table} VALUES((%s),(%s),(%s))"
        cursor.execute(query, entry)
        conn.commit()
    except pymysql.IntegrityError:
        pass

def get_hash_id(conn, id):
    cursor = conn.cursor()
    cursor.execute('SELECT hex_dig FROM users WHERE id = (%s) LIMIT 1', (id,))
    resultset = cursor.fetchall()
    return resultset[0][0] if resultset else -1

def user(conn, config, User):
    try:
        time_ms = round(time.time()*1000)
        cursor = conn.cursor()
        user = [int(User.id), User.id, User.name, User.username, User.bio, User.location, User.url,User.join_date, User.join_time, User.tweets, User.following, User.followers, User.likes, User.media_count, User.is_private, User.is_verified, User.avatar, User.background_image]

        hex_dig = hashlib.sha256(','.join(str(v) for v in user).encode()).hexdigest()
        entry = tuple(user) + (hex_dig,time_ms,)
        old_hash = get_hash_id(conn, User.id)

        if old_hash == -1 or old_hash != hex_dig:
            query = f"INSERT INTO users VALUES((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))"
            cursor.execute(query, entry)
        else:
            pass

        if config.Followers or config.Following:
            table = uTable(config.Followers)
            query = f"INSERT INTO {table} VALUES((%s),(%s))"
            cursor.execute(query, (config.User_id, int(User.id)))

        conn.commit()
    except pymysql.IntegrityError:
        pass

def tweets_table(batch, YYYYMMDD):
    if batch:
        table = f"tweets_disney_{YYYYMMDD}"
    else:
        table = "tweets"
    return table
    
def tweets(conn, Tweet, config):
    try:
        time_ms = round(time.time()*1000)
        cursor = conn.cursor()
        try:
            mentions = ",".join(Tweet.mentions)
        except TypeError as err:
            LOGGER.exception(err)
            mentions = json.dumps(Tweet.mentions)
        try:
            place = ",".join(Tweet.place)
        except TypeError as err:
            LOGGER.exception(err)
            place = json.dumps(Tweet.place)
        entry = (Tweet.id,
                    Tweet.id_str,
                    Tweet.tweet,
                    Tweet.conversation_id,
                    Tweet.datetime,
                    Tweet.datestamp,
                    Tweet.timestamp,
                    Tweet.timezone,
                    place,
                    Tweet.replies_count,
                    Tweet.likes_count,
                    Tweet.retweets_count,
                    Tweet.user_id,
                    Tweet.user_id_str,
                    Tweet.username,
                    Tweet.name,
                    Tweet.link,
                    mentions,
                    ",".join(Tweet.hashtags),
                    ",".join(Tweet.cashtags),
                    ",".join(Tweet.urls),
                    ",".join(Tweet.photos),
                    Tweet.quote_url,
                    Tweet.video,
                    Tweet.geo,
                    Tweet.near,
                    Tweet.source,
                    time_ms,
                    Tweet.translate,
                    Tweet.trans_src,
                    Tweet.trans_dest)
        table = tweets_table(config.Batch, config.YYYYMMDD)
        cursor.execute(f'INSERT INTO {table} VALUES((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))', entry)


        if config.Favorites:
            query = 'INSERT INTO favorites VALUES((%s),(%s))'
            cursor.execute(query, (config.User_id, Tweet.id))

        if Tweet.retweet:
            query = 'INSERT INTO retweets VALUES((%s),(%s),(%s),(%s),(%s))'

            def get_datetime(inp):
                return datetime.timestamp(datetime.strptime(inp, "%Y-%m-%d %H:%M:%S"))

            try:
                _d = get_datetime(Tweet.retweet_date)
            except ValueError as err:
                if Tweet.retweet_date.endswith(' WITA'):
                    LOGGER.exception(err)
                    _d = get_datetime(Tweet.retweet_date.rsplit(' WITA', 1)[0])
                else:
                    raise err
            cursor.execute(query, (int(Tweet.user_rt_id), Tweet.user_rt, Tweet.id, int(Tweet.retweet_id), _d))

        if Tweet.reply_to:
            for reply in Tweet.reply_to:
                query = 'INSERT INTO replies VALUES((%s),(%s),(%s))'

                def get_value(dict_inp: typing.Dict[str, typing.Any], key: str, default_value: typing.Any):
                    """get value from key with default_value.
                    .. note::
                        
                        it may be better to replace this with default :py:class:`dict.get`
                    """
                    try:
                        return dict_inp[key]
                    except KeyError as err:
                        if key not in dict_inp:
                            LOGGER.exception(err)
                            return default_value
                        else:
                            raise err

                reply_user_id = int(get_value(reply, 'user_id', 0))
                reply_username = get_value(reply, 'username', '')
                cursor.execute(query, (Tweet.id, reply_user_id, reply_username))

        conn.commit()
    except pymysql.IntegrityError:
        pass
