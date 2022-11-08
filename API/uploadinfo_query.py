##Subiendo informacion de las universidades a la coleccion de mongo "universitys"
from pymongo import MongoClient
import pandas as pd

myclient = MongoClient("mongodb://localhost:27017/")

db = myclient["Enikio"]


#Coleccion para universidades:
collection1 = db["universitys"]
collection2 = db['apartments']



#Queries:
def infouni(uni):
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
    
    coordenadas = []
    for i in cursor:
        coordenadas.append(i)
        
    return (coordenadas)

if __name__ == '__main__':
    infouni()