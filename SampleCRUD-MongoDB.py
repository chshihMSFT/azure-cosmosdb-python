# --------------------------------------------------------------------------------
# pymongo 3.11.1
# Python SDK for
#       Cosmos DB's API for MongoDB
# --------------------------------------------------------------------------------
#  Service:     https://docs.microsoft.com/en-us/azure/cosmos-db/mongodb-introduction
#  SDK:         https://pypi.org/project/pymongo/
#  API Doc:     https://pymongo.readthedocs.io/en/stable/
#  Example:     https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/cosmos/azure-cosmos/samples
# --------------------------------------------------------------------------------

import pymongo
from pymongo import MongoClient
import datetime

#Cosmos DB - MongoDB API v3.6
print("Demo / Cosmos DB - MongoDB API ... Start")
CosmosDBAccountName = "CosmosDBAccountName"
CosmosDBAccountKey = "CosmosDBAccountKey"

uri = "mongodb://" + CosmosDBAccountName + ":" + CosmosDBAccountKey + "@" + CosmosDBAccountName + ".mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@" + CosmosDBAccountKey + "@"
client = pymongo.MongoClient(uri)
db = client.testdb
collection = db.testcollection

print("Inserting a Document ...")
post = {"author": "Mike",
         "text": "My first blog post!",
         "tags": ["mongodb", "python", "pymongo"],
         "myshardkey": "demo001",
         "date": datetime.datetime.utcnow()}
post_id = collection.insert_one(post).inserted_id
print(post_id)

print("Getting a Single Document ...")
print(collection.find_one({"_id":post_id}))

print("Demo / Cosmos DB - MongoDB API ... End")
