import os,tweepy,re
from time import time,sleep
from auth import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)


tweet = api.user_timeline(screen_name = userID, count = 1, exclude_replies=True)[0]
tweetLen = len(tweet.text)
removeURL = removeURL = re.sub(r" http\S+", "", tweet.text) 
slicedTweet = removeURL[tweetLen::-1]
with open(log, "rb") as f:
    f.seek(2, os.SEEK_END)
    while f.read(1) != b'\n':
        f.seek(-2, os.SEEK_CUR)
    last_tweet_id = f.readline().decode()

if str(tweet.id) + "\n" == last_tweet_id:
    print("Nothing to do")
else:
    openLog = open(log, "a")
    openLog.write(str(tweet.id) + "\n")
    openLog.close()
    api.update_status(slicedTweet, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
    print("Done")