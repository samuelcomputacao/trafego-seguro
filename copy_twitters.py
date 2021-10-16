from dataBase import DataBase

db = DataBase()

twtters = db.getTwitters(coluns=['texto', 'classificacao'], where=[f'classificacao IS NOT NULL'])

file = open('resources/twittes_copy.csv', 'w')
file.write('texto;classificacao\n')
for tw in twtters:
    linha = f"{tw[0]};{tw[1]}\n"
    file.write(linha)
file.close()
db.close_connection()