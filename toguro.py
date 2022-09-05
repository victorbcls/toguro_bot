from time import sleep
import tweepy
import logging
from api import create_api
import random
logging.basicConfig(filename="toguro.log", level=logging.INFO)
logger = logging.getLogger('toguro')

frases = ['falou tudo pai',
          "concordo em tudo",
          'orgulho em ter shape',
          'o shape é maior que tudo fellas',
          'ninguém segura o shape do togs',
          'eh o shape']


class TweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
        self.tweet_id = ''

    def on_status(self, tweet):
        if tweet.user.id == self.me.id:
            return
        else:
            processing = f'Processando tweet - {tweet.text}'
            msg = logger.info(processing)
            self.tweet_id = tweet.id
            try:
                original_tweet = tweet.extended_tweet['full_text']
            except:
                original_tweet = tweet.text
            print(original_tweet)

            if tweet.is_quote_status == False & tweet.favorited == False:
                # aqui existe um bug... Se alguem retuitar um tweet que o bot ja curtiu/comentou, ele passa por essa verificação.
                # não chega a quebrar o app, só registra no log com warning. logo mais descubro como resolver
                try:
                    print(msg)
                    tweet.favorite()

                    api.update_status(
                        status=random.choice(frases), in_reply_to_status_id=self.tweet_id, auto_populate_reply_metadata=True)

                    logger.info({
                        "Status": "OK",
                        "Tweet ID": self.tweet_id,
                        "Link": f"https://twitter.com/twitter/status/{self.tweet_id}"
                    })
                    print(str({
                        "Status": "OK",
                        "Tweet ID": self.tweet_id,
                        "Link": f"https://twitter.com/twitter/status/{self.tweet_id}"
                    }))
                except tweepy.error.TweepError as error:

                    print(str({
                        "Status": "Warning",
                        "Tweet ID": self.tweet_id,
                        "Link": f"https://twitter.com/twitter/status/{self.tweet_id}",
                        "Error": str(error)
                    }))
                    logger.error({
                        "Status": "Warning",
                        "Tweet ID": self.tweet_id,
                        "Link": f"https://twitter.com/twitter/status/{self.tweet_id}",
                        "Error": str(error)
                    })
                    sleep(300)
                    pass

    def on_error(self, status):
        print(status.text)

        logger.error(status)
        if status == 420:
            return False


if __name__ == '__main__':
    api = create_api()
    tweets_listener = TweetListener(api)
    while True:
        try:
            stream = tweepy.Stream(auth=api.auth, listener=tweets_listener)
            stream.filter(follow="1182861037")

        except Exception as error:
            print(str({
                "Status": "Critical",
                "Tweet ID": tweets_listener.tweet_id,
                "Link": f"https://twitter.com/twitter/status/{tweets_listener.tweet_id}",
                "Error": str(error)
            }))
            logger.error({
                "Status": "Critical",
                "Tweet ID": tweets_listener.tweet_id,
                "Link": f"https://twitter.com/twitter/status/{tweets_listener.tweet_id}",
                "Error": str(error)
            })
            pass
