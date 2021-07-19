import os,tweepy,pyperclip,re

consumer_key = consumer_key
consumer_secret = consumer_secret
access_token_key = access_token_key
access_token_secret = access_token_secret
userID = userID
log = /path/to/log

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

while True:

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
        pyperclip.copy(slicedTweet)
        openLog = open(log, "a")
        openLog.write(str(tweet.id) + "\n")
        openLog.close
        print("Original Tweet: " + removeURL + "\n\n" + "Reversed: " + slicedTweet + "\n\n" + "Tweet ID: " + str(tweet.id))
    sleep(600 - time() % 600)
