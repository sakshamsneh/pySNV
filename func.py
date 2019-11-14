import re

import networkx as nx
import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# hashtag search re string
hashtag_re = re.compile("(?:^|\s)[＃#]{1}(\w+)", re.UNICODE)
analyser = SentimentIntensityAnalyzer()


def remove_pattern(input_txt, pattern):
    """Returns re search pattern on input_txt"""
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt


def clean_tweets(lst):
    """Returns cleaned text on re patterns"""
    lst = np.vectorize(remove_pattern)(lst, r"RT @[\w]*:")
    lst = np.vectorize(remove_pattern)(lst, r"@[\w]*")
    lst = np.vectorize(remove_pattern)(lst, "https?://[A-Za-z0-9./]*")
    lst = np.core.defchararray.replace(lst, "[^a-zA-Z#]", " ")
    return lst


def extractHashtag(input_txt):
    """Returns list of hashtags found"""
    r = re.findall(hashtag_re, input_txt)
    hashlist = [i for i in r]
    return hashlist


def sentiment_analyzer_scores(txt):
    """Returns compound sentiment scores"""
    score = analyser.polarity_scores(str(txt))
    lb = score['compound']
    return lb


def list_contains(List1, List2, stoptag):
    """Returns number of common elements in input lists, removing stoptags"""
    set1 = set([x.lower() for x in List1])
    set2 = set([x.lower() for x in List2])
    return len(set2.intersection(set1).difference(set(stoptag)))


def edgeGen(dataset, stoptag):
    """
    Generates edge list

    If same hashtags found between two users,
    adds them to edge list. Uses stoptags for clean results.

    Params:
    dataset(dataframe): Input dataframe
    stoptags(list):     List of stoptags to be removed from hashes

    Returns:
        generated edgelist from dataset
    """
    k = dataset.shape[0]
    edgelist = []
    for index, row in dataset.iterrows():
        w = row['hashtags']
        u = row['user']
        for index2, row2 in dataset.tail(k-(index+1)).iterrows():
            w2 = row2['hashtags']
            u2 = row2['user']
            check = list_contains(w, w2, stoptag)
            if(check != 0):
                edgelist.append([u, u2, check])
    return edgelist


def createGraph(dataset):
    """Returns NetworkX graph generated from input dataframe"""
    G = nx.Graph()
    u1 = dataset["u1"].tolist()
    u2 = dataset["u2"].tolist()
    w = dataset["w"].tolist()
    for index, row in dataset.iterrows():
        G.add_edge(row['u1'], row['u2'], weight=row['w'])
    return G
