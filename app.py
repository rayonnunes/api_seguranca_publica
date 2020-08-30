import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
from flask import request
from flask import json
from bson.json_util import dumps
import pymongo
from filters.get_filter import get_ano, get_mes, get_crime, get_uf, get_regiao, get_municipio

app = Flask(__name__)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


# ano - {$and : [{ano: {$gte: "2017"}}, {ano: {$lte: "2018"}}]}
# crime - {crime: <"1"-"9">}
# mes - {mes: {$in: ["mar", "abr", "mai"]}}
# municipio - {municipio: "nomedomunicipio"}
# regiao - {regiao: <"no", "ne", "co", "se", "su">}
# uf - {uf: <"ac","al","ap","am","ba","ce","df","es","go","ma","mt","ms","mg","pa","pb","pr","pe","pi","rj","rn","rs","ro","rr","sc","sp","se","to">}

# exemplo:
# {
#   $and : [{ano: {$gte: "2017"}}, {ano: {$lte: "2018"}}],
#   crime: "4",
#   mes: {$in: ["jan", "fev", "mar"]},
#   municipio: "saobenedito",
#   uf: "ce",
#   regiao: "ne"
# }

@app.route('/')
def get_home():
    return app.response_class(
        response=json.dumps({
            "message": "Hello World"
        }),
        status=200,
        mimetype='application/json'
    )


@app.route('/api')
def get_registros():
    data = {
        "ano": request.args.get('ano'),
        "crime": request.args.get('crime'),
        "mes": request.args.get('mes'),
        "municipio": request.args.get('municipio'),
        "regiao": request.args.get('regiao'),
        "uf": request.args.get('uf'),
    }
    mongo_uri = os.environ.get("MONGO_URI")
    client = pymongo.MongoClient(mongo_uri)
    db = client.base_sinesp
    collection = db.registros

    query_filters = {
        "ano": get_ano(data["ano"]),
        "mes": get_mes(data["mes"]),
        "crime": get_crime(data["crime"]),
        "municipio": get_municipio(data["municipio"]),
        "regiao": get_regiao(data["regiao"]),
        "uf": get_uf(data["uf"]),
    }

    result = []
    for query in collection.find(query_filters):
        result.append(query)

    response = app.response_class(
        response=dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run()
