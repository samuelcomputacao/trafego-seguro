from dataBase import DataBase
from util.string_util import clean_text, incluso

dataBase = DataBase()

ESTADOS = {}
MUNICIPIOS = {}

for mun in dataBase.getMunicipios(coluns=['nm_mun', 'sigla_uf']):
    MUNICIPIOS[clean_text(mun[0].lower())] = mun[1].lower()
for uf in dataBase.getEstados(coluns=['nm_uf', 'sigla_uf']):
    ESTADOS[clean_text(uf[0].lower())] = uf[1].lower()


def eh_numero(char):
    return str(char) in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def extrai_parte_numerica(texto):
    retorno = ''
    flag = False
    for i in range(len(texto)):
        if eh_numero(texto[i]) and not flag:
            retorno += texto[i]
    return retorno


def extrai_km(tw):
    texto = list(filter(lambda x: len(x) > 0, tw[2].split(" ")))
    for i in range(len(texto)):
        token = texto[i]
        km = -1
        if len(token) > 2:
            if token[0:2] == 'km':
                km = extrai_parte_numerica(token)
                if len(km) == 0 and i + 1 < len(texto):
                    km = extrai_parte_numerica(texto[i + 1])
        elif len(token) == 2 and token == "km":
            if i + 1 < len(texto):
                km = extrai_parte_numerica(texto[i + 1])

        if km != -1:
            if len(km) > 0:
                try:
                    km = int(km)
                    return km
                except ValueError:
                    print("Erro ao converter km!")
                    pass
    print(f"KM não Encontrado: {tw[2]}")
    return None


def extrai_br(tw):
    uf = extrai_uf(tw)
    texto = list(filter(lambda x: len(x) > 0, tw[2].split(" ")))
    for i in range(len(texto)):
        token = texto[i]
        br = -1
        if len(token) > 2:
            if token[0:2] == 'br':
                br = extrai_parte_numerica(token)
                if len(br) == 0 and i + 1 < len(texto):
                    br = extrai_parte_numerica(texto[i + 1])
            elif token[-2:] == 'br':
                br = extrai_parte_numerica(texto[i + 1])
        elif len(token) == 2 and token == "br":
            if i + 1 < len(texto):
                br = extrai_parte_numerica(texto[i + 1])

        if br != -1:
            if len(br) > 0:
                try:
                    br = int(br)
                    return br
                except ValueError:
                    print("Erro ao converter br!")
                    br = -1
                    pass
    print(f"BR não Encontrada:({tw[0]}) {tw[2]}")
    return None


def extrai_uf(tw):
    if tw[0] == '1420377510227939331':
        a = 1
    local = clean_text(tw[1])
    usuario = clean_text(tw[4])
    texto = tw[2]

    estados = list(filter(lambda x: incluso(x, usuario), ESTADOS.keys())) + list(
        filter(lambda x: incluso(x, local), ESTADOS.keys()))
    muncs = list(filter(lambda x: incluso(x, local), MUNICIPIOS.keys()))
    users = list(filter(lambda x: incluso(x, usuario), MUNICIPIOS.keys()))
    ufs = list(filter(lambda x: incluso(x, usuario), ESTADOS.values())) + list(
        filter(lambda x: incluso(x, local), ESTADOS.values()))

    if len(ufs) > 0:
        return ufs[0]
    elif len(estados) > 0:
        return ESTADOS[estados[0]]
    elif len(muncs) > 0:
        return MUNICIPIOS[muncs[0]]
    elif len(users) > 0:
        return MUNICIPIOS[users[0]]

    tokens = local.split(" ") + usuario.split(" ") + texto.split(" ")
    for token in tokens:
        if token in ESTADOS.keys():
            return ESTADOS[token]
        elif token in ESTADOS.values():
            return token
        elif token in MUNICIPIOS.keys():
            return MUNICIPIOS[token]
    return None


def extrai_ufbr(tw):
    br = extrai_br(tw)
    uf = extrai_uf(tw)
    if br is not None and uf is not None:
        return f"{uf}-{br}"
    return None


def extrai_informacoes(tw):
    return {"km_trunc": extrai_km(tw),
            "ufbr": extrai_ufbr(tw)}


tws = dataBase.getTwitters(coluns=["id", "local", "texto", "data", "usuario"], where=["classificacao='1'"])
tws_estruturados = []
for tw in tws:
    informacoes = extrai_informacoes(tw)
    informacoes['id'] = tw[0]
    tws_estruturados += [informacoes]
