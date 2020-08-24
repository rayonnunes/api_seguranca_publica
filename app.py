import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask
from flask import request
from flask import json
import pymongo

app = Flask(__name__)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/ocorrencias')
def hello_ocorrencias():
    MONGO_URI = os.environ.get("MONGO_URI")
    client = pymongo.MongoClient(MONGO_URI)
    db = client.ocorrencias
    collection = db.indicadores
    result = collection.find_one({"UF": "Ceará"})
    print(result)

    for crime in collection.find({"UF": "Ceará"}):
        print(crime)

    data = {
        "tabela": 'ocorrencias',
        "uf": request.args.get('uf'),
        "tipo": request.args.get('tipo'),
        "ano": request.args.get('ano'),
        "mes": request.args.get('mes')
    }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/vitimas')
def hello_vitimas():
    data = {
        "tabela": 'vitimas',
        "uf": request.args.get('uf'),
        "tipo": request.args.get('tipo'),
        "ano": request.args.get('ano'),
        "mes": request.args.get('mes')
    }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run()
