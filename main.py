import datetime
import random
from time import sleep
import tweepy
import logging
import env
from api import create_api
api = create_api()

bearer_token = env.bearer_token

client = tweepy.Client(bearer_token=bearer_token, access_token=env.access_token,
                       access_token_secret=env.access_token_secret, consumer_key=env.consumer_key, consumer_secret=env.consumer_secret)


while True:
    response = client.search_recent_tweets(
        query='toguro -is:retweet', max_results=60)

    logging.basicConfig(filename="toguro.log", level=logging.INFO)
    logger = logging.getLogger('toguro')

    frases = ['tá bom, mas cadê o shape?',
              "fala fala fala, mas não vejo um shape",
              "tu não tem shape mas a atitude é responsa. teu shape é intelectual",
              "o shape ta falando",
              "nao preciso te provar nada meu shape fala",
              "ninguém shaypado por aqui",
              "pleno 2022...",
              "mora com a mãe, tem mais de 19 anos e 5 meses, obrigação ser shaypado",
              "vamos atrás do shape, faz bem pra mente e pra cabeça",
              "shaypado?",
              "e o shape?",
              "shape?",
              "shape fellas", "nem precisa de mímica, peitoral tá falando alemão",
              "uma vida sem Shape é viver como um mero mortal",
              "pega busão ou metrô pra estudar ou trabalhar, obrigatoriamente tem que estar shaypado",
              "tá acordando agora pra trabalhar, ganha menos de 3 mil por mês, obrigatoriamente tem que estar shaypado",
              "joga free Fire, ten menos de 1 milhão na conta, obrigatoriamente tem que ser shaypado",
              "se você joga minecraft, obrigatoriamente precisa estar no Shape"]

    tweets = response.data

    for tweet in tweets:
        print(tweet)
        if ' toguro' not in str(tweet) and ' Toguro' not in str(tweet) and 'Toguro ' not in str(tweet) and 'toguro ' not in str(tweet) or '_toguro' in str(tweet):
            print("NÂO TINHA PO")
            continue
        try:
            status = api.get_status(tweet.id)
            if status.favorited == False:
                client.like(tweet.id, user_auth=True)
                api.update_status(
                    status=random.choice(frases), in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                now = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")

                logger.info({
                    "Status": "OK",
                    "Tweet ID": tweet.id,
                    "Link": f"https://twitter.com/twitter/status/{tweet.id}",
                    "Time": now

                })
                print(str({
                    "Status": "OK",
                    "Tweet ID": tweet.id,
                    "Link": f"https://twitter.com/twitter/status/{tweet.id}",
                    "Time": now

                }))
        except Exception as err:
            now = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
            logger.warning({
                "Status": err,
                "Tweet ID": tweet.id,
                "Link": f"https://twitter.com/twitter/status/{tweet.id}",
                "Time": now

            })
            print({
                "Status": err,
                "Tweet ID": tweet.id,
                "Link": f"https://twitter.com/twitter/status/{tweet.id}",
                "Time": now

            })
            pass
        sleep(60)
