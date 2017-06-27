# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

import sys
# We use the file saved from last step as example
tweets_filename = sys.argv[1]
tweets_file = open(tweets_filename, "r")

import csv
f2 = open(sys.argv[1].replace(".txt", "_processed.csv"), 'w')
fout = csv.writer(f2)

for line in tweets_file:
    try:
        # Read in one line of the file, convert it into a json object 
        tweet = json.loads(line.strip())
        if 'text' in tweet: # only messages contains 'text' field is a tweet
            d2w = []
            d2w.append(tweet['id']) # This is the tweet's id
            #print tweet['created_at'] # when the tweet posted
            d2w.append(tweet['text']) # content of the tweet
                        
            #print tweet['user']['id'] # id of the user who posted the tweet
            #print tweet['user']['name'] # name of the user, e.g. "Wei Xu"
            d2w.append(tweet['user']['screen_name']) # name of the user account, e.g. "cocoweixu"
            fout.writerow(d2w)
            #hashtags = []
            #for hashtag in tweet['entities']['hashtags']:
            #    hashtags.append(hashtag['text'])
            #print hashtags

    except:
        # read in a line is not in JSON format (sometimes error occured)
        continue
