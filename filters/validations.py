import re
from unicodedata import normalize

def validate_regiao(regiao: str):
    list_regioes = ["no", "ne", "co", "se", "su"]
    lowercase_regiao = regiao.lower()
    sliced_regiao = lowercase_regiao[slice(2)]
    if sliced_regiao in list_regioes:
        return sliced_regiao
    return None


def validate_uf(uf: str):
    list_uf = [
        "ac",
        "al",
        "ap",
        "am",
        "ba",
        "ce",
        "df",
        "es",
        "go",
        "ma",
        "mt",
        "ms",
        "mg",
        "pa",
        "pb",
        "pr",
        "pe",
        "pi",
        "rj",
        "rn",
        "rs",
        "ro",
        "rr",
        "sc",
        "sp",
        "se",
        "to"
    ]
    lowercase_uf = uf.lower()
    sliced_uf = lowercase_uf[slice(2)]
    if sliced_uf in list_uf:
        return sliced_uf
    return None


def validate_municipio(municipio: str):
    normalized_municipio = normalize('NFKD', municipio).encode('ASCII', 'ignore').decode('ASCII')
    joined_municipio = normalized_municipio.replace(" ", "")
    lowercase_municipio = joined_municipio.lower()
    return lowercase_municipio


def validate_crime(crime: str):
    num_crime = int(crime) if crime.isnumeric() else 0
    if 1 <= num_crime <= 9:
        return num_crime
    return None


def validate_ano(ano: str):
    list_anos = ano.split("-")
    pattern = "^\d{4}$"
    mapped_lista_anos = map(
        lambda lista: check_if_matches(lista, pattern), list_anos
    )
    validated_list = list(filter(None, mapped_lista_anos))

    if len(validated_list) >= 1:
        sliced_list = validated_list[slice(2)]
        if len(validated_list) > 1:
            if sliced_list[0] > sliced_list[1] or 0:
                sliced_list.reverse()
        return sliced_list
    return None


def validate_mes(mes: str):
    list_meses = [
        "jan",
        "fev",
        "mar",
        "abr",
        "mai",
        "jun",
        "jul",
        "ago",
        "set",
        "out",
        "nov",
        "dez",
    ]
    meses = mes.split("-")
    pattern = "^[a-z]{3}$"
    mapped_lista_meses = map(
        lambda lista: check_if_matches(lista, pattern), meses
    )
    validated_list = list(filter(None, mapped_lista_meses))
    if len(validated_list) >= 1:
        sliced_list = validated_list[slice(2)]
        if len(validated_list) > 1:
            index_mes_inicial = list_meses.index(sliced_list[0])
            index_mes_final = (list_meses.index(sliced_list[1]))
            if index_mes_inicial > index_mes_final:
                aux = index_mes_inicial
                index_mes_inicial = index_mes_final
                index_mes_final = aux
            index_mes_final += 1
            sliced_list = list_meses[slice(index_mes_inicial, index_mes_final)]
        return sliced_list
    return None

def check_if_matches(value: str, reg_exp: str):
    expression = re.compile(reg_exp)
    test = expression.search(value)
    if test is not None:
        return test.group(0)
    return None
