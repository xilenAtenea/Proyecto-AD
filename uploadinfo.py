#Subiendo informacion de las universidades a la coleccion de mongo "universitys"
from pymongo import MongoClient
import pandas as pd

myclient = MongoClient("mongodb://localhost:27017/")

db = myclient["Enikio"]

#Coleccion para universidades:
collection1 = db["universitys"]

#Subiendo informacion de las universidades a la coleccion de mongo "universitys"
mylist = [
{ "nombre": "Universidad Autónoma de Occidente" , "location": {'type': 'Point', 'coordinates': [-76.52048592608172, 3.353740400019329]}},
{ "nombre": "Universidad ICESI", "location": {'type': 'Point', 'coordinates': [-76.53094179612705, 3.3416907213039626]}},
{ "nombre": "Institución universitaria Antonio José Camacho", "location": {'type': 'Point', 'coordinates': [-76.52747705971524, 3.470593445052489]}},
{ "nombre": "Universidad de San Buenaventura Cali", "location": {'type': 'Point', 'coordinates': [-76.54438216439318, 3.343562195183882]}},
{ "nombre": "Universidad Libre (Sede San Fernando)", "location": {'type': 'Point', 'coordinates': [-76.54992013164862, 3.427567009699586]}},
{ "nombre": "Universidad Cooperativa de Colombia", "location": {'type': 'Point', 'coordinates': [-76.55105966842426, 3.391257975610888]}},

]

#collection1.insert_many(mylist)


#coleccion para partamentos:
collection2 = db['apartments']

#Subiendo informacion de los apartamentos a la coleccion de mongo "apartments"
df = pd.read_csv(r"C:\Users\xilen\OneDrive\Escritorio\AD_db\codesProyecto\informacion_apartamentitos.csv") 
records = df.to_dict(orient = 'records')  


for i in records:
    locationes = {'type': 'Point',
    'coordinates': [i[' longitud'], i[' latitud']]
    }
    i['location']= locationes
    del i[' latitud']
    del i[' longitud']

#collection2.insert_many(records)



#Queries:

uni = input ("Ingrese su universidad: ")
cursor = collection1.find({"nombre": uni}, {"_id": 0, "location": {"coordinates": 1}})

#Sacar solo coordenadas de la universidad escojida:
for i in cursor:
#{'location': {'coordinates': [-76.52048592608172, 3.353740400019329]}}
    coor = i["location"]["coordinates"]
    

#Query de los aptos cercanos a las coordenadas que se sacaron:
query= {"location":{"$nearSphere": {
     "$geometry": {
        "type" : "Point",
        "coordinates" : coor } } } }

print (f"Los apartamentos más cercanos a {uni} son:")
cursor = collection2.find(query).limit(5)
for i in cursor:
    print(i)
