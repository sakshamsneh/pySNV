import collections
import getopt
import re
import sys
# from locale import str
from statistics import mean

import numpy as np
import pandas as pd
import tweepy
from yaspin import yaspin

import config as cfg
import func


def getAPI():
    """Returns API created by tweepy"""
    auth = tweepy.OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
    auth.set_access_token(cfg.access_token, cfg.access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def get_tweets(api, listOfTweets, keyword, numOfTweets=20, date_since='2019-1-1', lang="en"):
    """
    Generates datalist of tweets

    Creates a list of dictionary of tweets from passed parameters.

    Params:
    api(tweepy API):    API for twitter access
    listOfTweets(list): List of dict
    numOfTweets(number):Number of tweets to be search for.
    date_since(date):   Starting date of search
    lang(text):         Search language

    Returns:
        list of dict of tweets and details
    """
    spinner = yaspin()
    spinner.start()
    for tweet in tweepy.Cursor(api.search, q=keyword, lang=lang, since=date_since).items(numOfTweets):
        # Add tweets in this format
        dict_ = {'Screen Name': tweet.user.screen_name,
                 'User Name': tweet.user.name,
                 'Tweet Created At': str(tweet.created_at),
                 'Tweet Text': tweet.text,
                 'Cleaned Tweet Text': func.clean_tweets(tweet.text),
                 'User Location': str(tweet.user.location),
                 'Tweet Coordinates': str(tweet.coordinates),
                 'Retweet Count': str(tweet.retweet_count),
                 'Retweeted': str(tweet.retweeted),
                 'Phone Type': str(tweet.source),
                 'Favorite Count': str(tweet.favorite_count),
                 'Favorited': str(tweet.favorited),
                 'Replied': str(tweet.in_reply_to_status_id_str)
                 }
        listOfTweets.append(dict_)
    spinner.stop()
    return listOfTweets


def getDataset(api, dataset, headsize, itemsize):
    """
    Generates dataframe of user hashtags

    Creates a dataframe of hashtags used by all unique users
    in the tweets dataset.

    Params:
    api(tweepy API):    API for twitter access
    dataset(dataframe): List of dict
    headsize(number):   Number of unique users taken.
    itemsize(number):   Number of tweets of each users to be taken.

    Returns:
        dataframe of users and their hashtags
    """
    userlist = dataset['user'].head(headsize).tolist()

    res = []
    [res.append(x) for x in userlist if x not in res]

    data = []
    for x in res:
        val = []
        h = []
        r = 0
        f = 0
        try:
            for tweet in tweepy.Cursor(api.user_timeline, id=x).items(itemsize):
                h.extend(func.extractHashtag(tweet.text))
                t = func.clean_tweets(tweet.text)
                k = func.sentiment_analyzer_scores(t)
                val.append(k)
                r = r + tweet.retweet_count
                f = f + tweet.favorite_count
            hl = []
            [hl.append(x) for x in h if x not in hl]
            data.append([str(x), mean(val), hl, r, f])
        except tweepy.TweepError:  # Caused by inexistance of user x
            pass

    return pd.DataFrame(data, columns=['user', 'sent', 'hashtags', 'rt', 'fav'])
