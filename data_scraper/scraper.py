# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
import os
import json
import pandas as pd
import pickle
import time
import string
BEARER = 'ReplaceThisWithBearerToken' # Bearer Token obtained from Twitter Developer account. Used for authorising API calls. Refer README.md for additional info.

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

headers = create_headers(BEARER)


# %%
def create_tweet_url(tid):
    tweet_fields = "tweet.fields=lang,author_id,conversation_id,created_at,public_metrics,referenced_tweets"
    url = f'https://api.twitter.com/2/tweets?ids={tid}&{tweet_fields}'
    return url

def create_topic_url(topic, count, until_id = '', endtime = ''):
    tweet_fields = "tweet.fields=lang,author_id,conversation_id,created_at,public_metrics,referenced_tweets"
    query = f'({topic} is:verified -is:reply -is:retweet lang:en)'
    until_param = ''
    if until_id == '':
        until_param = f'&end_time={endtime}' # send endtime in this format 2021-03-11T20:00:00Z' (endtime = 11 march 2021 20:00:00 in this case)
        # until_param = ''
    else:
        until_param = f'&until_id={until_id}'
    # print(query) 
    url = f'https://api.twitter.com/2/tweets/search/recent?query={query}&max_results={str(count)}{until_param}&{tweet_fields}'
    # print(url)
    return url


# %%
# straight from demo code, not even an iota changed except to handle rate limits 

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


# %%
def get_row(response, topic, cont):
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


# %%
def get_topic_data(topic, is_cont, num, endtime):
    print(f'scraping root tweets for topic {topic}')

    fil_data = []

    url = create_topic_url(topic, 100, endtime=endtime)
    # print(url)
    response = connect_to_endpoint(url, headers)
    tdata = get_row(response, topic, cont=is_cont)
    until_id = tdata[-1][1]
    fil_data.extend(tdata)
    # print(len(fil_data))

    iter = 1
    while len(fil_data) < num and iter < 50:
        iter += 1
        url = create_topic_url(topic, 100, until_id=until_id)
        response = connect_to_endpoint(url, headers)
        try:
            x = len(response['data'])
        except:
            return fil_data
        tdata = get_row(response, topic, is_cont)
        until_id = tdata[-1][1]
        fil_data.extend(tdata)
        # print(len(fil_data))
    return fil_data

# %%
topics = ['Trump', 'news']
is_cont = 1
# topics is a list of strings. it can be  a hashtag (like #BengalElection) or it can be  just a string about an event (like 'Bengal Election' or 'Dr. Seuss' or 'Trump')
# if topic is a #tag, use "%23" instead of '#' i.e. '%23BengalElections' and not '#BengalElection'
data = []
for topic in topics:
    topic_data = get_topic_data(topic, is_cont=is_cont, num=1000, endtime='2021-04-16T21:00:00Z') # send is_cont = 1 if topic is controversial, num = min number of tweets to scrape for topic
    data.extend(topic_data)
    topic_df = pd.DataFrame(data, columns=['time', 'id', 'user_id', 'parent_id', 'root_id', 'reply_count', 'rt_count', 'like_count', 'text', 'topic', 'is_cont'])
    
    # temp = topic.replace(' ', '_')
    # temp = temp.replace('%23', '')
    # fpkl = f'topicwise/{temp}.pkl'
    # fcsv = f'topicwise/{temp}.csv'

    # topic_df.to_pickle(fpkl)
    # topic_df.to_csv(fcsv, sep=',', header=True, index=False)

df = pd.DataFrame(data, columns=['time', 'id', 'user_id', 'parent_id', 'root_id', 'reply_count', 'rt_count', 'like_count', 'text', 'topic', 'is_cont'])
#print()
#print(len(df))
#print()
# df.to_pickle('root.pkl')
# df.to_csv('root.csv', sep=',', header=True, index=False)


# %%
def create_reply_url(tid, uid):
    tweet_fields = "tweet.fields=lang,author_id,conversation_id,created_at,public_metrics,referenced_tweets"
    url = f'https://api.twitter.com/2/tweets/search/recent?query=(conversation_id:{tid} to:{uid})&max_results=50&{tweet_fields}'
    # print(url)
    return url


# %%
parent_tweets_df = df[df['reply_count'] >= 10] # filter out tweets with less than 20 replies
parent_tweets = [tuple(r) for r in parent_tweets_df[['id', 'user_id', 'topic', 'is_cont']].to_numpy()]
print(f"total root tweets after filtering for 10 replies: {len(parent_tweets)}")
print('beginning to scape replies, this may take a while...')
replies = []
# sample = temp[0:10]
counter = 0

for tweet in parent_tweets:
    counter += 1
    url = create_reply_url(tid=tweet[0], uid=tweet[1])
    response = connect_to_endpoint(url, headers)
    tweets = get_row(response, topic=tweet[2], cont=tweet[3])
    # print(f'obtained {len(tweets)} replies')
    replies.extend(tweets)
    if counter % 50 == 0:
        print(f'scraped replies for {counter} tweets, saving checkpoint')
        temp_df = pd.DataFrame(replies, columns=['time', 'id', 'user_id', 'parent_id', 'root_id', 'reply_count', 'rt_count', 'like_count', 'text', 'topic', 'is_cont'])
        # print(f'current length: {len(temp_df)} replies')
        temp_df.to_pickle('replies_checkpoint.pkl')
print(f"total number of tweets including replies: {len(replies) + len(parent_tweets)}")
replies_df = pd.DataFrame(replies, columns=['time', 'id', 'user_id', 'parent_id', 'root_id', 'reply_count', 'rt_count', 'like_count', 'text', 'topic', 'is_cont'])
replies_df = replies_df.append(parent_tweets_df)
if len(topics) > 1:
    topic = "_".join(topics)
else:
    topic = topic[0]
temp = topic.replace(' ', '_')
temp = temp.replace('%23', '')
replies_df.to_pickle(f'topicwise/{temp}_root_n_replies.pkl')
replies_df.to_csv(f'topicwise/{temp}_root_n_replies.csv', sep=',', header=True, index=False)


# %%



