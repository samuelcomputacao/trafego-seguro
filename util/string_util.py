import re

def replace(text, entry=[], exit=''):
    for caracter in entry:
        text = text.replace(caracter, exit)
    return text


def remove_emogi(text):
    base = 'abcdefghijklmnopqrstuvwxyz- 1234567890'
    result = ''
    for caractere in text:
        if caractere in base:
            result += caractere
    return result

def clean_caracteres(text):
    text = replace(text, 'á|à|ã|ä|â'.split("|"), 'a')
    text = replace(text, 'é|è|ë|ê'.split("|"), 'e')
    text = replace(text, 'í|ì|ï|î'.split("|"), 'i')
    text = replace(text, 'ó|ò|ö|ô'.split("|"), 'o')
    text = replace(text, 'ú|ù|ü'.split("|"), 'u')
    text = replace(text, ['ç'], 'c')
    text = replace(text, '!|?|"|*|°|º|ª|§|)|(|]|[|{|}'.split("|"), '')
    text = replace(text, '"', '')
    text = replace(text, "'", '')
    text = replace(text, '|', '')
    text = replace(text, "|\\|]|[|=|+|)|(|&|%|$|#|!|{|}", '')
    text = replace(text, '\n|\t|\a|\b|\f|\r|-|_|/'.split("|"), ' ')
    return remove_emogi(text)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'RT+', '', text)
    text = re.sub(r'@\S+', '', text)
    text = re.sub(r'https?\S+', '', text)
    text = re.sub(r'http?\S+', '', text)
    return clean_caracteres(text)

def incluso(texto1, texto2):
    # if texto2=='campo largo':
    #     print(1)
    index = -1
    try:
        index = texto2.index(texto1)
    except ValueError:
        pass
    if index != -1:
        if index + len(texto1) == len(texto2):
            if index == 0 or texto2[index - 1] == ' ':
                return True
        elif texto2[index + len(texto1)] == ' ':
            if index == 0 or texto2[index - 1] == ' ':
                return True
    return False
