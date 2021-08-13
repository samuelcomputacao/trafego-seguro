from dataBase import DataBase

db = DataBase()
file = open('resources/twittes.csv', 'r')
flag = True
tweets = []
for linha in file:
    if flag:
        flag = False
    else:
        linha = linha.strip().split(';')
        classificacao = linha[2]
        if classificacao in ['0', '1']:
            tweets.append({
                'id': linha[0].replace("'",""),
                'classificacao': classificacao
            })
db.update_twitters(tweets)
db.close_connection()
