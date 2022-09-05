import tweepy
from api import create_api
api = create_api()       

#funçao para tweetar o que está se passando como parametro 
def tweet(str):
    api.update_status(str)

