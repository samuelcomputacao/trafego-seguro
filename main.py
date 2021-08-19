import pandas as pd
from tweetAPI import TweetAPI
from datetime import datetime, timedelta
from dataBase import DataBase


def get_friends():
    df = pd.read_csv(filepath_or_buffer="resources/friends.csv", sep=";")
    classes = {1: True, 0: False}
    df['specific'] = df['specific'].apply(lambda x: classes[x])
    return df


CONSUMER_KEY = 'UZLEno0H4UqDnMbzp06lAO4K4'
CONSUMER_SECRET = '8Q60W8qUu0ZqGEMO7zpeD9MoGZD6HFTTVgrJa72VVnykVCoFwv'
ACCESS_TOKEN = '1071095366-zFazweFNeItzWbqbgojoBQNEKVUfFA1GOSyRivt'
ACCESS_TOKEN_SECRET = 'YNBChOqrv805TEW8uBD5HsagHSOeX6ufZzzPFBuNPLgx5'

api = TweetAPI(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
               access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

keywords_specific = ['ferid', 'acidente', 'mort', 'choque', 'trajédia', 'atropel',
                     'vitima', 'colisão', 'virada', 'virou', 'engavetamento', 'abalroamento', 'batida', 'capota',
                     'incendio',
                     'morre', 'faleceu', 'saiu da pista', 'tombamento', 'tombou', 'bateu']

keywords = ['acidente', 'atropela',
            'colisão', 'engavetamento', 'abalroamento', 'capotamento',
            'saiu da pista', 'tombamento', 'tombou']

date = datetime.today()
date = datetime(year=date.year, month=date.month, day=date.day)
date = date - timedelta(days=3)
print(f'Buscando Twitters em {date}')
tweets = api.search_by_friends(count=20, keywords=keywords, keywords_specific=keywords_specific, date=date,
                               friends=get_friends())

db = DataBase()
db.save_twitters(tweets)


exit()
