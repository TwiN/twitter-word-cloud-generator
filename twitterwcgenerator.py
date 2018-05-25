#!/usr/bin/env python
# encoding: utf-8

import tweepy
import os
from os import path
import matplotlib.pyplot as plt

from wordcloud import WordCloud


debug = True

# Twitter API credentials: https://developer.twitter.com/en/apply-for-access
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_key = os.environ['TWITTER_ACCESS_KEY']
access_secret = os.environ['TWITTER_ACCESS_SECRET']


# Twitter only allows access to a users most recent 3240 tweets with this method
def get_all_tweets(screen_name):
    # authorize twitter and initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    all_tweets = []
    all_full_tweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    all_tweets.extend(tweets)

    # save the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1

    while len(tweets) > 0 and not debug:
        tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        all_tweets.extend(tweets) # add them to the list
        oldest = all_tweets[-1].id - 1 # get the id of the last tweet fetched
        print("...%s tweets fetched so far" % (len(all_tweets)))

    for tweet in all_tweets:
        twt = tweet.text
        if tweet.truncated:
            twt = api.get_status(tweet.id, tweet_mode='extended').full_text
        twt = clean_tweet(twt)
        all_full_tweets.append(twt)

    return all_full_tweets


def clean_tweet(tweet):
    try:
        tweet = tweet[:tweet.index("https://t.co/")]
    except ValueError:
        pass
    return tweet


tweets = get_all_tweets("realDonaldTrump")


with open('tweets.txt', 'w', encoding='UTF-8') as f:
    f.write("\n".join(tweets))


d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, 'tweets.txt'), encoding='utf-8').read()

# Generate a word cloud image
wordcloud = WordCloud().generate(text)

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()