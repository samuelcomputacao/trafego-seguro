from dataBase import DataBase

db = DataBase()

twtters = db.getTwitters(coluns=['id', 'texto'], where=[f'classificacao IS NULL'])

file = open('resources/twittes.csv', 'w')
file.write('id;texto;classificacao\n')
for tw in twtters:
    linha = f"'{tw[0]}';{tw[1]};--\n"
    file.write(linha)
file.close()
db.close_connection()
