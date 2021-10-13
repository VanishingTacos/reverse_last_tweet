import os
import tweepy
import re
import sys
import urllib.request
import ffmpeg
from auth import *

# Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

# Authentication check
if not api.verify_credentials():
    sys.exit("Authentication ERROR!")


tweet = api.user_timeline(screen_name = userID, count = 1, exclude_replies=True, tweet_mode = "extended", include_rts = False)[0] # Pulls latest tweet from users timeline that is not a reply or rt


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
    # open log and appends new tweet ID
    openLog = open(log, "a")
    openLog.write(str(tweet.id) + "\n")
    openLog.close()
    tweetLen = len(tweet.full_text) # calculate the tweets length
    removeURL = re.sub(r'http\S+', '',tweet.full_text) # Removes URL from the tweet if one is found
    slicedTweet = removeURL[tweetLen::-1] # Reverses the tweet

    # try to get video info. if none is found then skip
    try:
        media_info = tweet.extended_entities["media"][0]["video_info"] # get media info
        # if media is video then continue
        if media_info["variants"][1]["content_type"] == "video/mp4":
            video_link = media_info["variants"][1]["url"] # get video url
            urllib.request.urlretrieve(video_link, media + "video0.mp4") # download video
            in_file = ffmpeg.input(media + "video0.mp4") # input file for ffmpeg
            reversed_video = in_file.video.filter("reverse") # reverse video
            reversed_audio = in_file.audio.filter("areverse") # reverse audio
            join = ffmpeg.concat(reversed_video,reversed_audio, v=1, a=1) # recombine video and audio
            out = join.output(media + "out0.mp4") # out file
            args = out.global_args('-loglevel', 'quiet') # shut up ffmpeg
            args.run() # run ffmpeg
            upload = api.media_upload(media + "out0.mp4", chunked = True, media_category = "tweet_video") # upload video
            api.update_status(slicedTweet, in_reply_to_status_id = tweet.id, auto_populate_reply_metadata = True, media_ids=[upload.media_id_string]) # post reply with video
            # remove videos
            os.remove(media + "video0.mp4")
            os.remove(media + "out0.mp4")
        print("Done")

    except:
        # check if tweet contains a url
        if tweet.entities['urls']:
            for url in tweet.entities['urls']:
                # if expanded_url is equal to twitch link then get tweet link and retweet
                if url['expanded_url'] == "http://twitch.tv/" + twitch:
                    liveLink = ("https://twitter.com/" + userID + "/statuses/" + str(tweet.id))
                    api.update_status(slicedTweet + "\n\n" + liveLink )

                elif url['expanded_url'] == "https://twitch.tv/" + twitch:
                    liveLink = ("https://twitter.com/" + userID + "/statuses/" + str(tweet.id))
                    api.update_status(slicedTweet + "\n\n" + liveLink )
                else:
                    # else if tweet has link and is not a twitch link then just reply
                    api.update_status(slicedTweet, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True) # reply to tweet
        else:
            api.update_status(slicedTweet, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True) # reply to tweet

        print("Done")