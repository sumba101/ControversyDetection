# Twitter Controversy Detection
## Dataset Scraper

The file `scraper.py` is used for scraping tweets from twitter using Twitter API v2. The output will be present in the `topicwise` directory, in both pickled and csv formats.<br>

### Setup
1. Ensure directory `topicwise` is present in the same directory as `scraper.py`. If it is not:

```bash
/PATH/TO/data_scraper $ mkdir topicwise
```

2. Install pre-requisites
```bash
/PATH/TO/data_scraper $ pip3 install -r requirements.txt
```

3. Modify `scraper.py` for usage (see **Usage Instructions**)

4. Run the file:

```bash
/PATH/TO/data_scraper $ python3 scraper.py
```

5. The scraped tweets and their replies will be available in `topicwise/<topic>_root_n_replies.pkl` and `topicwise/<topic>_root_n_replies.csv`.<br>
The pickle file contains the root tweets and their replies loaded into a pandas dataframe. The csv file contains the same dataframe dumped in csv format. 

Note: For information about the dataframe, refer **Data Description**

### Usage Instructions
0. You will need a twitter developer account and generate a bearer token for it and place in `BEARER = 'insert bearer token here'`. This is used to authorise all calls to Twitter API and the code will not run without it. Refer [Twitter Developer Portal](developer.twitter.com) for instructions on obtaining a developer account and generating a bearer token
  
1. Add topics to be scraped. Topics to be scraped should be put in as a `list` of strings in `line 133` of `scraper.py`. Ensure all topics to be scraped are to have the same label. For scraping hastags, use url encoding for `#`.

2. change `is_cont` in `line 134` to **1** if the topic is controversial, **0** otherwise. <br>

 For eg, to scrape the topics *trump* and *#election* as controversial topics, the file should look like this:
```py
131: .
132: .
133: topics = ['trump', '%23election']
134: is_cont = 1
135: .
136: .
```
3. Following are the tuning parameters that individual can change on the basis of their requirements . 
   1. ``` is:verified ``` _line 39_ - Tag to consider only verified accounts ( usually a preferable choice as those tweets are rich with replies ) . 
   2. ``` -is:retweet ``` _line 39_ - Tag to not consider retweets ( redundant information ) .
   3. ``` -is:reply ``` _line 39_ - Tag to not consider the replies as the root tweet . 
  4. The user also needs to change the date and time in the section of ``` endtime ``` in _line 139_ to the current date and time in UTC This is the latest tweet that will be scraped i.e. tweets posted after this timestamp will not be retrieved. This is to ensure that enough replies have been made to the scraped tweets. The format for date is **yyyy-mm-dd** and for time is 24 hrs format .  For example : 
   ``` endtime='2021-04-16T21:00:00Z ``` is an example of time stamp 16th April 2021 , 2100 hrs UTC .  
### Data description

The dataset is a single Pandas dataframe containing 11 columns:
1. **time**: the time at which the tweet was posted
1. **id**: the unique that twitter assigns to every tweet
1. **user_id**: the unique id of the user who posted the tweet
1. **parent_id**: this is the unique ***id*** of the tweet to which the current tweet is a reply. For eg, If tweet X has ***parent_id*** corresponding to ***id*** of tweet Y. then X is posted in reply to Y. This column is set to -1 for root tweets, i.e. tweets that are not posted as a reply to any other tweets.
1. **root_id**: The ***id*** of the root tweet of a conversation (returned by twitter API as conversation_id). For eg, if X is a root tweet, Y is a reply to X, and Z is a reply to Y, then X, Y and Z will all have the same ***root_id***, which is the ***id*** of X. This is different from ***parent_id***: Z[*parent_id*] = Y[*id*] but Z[*root_id*] = X[*id*]
1. **reply_count**: the number of repies this tweet has recieved
1. **rt_count**: the number of times that this tweet has been retweeted
1. **like_count**: the number of likes this tweet has recieved
1. **text**: the full text of the tweet, including links, emoticons, hashtags, user mentions etc.
1. **topic**: the topic which this tweet was scraped for. For tweets that are not root tweets, it is the topic for which the root tweet has been scraped for.
1. **is_cont**: binary value. **1** if the topic associated with this tweet is controversial, **0** if it is not. 






