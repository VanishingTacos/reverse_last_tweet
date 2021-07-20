import os,tweepy,re,sys
from auth import *


# Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

# Authentication check
if api.verify_credentials() == False:
    sys.exit("Authentication ERROR!")
else:
    print("Authentication OK!")

tweet = api.user_timeline(screen_name = userID, count = 1, exclude_replies=True, tweet_mode = "extended", include_rts = False)[0] # Pulls latest tweet from users timeline that is not a reply or a rt

# Check log for the latest entry
with open(log, "rb") as f:
    f.seek(2, os.SEEK_END)
    while f.read(1) != b'\n':
        f.seek(-2, os.SEEK_CUR)
    last_tweet_id = f.readline().decode()

# If latest current tweet ID matches latest log entry then do nothing, else post reversed tweet
if str(tweet.id) + "\n" == last_tweet_id:
    print("Nothing to do")
else:
    openLog = open(log, "a")
    openLog.write(str(tweet.id) + "\n")
    openLog.close()
    tweetLen = len(tweet.full_text) # Caculate the tweets length
    removeURL = re.sub(r" http\S+", "", tweet.full_text) # Removes URL from the tweet if one is found 
    slicedTweet = removeURL[tweetLen::-1] # Reverses the tweet
    api.update_status(slicedTweet, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True) # reply to tweet
    print("Done")