from .validations import validate_ano, validate_crime, validate_mes, validate_municipio, validate_regiao, validate_uf

def get_regiao(regiao: str):
    validated_regiao = validate_regiao(regiao)
    if validated_regiao is not None:
        return {"regiao": validated_regiao}
    return None


def get_uf(uf: str):
    validated_uf = validate_uf(uf)
    if validated_uf is not None:
        return {"uf": validated_uf}
    return None


def get_municipio(municipio: str):
    validated_municipio = validate_municipio(municipio)
    if validated_municipio is not None:
        return {"municipio": validated_municipio}
    return None


def get_crime(crime: str):
    validated_crime = validate_crime(crime)
    if validated_crime is not None:
        return {"crime": crime}
    return None


def get_ano(ano: str):
    validated_ano = validate_ano(ano)
    if validated_ano is not None:
        if len(validated_ano) > 1:
            return {"$and": [{"ano": {"$gte": str(validated_ano[0])}}, {"ano": {"$lte": str(validated_ano[1])}}]}
        return {"ano": ano}
    return None


def get_mes(mes: str):
    validated_mes = validate_mes(mes)
    if validated_mes is not None:
        return {"mes": {"$in": validated_mes}}
    return None
