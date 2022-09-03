from bson import ObjectId
from pymongo import MongoClient
import ssl


muted_individuals = {}
try:

    cluster = MongoClient("mongodb+srv://Chinggis:Goshonia@cluster0.hmojs.mongodb.net/test")
    print("Connected successfully!!!")
    db = cluster["UserData"]
    collection = db["UserData"]

except:
    print("Could not connect to MongoDB")


def save():
    print("Saving. . .")
    replacement_muted_individual = {}
    for user in muted_individuals:
        replacement_muted_individual[str(user.id)] = [str(g) for g in muted_individuals[user]]
        print(replacement_muted_individual)
    collection.replace_one({'_id': ObjectId('60a4286ff0d244eb0933c58b')}, replacement_muted_individual)
    print("Saved!")