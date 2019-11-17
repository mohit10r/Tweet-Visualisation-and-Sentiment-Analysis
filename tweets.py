from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import twitter
import numpy as np
import pandas as pd

class TwitterClient():
    def __init__(self,twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self,num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline,id = self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets    

    def get_twitter_client(self):
        return self.twitter_client

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter.CONSUMER_KEY, twitter.CONSUMER_SECRET)
        auth.set_access_token(twitter.ACCESS_KEY,twitter.ACCESS_SECRET)
        return auth



class TwitterStreamer():

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()


    def stream_tweets(self,fetched_tweets_filename,hash_tag_list):
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth,listener)
        stream.filter(track=hash_tag_list)            


class TwitterListener(StreamListener):

    def __init__(self,fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_filename,'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data : %s" %str(e))
        return True    

    def on_error(self,status):
        if status==420:
            return False

class TweetAnalyzer():
    def tweets_to_data_frame(self,tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['Tweets'])
        return df
    
if __name__ == "__main__":
    
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client()
    tweets = api.user_timeline(screen_name='realDonaldTrump',count=20)
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    #print(df.head(10))
    print(tweets[0].retweet_count)