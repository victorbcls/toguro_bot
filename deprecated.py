from time import sleep
import tweepy
import logging
from api import create_api
import random
import datetime
logging.basicConfig(filename="toguro.log", level=logging.INFO)
logger = logging.getLogger('toguro')

frases = ['tá bom, mas cadê o shape?',
          "fala fala fala, mas não vejo um shape",
          "tu não tem shape mas a atitude é responsa. teu shape é intelectual",
          "peitoral não diz nada",
          "o shape ta falando",
          "nao preciso te provar nada meu shape fala",
          "ninguém shaypado por aqui",
          "pleno 2022...",
          "mora com a mãe, tem mais de 19 anos e 5 meses, obrigação ser shaypado",
          "vamos atrás do shape, faz bem pra mente e pra cabeça",
          "shaypado?",
          "e o shape?",
          "shape?",
          "shape fellas", "nem precisa de mímica , peitoral tá falando alemão"]


class TweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
        self.tweet_id = ''

    def on_status(self, tweet):
        if tweet.user.id == self.me.id:
            return
        else:

            now = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")

            processing = f'{now} -> Processando tweet - {tweet.text}'
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
                    now = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")

                    logger.info({
                        "Status": "OK",
                        "Tweet ID": self.tweet_id,
                        "Link": f"https://twitter.com/twitter/status/{self.tweet_id}",
                        "Time": now

                    })
                    print(str({
                        "Status": "OK",
                        "Tweet ID": self.tweet_id,
                        "Link": f"https://twitter.com/twitter/status/{self.tweet_id}",
                        "Time": now

                    }))
                except tweepy.error.TweepError as error:
                    now = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")

                    print(str({
                        "Status": "Warning",
                        "Tweet ID": self.tweet_id,
                        "Link": f"https://twitter.com/twitter/status/{self.tweet_id}",

                        "Error": str(error),
                        "Time": now

                    }))
                    logger.error({
                        "Status": "Warning",
                        "Tweet ID": self.tweet_id,
                        "Link": f"https://twitter.com/twitter/status/{self.tweet_id}",
                        "Error": str(error),
                        "Time": now

                    })
                    if '429' in str(error):
                        print("Faltam 15 minutos para a próxima tentativa")
                        sleep(300)
                        print("Faltam 10 minutos para a próxima tentativa")
                        sleep(300)
                        print("Faltam 5 minutos para a próxima tentativa")
                        sleep(300)
                        print("Vou tentar denovo")

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
            stream.filter(track=['toguro', "Toguro"])

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
