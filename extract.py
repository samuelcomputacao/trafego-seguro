
from re import  findall
from datetime import datetime
from util.date_util import get_date_timezone, FORMAT_DATE
from dataBase import DataBase
from util.string_util import clean_text, incluso
from functools import cmp_to_key


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
        else: flag = True
    return retorno


def extrai_km(tw):
    texto = tw[2]
    tokens = findall(r'km[s]*[ ]*\d+', texto)
    if len(tokens) > 0:
        km = extrai_parte_numerica(tokens[0][::-1])[::-1]
        if len(km) > 0:
             try:
                 int(km)
                 return km
             except ValueError:
                 print("Erro ao converter km!")
                 pass
    return None


def extrai_br(tw, prefixo):
    texto = tw[2]
    tokens = findall(r'%s[ ]*\d+' % prefixo, texto)
    if len(tokens) > 0:
        br = extrai_parte_numerica(tokens[0][::-1])[::-1]
        if len(br) > 0:
            try:
                int(br)
                return br
            except ValueError:
                print("Erro ao converter br!")
    return None

def sizeComp(x,y):
    return len(y) - len(x)

def extrai_uf(tw):
    local = clean_text(tw[1])
    usuario = clean_text(tw[4])
    texto = tw[2]

    estados = sorted(list(filter(lambda x: incluso(x, usuario), ESTADOS.keys())) + list(filter(lambda x: incluso(x, local), ESTADOS.keys())), key=cmp_to_key(sizeComp))
    muncs = sorted(list(filter(lambda x: incluso(x, usuario), MUNICIPIOS.keys())) + list(filter(lambda x: incluso(x, local), MUNICIPIOS.keys())), key=cmp_to_key(sizeComp))
    ufs = list(filter(lambda x: incluso(x, usuario), ESTADOS.values())) + list(
        filter(lambda x: incluso(x, local), ESTADOS.values()))

    if len(ufs) > 0:
        return ufs[0]
    elif len(estados) > 0:
        return ESTADOS[estados[0]]
    elif len(muncs) > 0:
        return MUNICIPIOS[muncs[0]]

    print(MUNICIPIOS['curitiba'])
    # tokens = local.split(" ") + usuario.split(" ") + texto.split(" ")
    # for token in tokens:
    #     if token in ESTADOS.keys():
    #         return ESTADOS[token]
    #     elif token in ESTADOS.values():
    #         return token
    #     elif token in MUNICIPIOS.keys():
    #         return MUNICIPIOS[token]
    return None


def extrai_ufbr(tw):
    uf = extrai_uf(tw)
    br = extrai_br(tw, 'br')
    if br is None and uf is not None:
        br = extrai_br(tw, uf)
    if br is not None and uf is not None:
        return f"{uf}-{br}"
    return None


def extrai_dia_semana_num(tw):
    if tw[3] is not None:
        data = datetime.strptime(tw[3], FORMAT_DATE)
        return str(data.weekday())
    return None


def extrai_turno_simples(tw):
    if tw[3] is not None:
        data = datetime.strptime(tw[3], FORMAT_DATE)
        hora = data.hour
        if hora < 12:
            return "0"
        else:
            return "1"
    return None


def extrai_tipo_acidente_simples(tw):
    texto = tw[2]
    if len(list(filter(lambda x: incluso(x, texto),
                       ["saida de pista", "capotamento", "tombamento", "derramamento de carga"]))) > 0:
        return "2"
    elif len(list(filter(lambda x: incluso(x, texto),
                         ["queda de ocupante de veiculo", "colisao", "engavetamento", "atropelamento de animal",
                          "queda de motocicleta", "queda de bicicleta", "queda de veiculo",
                          "atropelamento de pessoa"]))) > 0:
        return "1"
    else:
        return "0"


def extrai_classe(tw):
    texto = tw[2]
    if len(list(filter(lambda x: incluso(x, texto),
                       ["morte", "mortes", "ferido", "feridos", "ferida", "feridas", "morreu", "morreram", "faleceu",
                        "faleceram"]))) == 0:
        return "0"
    return "1"


def extrai_tipo_pista_simples(ufbr, km):
    uf, br = ufbr.split("-")
    legenda = dataBase.getRodoviasFederais(coluns=['leg_multim'],
                                           where=[f"vl_br='{br}'", f"sg_uf='{uf.upper()}'", f"vl_km_inic<={km}",
                                                  f"vl_km_fina>={km}"])
    if len(legenda) > 0:
        legenda = legenda[0][0]
        if len(list(filter(lambda x: x in legenda.lower(),
                           ["dupl", "múlt"]))) > 0:
            return "1"
        else:
            return "0"
    else:
        return None


def extrai_informacoes_full(tw):
    ufbr = extrai_ufbr(tw)
    km = extrai_km(tw)
    if ufbr is not None and km is not None:
        return {"km_trunc": km,
                "id": tw[0],
                "ufbr": ufbr,
                "dia_semana_num": extrai_dia_semana_num(tw),
                "turno_simples": extrai_turno_simples(tw),
                "tipo_pista_simples": extrai_tipo_pista_simples(ufbr, km),
                "categoria_sentido_via": "0",
                "tracado_via_simples": "0",
                "condicao_metereologica_simples": "0",
                "tipo_acidente_simples": extrai_tipo_acidente_simples(tw),
                "classe": extrai_classe(tw)}
    return None

def extrai_informacoes_basic(tw):
    if tw[0] == 1437426853896245251:
       a = 1
    ufbr = extrai_ufbr(tw)
    km = extrai_km(tw)
    if ufbr is not None and km is not None:
        return {"km_trunc": km,
                "id": tw[0],
                "ufbr": ufbr}
    return None


def valida_tw(tw):
    for key in tw.keys():
        if tw[key] is None:
            return False
    return True

def not_valida_tw(tw):
    return not valida_tw(tw)


tws = dataBase.getTwitters(coluns=["id", "local", "texto", "data", "usuario"], where=["classificacao='1'"])

tws_estruturados = []
tws_problemas = []
for tw in tws:
    informacoes = extrai_informacoes_basic(tw)
    if informacoes is not None:
        informacoes['id'] = tw[0]
        tws_estruturados += [informacoes]
    else:
        tws_problemas += [tw]
        print(tw)
lista = list(filter(valida_tw, tws_estruturados))
print("%i e %i" %(len(tws_estruturados), len(tws_problemas)))
#dataBase.salvarClassificacao(list(filter(valida_tw, tws_estruturados)))
