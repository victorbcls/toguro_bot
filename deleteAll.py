import tweepy
# from tweet import tweet
from api import create_api
api = create_api()


# função para deletar todos os tweets da conta, para casos extremos de bug
# não utilizado nunca
def deleteAll():
    timeline = tweepy.Cursor(api.user_timeline).items()
    for tweet in timeline:
        print("deletando um tweet")
        print(tweet.text)
        api.destroy_status(tweet.id)
        print("tweet deletado")


deleteAll()
