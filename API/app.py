from flask import Flask, request, jsonify, render_template, url_for, redirect
import pymongo
from pymongo import MongoClient
import pandas as pd

myclient = MongoClient("mongodb://localhost:27017/")

db = myclient["Enikio"]
collection1 = db["universitys"]
collection2 = db['apartments']

app = Flask(__name__)
app.config["DEBUG"] = True

#Principal
@app.route("/", methods=["GET"])
def home_page():
    return render_template('index.html')

#Buscar aptos
@app.route('/aptos', methods=['GET'])
def api_root():
    return render_template('docs2.html', data = [{ "nombre": "Universidad Autónoma de Occidente" }, { "nombre": "Universidad ICESI"},{ "nombre": "Institución universitaria Antonio José Camacho"},
{ "nombre": "Universidad de San Buenaventura Cali"},
{ "nombre": "Universidad Libre (Sede San Fernando)"},
{ "nombre": "Universidad Cooperativa de Colombia"}])

#Arrendador. Inicio de sesion/crear sesion
@app.route('/inicio', methods=['GET'])
def api_root2():
    return render_template('docs3.html')

@app.route('/aptos/valor', methods=['GET', 'POST'])
def valor():
    select = request.form.get('comp_select')
    return(str(select)) 

"""
#Para buscar todos, no lo estamos usando.
@app.route('/api/v2/mongo/find/all', methods=['GET'])
def api_mongo_find_all():
    return mongo_find({}) 
"""

#Luego de haber iniciado sesion, para buscar con su idApto
@app.route('/inicio/postulados', methods=['GET', 'POST'])
def api_mongo_find():
    if request.method == 'GET':
        return render_template('query.html')
    elif request.method == 'POST':
        data = parse_form()
        return mongo_find(data)




@app.route('/aptos/formulario', methods=['GET', 'POST'])
def api_mongo_insert():
    if request.method == 'GET':
        return render_template('mongoinsert.html')
    elif request.method == 'POST':
        data = parse_form()
        mongo_insert_one(data)
        return redirect(url_for('api_root'))


def create_mongo_session(database, collection):
    client = pymongo.MongoClient('localhost', 27017)
    db = client[database]
    col = db[collection]
    return db, col


def parse_form():
    x = {}
    d = request.form
    for key in d.keys():
        value = request.form.getlist(key)
        for val in value:
            x[key] = val
    return x

def mongo_find(query):
    _, col = create_mongo_session('Enikio', 'infoPostulados')
    find_result = []
    for i in col.find(query):
        find_result.append(i)
    return str(find_result)


def mongo_insert_one(doc):
    #doc
    _, col = create_mongo_session('Enikio', 'infoPostulados')
    col.insert_one(doc)
def mongo_insert_many(doc):
    #doc
    db, col = create_mongo_session('Enikio', 'infoPostulados')
    col.insert_many(doc)


app.run(port=35081)