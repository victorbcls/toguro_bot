import tweepy
import logging
import env
import datetime
now = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
logger = logging.getLogger()


def create_api():

    auth = tweepy.OAuthHandler(env.consumer_key, env.consumer_secret)
    auth.set_access_token(env.access_token, env.access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Erro criando a API", exc_info=True)
        raise e
    print("API CRIADA")
    logger.info(f"{now} -> API criada")
    return api
