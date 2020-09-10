from flask import Flask
from flask import request
from bson.json_util import dumps
from connection.mongo import connect_mongo
from filters.get_filter import get_ano, get_mes, get_crime, get_uf, get_regiao, get_municipio

app = Flask(__name__)

@app.route('/')
def index():
    response_data = {
        "title": "Seja bem vindo a API de ocorrências criminais!!",
        "repositorio": "https://github.com/rayonnunes/api_seguranca_publica",
        "documentacao": "https://docs.google.com/document/d/1lVvDhZBcp_k0Hz08HF7o4nEW-oZf9l_FGSSKJEjB0Ak"
    }
    response = app.response_class(
        response=dumps(response_data, ensure_ascii=False).encode('utf8'),
        status=200,
        mimetype='application/json'
    )
    return response;

@app.route('/api')
def get_registros():
    data = {
        "regiao": request.args.get('regiao'),
        "uf": request.args.get('uf'),
        "municipio": request.args.get('municipio'),
        "crime": request.args.get('crime'),
        "ano": request.args.get('ano'),
        "mes": request.args.get('mes'),
        "page": request.args.get('page') if request.args.get('page') is not None else 1,
        "per_page": request.args.get('per_page') if (request.args.get('per_page')) is not None else 100,
    }

    query_filters = {}
    if data["regiao"] is not None:
        regiao = get_regiao(data["regiao"])
        if regiao is not None:
            query_filters.update(regiao)

    if data["uf"] is not None:
        uf = get_uf(data["uf"])
        if uf is not None:
            query_filters.update(uf)

    if data["municipio"] is not None:
        municipio = get_municipio(data["municipio"])
        if municipio is not None:
            query_filters.update(municipio)

    if data["crime"] is not None:
        crime = get_crime(data["crime"])
        if crime is not None:
            query_filters.update(crime)

    if data["ano"] is not None:
        ano = get_ano(data["ano"])
        if ano is not None:
            query_filters.update(ano)

    if data["mes"] is not None:
        mes = get_mes(data["mes"])
        if mes is not None:
            query_filters.update(mes)

    collection = connect_mongo()
    print(query_filters)
    limit = int(data["per_page"]) if int(data["per_page"]) < 1000 else 1000
    skip = int(data["per_page"]) * (int(data["page"]) - 1)
    result = {
        "page": int(data["page"]),
        "results_per_page": limit,
        "total_results": 0,
        "total_ocorrencias": 0,
        "data": []
    }
    count_results = 0
    count_ocorrencias = 0
    for query in collection.find(query_filters).skip(skip).limit(limit):
        del query["_id"]
        del query["field_0"]
        count_results += 1
        count_ocorrencias += float(query["ocorrencias"])
        result["data"].append(query)
    result["total_results"] = count_results
    result["total_ocorrencias"] = int(count_ocorrencias)
    response = app.response_class(
        response=dumps(result, ensure_ascii=False).encode('utf8'),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
   app.run(host='0.0.0.0',port=80)
