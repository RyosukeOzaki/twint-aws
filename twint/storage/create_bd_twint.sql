-- drop schema twitter;
create schema twitter;
use twitter;

CREATE TABLE users(
                    id bigint(30) not null,
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
                    time_update bigint(30) not null,
                    CONSTRAINT users_pk PRIMARY KEY (id, hex_dig(150))
                ) DEFAULT CHARSET=utf8mb4;


CREATE TABLE tweets (
                    id bigint(30) not null,
                    id_str text not null,
                    tweet text,
                    conversation_id text not null,
                    created_at bigint(30) not null,
                    date text not null,
                    time text not null,
                    timezone text not null,
                    place text,
                    replies_count integer,
                    likes_count integer,
                    retweets_count integer,
                    user_id bigint(30) not null,
                    user_id_str text not null,
                    screen_name text not null,
                    name text,
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
                    time_update bigint(30) not null,
                    `translate` text,
                    trans_src text,
                    trans_dest text,
                    PRIMARY KEY (id)
                ) DEFAULT CHARSET=utf8mb4;

CREATE TABLE retweets(
                    user_id bigint(30) not null,
                    username text not null,
                    tweet_id bigint(30) not null,
                    retweet_id bigint(30) not null,
                    retweet_date bigint(30) not null,
                    CONSTRAINT retweets_pk PRIMARY KEY(user_id, tweet_id),
                    CONSTRAINT retweets_user_id_fk FOREIGN KEY(user_id) REFERENCES users(id),
                    CONSTRAINT retweets_tweet_id_fk FOREIGN KEY(tweet_id) REFERENCES tweets(id)
                ) DEFAULT CHARSET=utf8mb4;
CREATE TABLE replies(
                    tweet_id bigint(30) not null,
                    user_id bigint(30) not null,
                    username text not null,
                    CONSTRAINT replies_pk PRIMARY KEY (user_id, tweet_id),
                    CONSTRAINT replies_tweet_id_fk FOREIGN KEY (tweet_id) REFERENCES tweets(id)
                ) DEFAULT CHARSET=utf8mb4;
CREATE TABLE favorites(
                    user_id bigint(30) not null,
                    tweet_id bigint(30) not null,
                    CONSTRAINT favorites_pk PRIMARY KEY (user_id, tweet_id),
                    CONSTRAINT favories_user_id_fk FOREIGN KEY (user_id) REFERENCES users(id),
                    CONSTRAINT favories_tweet_id_fk FOREIGN KEY (tweet_id) REFERENCES tweets(id)
                ) DEFAULT CHARSET=utf8mb4;
CREATE TABLE followers (
                    id bigint(30) not null,
                    follower_id bigint(30) not null,
                    CONSTRAINT followers_pk PRIMARY KEY (id, follower_id),
                    CONSTRAINT followers_id_fk FOREIGN KEY(id) REFERENCES users(id),
                    CONSTRAINT followers_follower_id_fk FOREIGN KEY(follower_id) REFERENCES users(id)
                ) DEFAULT CHARSET=utf8mb4;
CREATE TABLE following (
                    id bigint(30) not null,
                    following_id bigint(30) not null,
                    CONSTRAINT following_pk PRIMARY KEY (id, following_id),
                    CONSTRAINT following_id_fk FOREIGN KEY(id) REFERENCES users(id),
                    CONSTRAINT following_following_id_fk FOREIGN KEY(following_id) REFERENCES users(id)
                ) DEFAULT CHARSET=utf8mb4;
CREATE TABLE followers_names (
                    user text not null,
                    time_update integer not null,
                    follower text not null,
                    PRIMARY KEY (user(150), follower(150))
                ) DEFAULT CHARSET=utf8mb4;
CREATE TABLE following_names (
                    user text not null,
                    time_update integer not null,
                    follows text not null,
                    PRIMARY KEY (user(150), follows(150))
                ) DEFAULT CHARSET=utf8mb4;