import requests
from requests.structures import CaseInsensitiveDict
import os
import json
import pandas as pd
import pickle
import time
BEARER = 'AAAAAAAAAAAAAAAAAAAAALo6NAEAAAAAP%2BhqPpvJq2FY5S2%2Bs28OwLyh7CE%3Dr1K8imd2QZvtIKFRICXmHUQsC1WcRBkDiVXExVJFjNZYpJBx8L'

headers = {"Authorization": f'Bearer {BEARER}'}

# main function to retrieve data from twitter using twitter API
def connectToEndpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    # print(response.status_code)
    if (response.status_code == 429):
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

# functions to create urls to use with connect_to_endpoint()
def createTweetUrl(tid):
    tweet_fields = "tweet.fields=author_id,conversation_id"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = f'https://api.twitter.com/2/tweets?ids={tid}&{tweet_fields}'
    return url

def createReplyUrl(tid, uid):
	tweet_fields = "tweet.fields=author_id,conversation_id"
	url = f'https://api.twitter.com/2/tweets/search/recent?query=(conversation_id:{tid} to:{uid})&max_results=50&{tweet_fields}'
    # print(url)
	return url

def createUserUrl(uname):
    usernames = f'usernames={uname}'
    url = f'https://api.twitter.com/2/users/by?{usernames}'
    return url

def createTimelineUrl(uid):
	tweet_fields = "tweet.fields=author_id,conversation_id"
	url = f'https://api.twitter.com/2/users/{uid}/tweets?max_results=10&{tweet_fields}'
	return url

# function to parse JSON response received from Twitter API
def parseResponse(response):
	data = []
	try:
		for tweet in response['data']:
			tid = tweet['id']
			text = tweet['text']
			con_id = tweet['conversation_id']
			auth_id = tweet['author_id']
			info = tuple([tid, con_id, auth_id, text])
			data.append(info)
		return data
	except KeyError:
		return data
 
def fetch_score(text, comments):
    text = {
        'root' : text,
        'comments' : comments
    }
    # print('request sent')
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    res = requests.post("https://34d7e88b877b.ngrok.io/predict_status", headers=headers, data=json.dumps(text))
    print(res)
    return res.json()['contro']

# main driver code
def driverFunction(url):
# url : Url of the twitter page
# THE OBJECT RETURED BY THIS MUST BE DICTIONARY OF TWEET TEXT TO CONTROVERSIALITY BOOL(True/False)
# Example: 	response = {"#WestBengalPolls | \"She [Mamata] alleges that polling agent was ousted from one booth. But said nothing when her people pelted stones on media and injured one. Her political ground is slipping away. What she did is illegal\": @SuvenduWB, BJP candidate from Nandigram (reports ANI)":" True"}

	# url= "https://twitter.com/" + url
	# output = processTweet(url)
	# output = dict(sorted(output.items(), key=lambda item: item[1]))
	
	string = url.split('/')
	if len(string) == 1:
		roots, replies = processProfile(url)
	else:
		roots, replies = processStatus(string[-1])
	
	results = {}
	for i, root in roots.iterrows():
		# print(type(temp_roots))
		# print(root)
		text = root['text']
		comments = []
		con_id = root['conversation_id']
		# print(con_id)
		reply = replies[replies['conversation_id'] == con_id]
		try:
			sample_reply = reply.sample(10)
		except ValueError:
			sample_reply = reply 
		# print(sample_reply)
		for j, tweet in sample_reply.iterrows():
			comments.append(tweet['text'])
		results[text] = bool(fetch_score(text, comments))
		
	# Please check receiver.py to see sample returned values

	return results

def processStatus(tid):

	# output = {"Every single American has a right to clean drinking water. It’s just plain wrong that in the United States of America today, millions of children still receive their water through lead service pipes. It’s long past time we fix that.":True}

	tweetUrl = createTweetUrl(tid)
	response = connectToEndpoint(tweetUrl, headers)

	tweet = parseResponse(response)

	if len(tweet) == 0:
		# HANDLE THIS ERROR PLEASE IDK WHAT TO DO IF THIS HAPPENS
		print('Tweet not found')
		return tweet
	
	replyUrl = createReplyUrl(tweet[0][1], tweet[0][2])
	response = connectToEndpoint(replyUrl, headers)

	reply = parseResponse(response)

	tweets = pd.DataFrame(tweet, columns = ['tweet_id', 'conversation_id', 'author_id', 'text'])

	replies= pd.DataFrame(reply, columns = ['tweet_id', 'conversation_id', 'author_id', 'text'])


	return tweets, replies

def getUserId(name):
    userUrl = createUserUrl(name)
    response = connectToEndpoint(userUrl, headers)
    try:
	    uid = response['data'][0]['id']
	    return uid
    except KeyError:
	    return -1

def processProfile(name):

	user_id = getUserId(name)
	if user_id == -1:
		print('Error: User not found')
		return -1

	timelineUrl = createTimelineUrl(user_id)
	response = connectToEndpoint(timelineUrl, headers)

	tweets = parseResponse(response)

	rootTweets = pd.DataFrame([], columns = ['tweet_id', 'conversation_id', 'author_id', 'text']) 
	replies = pd.DataFrame([], columns = ['tweet_id', 'conversation_id', 'author_id', 'text']) 

	for tweet in tweets:
		root, reply = processStatus(tweet[0])
		rootTweets = rootTweets.append(root)
		replies = replies.append(reply)

	return rootTweets, replies

# if __name__ == '__main__':
# 	url = 'BarackObama'
# 	results = driverFunction(url)
# 	for text in results.keys():
# 		print(text, results[text])
