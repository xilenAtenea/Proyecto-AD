from pymongo import MongoClient


def DBconnection():
    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient["Enikio"]
    collection3 = db["infoArrendadores"]

    return db