import requests
import os
import json
import pandas as pd
import pickle
import time
import string
import root_scraper as rs

UNFILTERED_TWEETS_PER_TOPIC = 990

def extract_timeframe(url):
    since_idx = url.find("since") + 8
    until_idx = url.find("until") + 8
    since = url[since_idx:since_idx+19]
    until = url[until_idx:until_idx+19]
    since = '{}Z'.format(since.replace('_', 'T'))
    until = '{}Z'.format(until.replace('_', 'T'))
    return since, until


if __name__=='__main__':
    with open("small_input.csv") as f:
        input_lines = f.readlines()
        input_lines = input_lines[1:]
    # print(input_lines[0])
    topic_list = []
    for line in input_lines:
        fields = line.split(',')
        # print(fields)
        name = fields[0].strip()
        url = fields[1].strip()
        label = int(fields[2].strip())
        since, until = extract_timeframe(url)
        topic_list.append(tuple([name, label, since, until]))
    topic_df = pd.DataFrame(topic_list, columns=['name', 'label', 'since', 'until'])
    # print(topic_df.head())
    topic_df.to_csv('topic_list.csv', sep=',', header=True, index=False)

    
    if not os.path.exists('topic_root/csv'):
        os.makedirs('topic_root/csv')
    if not os.path.exists('topic_root/pkl'):
        os.makedirs('topic_root/pkl')   
    counts = []
    full_df = rs.to_df([])
    for idx, topic in topic_df.iterrows():
        topic_tweets = rs.scrape_for_topic(topic['name'], topic['label'], UNFILTERED_TWEETS_PER_TOPIC, endtime=topic['until'])
        counts.append(len(topic_tweets))
        df = rs.to_df(topic_tweets)
        temp = topic['name'].replace(' ', '_')
        temp = temp.replace('%23', '')
        fpkl = f'topic_root/pkl/{temp}.pkl'
        fcsv = f'topic_root/csv/{temp}.csv'
        df.to_pickle(fpkl)
        df.to_csv(fcsv, sep=',', header=True, index=False)
        full_df = full_df.append(df)
    # print(counts)
    
    topic_df['count'] = counts
    topic_df.to_csv('topic_list.csv', sep=',', header=True, index=False)
    full_df.to_csv('compiled_tweets.csv', sep=',', header=True, index=False)
    full_df.to_pickle('compiled_tweets.pkl')