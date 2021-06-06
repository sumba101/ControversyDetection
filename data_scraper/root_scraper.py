import requests
import os
import json
import pandas as pd
import pickle
import time
import string

ENDPOINT = 'https://api.twitter.com/2/tweets/search/all?query='

BEARER = 'READACTED' # insert bearer token from Twitter Developer account (requires academic research access, change endpoint to "...tweets/search/recent?query=" to use standard access Twitter API)

TWEETS_PER_ITER = 500

ITER = 50

HEADERS = {"Authorization": "Bearer {}".format(BEARER)}

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    # print(response.status_code)
    if (response.status_code == 429): # 429 is the response code for having reachedd API rate limit, which resets after 15 minute window
            print('Sleeping for 15 minutes')
            time.sleep(15*61)
            print('restarted')
            response = requests.request("GET", url, headers=headers)
            # print(response.headers['x-rate-limit-reset'])
            # exit()
    if response.status_code != 200: 
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def create_topic_url(topic, count, until_id = '', endtime = '', verified=True):
    tweet_fields = "tweet.fields=lang,author_id,conversation_id,created_at,public_metrics,referenced_tweets"
    
    if verified:
        query = f'({topic} is:verified -is:reply -is:retweet lang:en)'
    else:
        query = f'({topic} -is:reply -is:retweet lang:en)'
    end_param = ''
    if until_id == '':
        end_param = f'end_time={endtime}' # send endtime in this format 2021-03-11T20:00:00Z' (endtime = 11 march 2021 20:00:00 in this case)
        # until_param = ''
    else:
        end_param = f'until_id={until_id}'

    max_return = f'max_results={str(count)}'
    # print(query) 
    url = f'{ENDPOINT}{query}&{max_return}&{end_param}&{tweet_fields}'
    # print(url)
    return url

def parse_json(response, topic, cont):
    data = []
    # print(len(response['data']))
    for tweet in response['data']:
        t_topic = topic
        t_id = tweet['id']
        text = tweet['text']
        user_id = tweet['author_id']
        root_id = tweet['conversation_id']
        is_cont = cont
        created_at = tweet['created_at']
        rt_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        # in_reply_to_tweet_id
        in_reply_to_tweet_id = '-1'
        try:
            ref_tweets = tweet['referenced_tweets']
            for refs in ref_tweets:
                if refs['type'] == 'replied_to':
                    in_reply_to_tweet_id = refs['id']
        except KeyError:
            pass       
        data.append(tuple([created_at, t_id, user_id, in_reply_to_tweet_id, root_id, reply_count, rt_count, like_count, text, t_topic, is_cont]))
    # print(len(data))
    return data

def to_df(tuples):
    return pd.DataFrame(tuples, columns=['time', 'id', 'user_id', 'parent_id', 'root_id', 'reply_count', 'rt_count', 'like_count', 'text', 'topic', 'is_cont'])    

def scrape_for_topic(topic, is_cont, num, endtime, verified=True):
    
    print(f'scraping root tweets for topic {topic}')

    fil_data = []
    i = 0
    url = create_topic_url(topic, TWEETS_PER_ITER, endtime=endtime, verified=verified)
    # print(url)
    response = connect_to_endpoint(url, HEADERS)
    tdata = parse_json(response, topic, cont=is_cont)
    until_id = tdata[-1][1]
    fil_data.extend(tdata)
    # print(len(fil_data))

    iter = 1
    while len(fil_data) < num and iter < ITER:
        iter += 1
        url = create_topic_url(topic, TWEETS_PER_ITER, until_id=until_id, verified=verified)
        # print(url)

        response = connect_to_endpoint(url, HEADERS)
        try:
            x = len(response['data'])
        except:
            return fil_data
        tdata = parse_json(response, topic, is_cont)
        until_id = tdata[-1][1]
        fil_data.extend(tdata)
        # print(len(fil_data))
    print(f'total tweets scraped for this topic: {len(fil_data)}')
    return fil_data

if __name__ == '__main__':
    topics = ['Demi Lovato']
    is_cont = 1
    endtime = '2021-05-20T00:00:00Z'
    # starttime = '2021-05-19T00:00:00Z'
    if not os.path.exists('topic_root/csv'):
        os.makedirs('topic_root/csv')
    if not os.path.exists('topic_root/pkl'):
        os.makedirs('topic_root/pkl')
    
    tweets = []
    for topic in topics:
        topic_tweets = scrape_for_topic(topic, is_cont, 1000, endtime=endtime, verified=False)
        # tweets.extend(topic_tweets)
        topic_df = to_df(topic_tweets)
        temp = topic.replace(' ', '_')
        temp = temp.replace('%23', '')
        fpkl = f'topic_root/pkl/{temp}.pkl'
        fcsv = f'topic_root/csv/{temp}.csv'
        topic_df.to_pickle(fpkl)
        topic_df.to_csv(fcsv, sep=',', header=True, index=False)

