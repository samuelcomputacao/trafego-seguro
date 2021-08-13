import psycopg2


class DataBase:
    connection = None

    def __init__(self):
        self.connection = psycopg2.connect(host='localhost', database='transito', user='postgres', password='12345')

    def getTwitters(self, coluns=["*"], where=[]):
        where.append("1=1")
        cur = self.connection.cursor()
        cur.execute(f"SELECT {','.join(coluns)} FROM twitter WHERE {' AND '.join(where)}")
        rs = cur.fetchall()
        cur.close()
        return rs

    def close_connection(self):
        self.connection.close()

    def update_twitters(self, tweets=[]):
        if len(tweets) > 0:
            cur = self.connection.cursor()
            for tw in tweets:
                sql = f"UPDATE twitter SET classificacao='{tw['classificacao']}' WHERE id='{tw['id']}'"
                cur.execute(sql)
            self.connection.commit()

    def save_twitters(self, tweets):
        print('Salvando Twitters')
        cont = 0
        sql = "CREATE TABLE IF NOT EXISTS twitter( " \
              "usuario VARCHAR(100)," \
              "local VARCHAR(100)," \
              "texto VARCHAR(500) NOT NULL," \
              "data VARCHAR(20)," \
              "id BIGINT," \
              "CONSTRAINT tweet_pk PRIMARY KEY(id))"
        cur = self.connection.cursor()
        cur.execute(sql)
        self.connection.commit()
        for tw in tweets:
            if not len(self.getTwitters(where=[f"id = '{tw['id']}'"])) > 0:
                sql = f"INSERT INTO twitter (id, usuario, local, texto, data) VALUES ('{tw['id']}','{tw['usuario']}','{tw['local']}','{tw['texto']}','{tw['data']}')"
                try:
                    cur.execute(sql)
                    cont += 1
                    for link in tw['links']:
                        sql = f"INSERT INTO link (id_tw, endereco) VALUES ('{tw['id']}','{link}')"
                        cur.execute(sql)
                except Exception as err:
                    print("Error: {0}".format(err))
                    pass
        self.connection.commit()
        print(f'Twitters salvos: {cont}')
