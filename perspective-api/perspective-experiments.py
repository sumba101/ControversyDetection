#!/usr/bin/env python
# coding: utf-8

# In[1]:
import time

import pickle
import json 
import requests
import time
import pandas as pd
from collections import defaultdict as dd
print("Starting", flush=True)
time.sleep(5)
# In[2]:


with open('data/final.pickle', 'rb') as f:
    tmp = pickle.load(f)
    df = pd.DataFrame.from_dict(tmp)
    
# df = pd.read_csv('data/final.pickle')


# In[ ]:





# In[3]:


parents = df[df['parent_ID'] == '-1']


# In[4]:


comments = df[df['parent_ID'] != '-1']


# In[5]:


pdict = parents.reset_index(drop=True).to_dict()
new = dd()
for i in range(len(pdict['tweet_id'])):
    parent = pdict['tweet_id'][i]
    tmp = comments[comments['parent_ID']==parent]
    new[parent] = tmp.tweet_raw_text.values
#     tmp1.append(tmp.shape[0])
#     break


# In[6]:


count = 0
counts = []
for i in new.keys():
    tmp = []
    for j in new[i]:
        if '&gt' not in j or j.strip() != '':
            tmp.append([count, j])
            count += 1
    counts.append(len(tmp))
    new[i] = tmp
#     print(new[i])
#     break
# count


# In[7]:


abc = 0
for i in counts:
    if i < 10:
        abc += 1
abc, count


# In[8]:


for i in new.keys():
    print(new[i])
    break


# In[9]:


# f = open('data/', 'rb')
# data = pickle.load(f)


# In[10]:


# full_tweet = data['full_tweet']
# tweet_raw_text = data['tweet_raw_text']
# task1 = data['task_1']


# In[11]:


api_key = 'AIzaSyBLnXd0ElYhQ9WzUaN-9sI4fPavky3md3o'
url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +    
    '?key=' + api_key)
lg = ['en']
attr = ['TOXICITY', 'SEVERE_TOXICITY', 'TOXICITY_FAST', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT', 'SEXUALLY_EXPLICIT', 'OBSCENE']
attr_dict = {}
attr_results = {}
for i in attr:
    attr_dict[i] = dd()
    attr_results[i+'_WHOLE'] = dd()
    attr_results[i+'_RAW'] = dd()
attr_results['RAW_SPAN'] = []
attr_results['WHOLE_SPAN'] = []


# In[12]:


test = 0
if test:
    count = 0
    tmp = dd()
    for i in new.keys():
        tmp[i] = new[i]
        count += 1
        if count == 5:
            break
    new = tmp


# In[13]:


new['1369678162427318275']


# In[ ]:


import time
from tqdm import tqdm
ts = time.time()
count = 0
for i in tqdm(new.keys()):
    for j in new[i]:
        data_dict = {
            'comment': {'text': j[1]},
            'languages': lg,
            'requestedAttributes': attr_dict
        }
        count += 1
        time.sleep(1.2)
        response = requests.post(url=url, data=json.dumps(data_dict))
        response_dict = json.loads(response.content)
#         print(response_dict)
        try:
            for i in attr:
                attr_results[i+'_WHOLE'][j[0]] = response_dict["attributeScores"][i]["summaryScore"]["value"]
#         attr_results['WHOLE_SPAN'].append(response_dict["attributeScores"]['TOXICITY_FAST']['spanScores'])
        except:
            print(response_dict)
        if count % 10 == 0:
            print("Sentences processed:", count, time.time() - ts, flush=True)
        # print(full_tweet[i], response_dict["attributeScores"]["TOXICITY"]["summaryScore"]["value"], task1[i])
        # print(json.dumps(response_dict, indent=2))
te = time.time()
print(ts-te)


# In[ ]:


with open('data/perspective_scores.pickle','wb+') as f:
    pickle.dump(attr_results, f)
with open('data/perspective_scores.pickle','rb') as f:
    tmp = pickle.load(f)
    print(tmp.keys())


# In[ ]:


# time.sleep(1.5)
# count = 0
# for i in range(3161, len(tweet_raw_text)):
#     data_dict = {
#         'comment': {'text': tweet_raw_text[i]},
#         'languages': lg,
#         'requestedAttributes': attr_dict
#     }
#     response = requests.post(url=url, data=json.dumps(data_dict)) 
#     response_dict = json.loads(response.content)
#     time.sleep(1.5)
#     count += 1
#     for j in attr:
#         attr_results[j+'_RAW'].append(response_dict["attributeScores"][j]["summaryScore"]["value"])
#     attr_results['RAW_SPAN'].append(response_dict["attributeScores"]['TOXICITY_FAST']['spanScores'])
#     if count % 100 == 0:
#         print("Sentences processed:", count)
#     # print(full_tweet[i], response_dict["attributeScores"]["TOXICITY"]["summaryScore"]["value"], task1[i])
#     # print(json.dumps(response_dict, indent=2))


# In[ ]:


# tweet_raw_text[3160]


# In[ ]:


# filehandler = open("perspective_api_info/en.pickle","wb")
# pickle.dump(attr_results,filehandler)
# filehandler.close()


# In[ ]:


# time.sleep(1.1)


# In[ ]:


# f = open('perspective_api_info/en.pickle', 'rb')
# attr_results = pickle.load(f)


# In[ ]:


# for i in data.keys():
#     print(i, len(attr_results[i]))


# In[ ]:


# for i in attr:
#     attr_results[i+'_RAW'] = []


# In[ ]:


# for j in attr:
#     attr_results[j+'_RAW'].append(-1)
# attr_results['RAW_SPAN'].append([])


# In[ ]:




