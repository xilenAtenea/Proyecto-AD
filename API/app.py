from flask import Flask, request, jsonify, render_template, url_for, redirect
import pymongo
from pymongo import MongoClient
import pandas as pd
import database_login as dbase
from user import Signup
from uploadinfo_query import infouni
import folium

db= dbase.DBconnection()


app = Flask(__name__)
app.config["DEBUG"] = True

#Principal
@app.route("/", methods=["GET"])
def home_page():
    return render_template('index.html')

@app.route("/inicio", methods=["GET", "POST"])
def inicio():
    return render_template('docs3.html')

#Buscar aptos
@app.route('/aptos', methods=['GET'])
def api_root():
    return render_template('docs2.html', data = [{ "nombre": "Universidad Autónoma de Occidente" }, { "nombre": "Universidad ICESI"},{ "nombre": "Institución universitaria Antonio José Camacho"},{ "nombre": "Universidad de San Buenaventura Cali"},{ "nombre": "Universidad Libre (Sede San Fernando)"},{ "nombre": "Universidad Cooperativa de Colombia"}])



#Arrendador. Inicio de sesion/crear sesion
@app.route('/inicio/datos', methods=['POST'])
def user():
        collection3 = db['infoArrendadores']
        #name = request.form['name']
        #email = request.form['email']
        #password= request.form['password']

        dbname = collection3.find_one({'name': request.form['name']})
        dbemail = collection3.find_one({'email': request.form['email']})
        dbpassword = collection3.find_one({'password': request.form['password']})

        if dbname and dbemail and dbpassword:
            return redirect(url_for('api_mongo_find'))

        else:
            return 'Usuario no reconocido. Inténtelo de nuevo.'
        




#Con esto se ve que si sale el valor que se seleccione en el docs2
@app.route('/valor', methods=['GET', 'POST'])
def valor():
    select = request.form.get("comp_select")
    coor, coordenadas = infouni(str(select))
    mapa = map(coor, coordenadas)

    print(type(coordenadas))

    return mapa
    



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

def map(coords, coordenadas):
    start_coords = [ coords[1], coords[0] ]
    
    folium_map = folium.Map(location=start_coords, zoom_start=15)
     
    folium.CircleMarker(start_coords,     
                        radius=2, weight=5,
                        color='red').add_to(folium_map)
    folium.LayerControl().add_to(folium_map)

    for i in coordenadas:

        folium.Marker(location= [i["location"]["coordinates"][1], i["location"]["coordinates"][0]]).add_to(folium_map)
        folium.LayerControl().add_to(folium_map)



    return folium_map._repr_html_()


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
    for i in col.find(query, {'_id': 0}):
        find_result.append(i)
    return str(find_result)


def mongo_insert_one(doc):
    #doc
    _, col = create_mongo_session('Enikio', 'infoPostulados')
    col.insert_one(doc)

def mongo_insert_one2(doc):
    #doc
    _, col = create_mongo_session('Enikio', 'infoArrendadores')
    col.insert_one(doc)


app.run(port=35081)