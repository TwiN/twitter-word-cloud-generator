#!/usr/bin/env python
# encoding: utf-8

import tweepy
import os

debug = True

# Twitter API credentials
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_key = os.environ['TWITTER_ACCESS_KEY']
access_secret = os.environ['TWITTER_ACCESS_SECRET']


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter and initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    all_tweets = []
    all_full_tweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    tweets = api.user_timeline(screen_name=screen_name, count=50)

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
        if tweet.truncated:
            twt = api.get_status(tweet.id, tweet_mode='extended') # tweet was truncated, get the full tweet
            all_full_tweets.append(twt.full_text)
        else:
            all_full_tweets.append(tweet.text)

    return all_full_tweets


tweets = get_all_tweets("realDonaldTrump")


for tweet in tweets:
    print(tweet)