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

    def getDadosPRF(self, coluns=["*"], where=[]):
        where.append("1=1")
        cur = self.connection.cursor()
        cur.execute(f"SELECT {','.join(coluns)} FROM dados_prf WHERE {' AND '.join(where)}")
        rs = cur.fetchall()
        cur.close()
        return rs

    def getEstados(self, coluns=["*"], where=[]):
        where.append("1=1")
        cur = self.connection.cursor()
        cur.execute(f"SELECT {','.join(coluns)} FROM estado WHERE {' AND '.join(where)}")
        rs = cur.fetchall()
        cur.close()
        return rs

    def getMunicipios(self, coluns=["*"], where=[]):
        where.append("1=1")
        cur = self.connection.cursor()
        cur.execute(f"SELECT {','.join(coluns)} FROM municipio WHERE {' AND '.join(where)}")
        rs = cur.fetchall()
        cur.close()
        return rs

    def getRodoviasFederais(self, coluns=["*"], where=[]):
        where.append("1=1")
        cur = self.connection.cursor()
        cur.execute(f"SELECT {','.join(coluns)} FROM rodovias_federais WHERE {' AND '.join(where)}")
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

    def salvarClassificacao(self, tweets = []):
        if len(tweets) > 0:
            sql = "CREATE TABLE IF NOT EXISTS dados_prf(" \
                  "id VARCHAR(255)," \
                  "ufbr VARCHAR(10)," \
                  "km_trunc INTEGER," \
                  "dia_semana_num INTEGER," \
                  "turno_simples INTEGER," \
                  "tipo_pista_simples INTEGER," \
                  "categoria_sentido_via INTEGER," \
                  "tracado_via_simples INTEGER," \
                  "condicao_metereologica_simples INTEGER," \
                  "tipo_acidente_simples INTEGER," \
                  "classe INTEGER)"
            cur = self.connection.cursor()
            cur.execute(sql)
            self.connection.commit()
            for tw in tweets:
                if not len(self.getDadosPRF(where=[f"id = '{tw['id']}'"])) > 0:
                    sql = f"INSERT INTO dados_prf (id,ufbr,km_trunc,dia_semana_num,turno_simples,tipo_pista_simples,categoria_sentido_via,tracado_via_simples," \
                          f"condicao_metereologica_simples,tipo_acidente_simples,classe)" \
                          f" VALUES ('{tw['id']}','{tw['ufbr']}',{tw['km_trunc']},{tw['dia_semana_num']},{tw['turno_simples']}," \
                          f"{tw['tipo_pista_simples']},{tw['categoria_sentido_via']},{tw['tracado_via_simples']}," \
                          f"{tw['condicao_metereologica_simples']},{tw['tipo_acidente_simples']},{tw['classe']})"
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
