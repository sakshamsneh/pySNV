import datetime

import networkx as nx
import pandas as pd
from yaspin import yaspin

import func
import tweepyFunc


def main():
    """Main function, works from command line"""
    api = tweepyFunc.getAPI()

    listOfTweets = []
    tag = ''
    count = 200
    date_since = '2019-1-1'

    tag = input("INPUT TAG:\t")
    count = int(input("INPUT COUNT:\t"))
    date_since = input("INPUT DATE:\t")
    print("DETAILS:\tTAG:\t"+tag+"\tCOUNT:\t" +
          str(count)+"\tDATE_SINCE:\t"+date_since)

    listOfTweets = tweepyFunc.get_tweets(
        api, listOfTweets, tag, count, date_since)
    dataset = pd.DataFrame(listOfTweets)
    # dataset.to_csv('data/'+tag+'Tweets.csv')

    spinner = yaspin().white.bold.shark.on_blue
    spinner.start()

    data = dataset[['Cleaned Tweet Text', 'Retweet Count',
                    'Screen Name', 'Tweet Created At']].copy()
    data.columns = ['tweet', 'rtc', 'user', 'datetime']
    # data.to_csv('data/simpleDB.csv')

    df = tweepyFunc.getDataset(api, data, 500, 20)
    # df.to_csv('data/hashTweets.csv')

    df = df.sample(n=df.shape[0], replace=True)
    stoptag = ['endgame', 'marvel', 'avengers',
               'exclusive', 'giveaway', 'fun', 'funko', 'pop', 'Gi', 'E', 'G', '1', '2', '3', '', 'c', 'ff', 't', 'th', 'rt', 'repost', 'pl', 'po', 'p', 'mcu', 'maga', 'm', 'in', 'infinitywar', 'give', 'givea', 'giveawa']
    edgelist = func.edgeGen(df, stoptag)
    data = pd.DataFrame(edgelist, columns=['u1', 'u2', 'w'])
    # data.to_csv('data/edgelist1.csv')

    G = func.createGraph(data)
    nx.write_gexf(G, "output/test.gexf")
    spinner.stop()
    print("OUTPUT SAVED!")


if __name__ == "__main__":
    main()
