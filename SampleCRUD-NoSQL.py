# --------------------------------------------------------------------------------
# azure-cosmos 4.5.1
# Python SDK for
#       Cosmos DB SQL API
# --------------------------------------------------------------------------------
#  Service:     https://docs.microsoft.com/azure/cosmos-db/
#  SDK:         https://pypi.org/project/azure-cosmos/
#  API Doc:     https://docs.microsoft.com/en-us/python/api/azure-cosmos/
#  Example:     https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-python-samples
# --------------------------------------------------------------------------------

from azure.cosmos import exceptions, CosmosClient, PartitionKey, diagnostics
import datetime, time
import json
import uuid
import random

dbName = "dbName"
collName = "collectionName"
category = "demo_Python"
task = {'id': 'doc001', 'category': category, 'name': 'names',
        'description': 'descriptions',
        'isComplete': True,
        'createTimestamp': '2000-01-01',
        'priority': 1} #default values, will be replaced in runtime. 
intervalTimeinSec = 3

client = CosmosClient('https://CosmosDBAccountName.documents.azure.com:443/',  'CosmosDBAccountKey')
database = client.create_database_if_not_exists(dbName, offer_throughput=400)
container = database.create_container_if_not_exists(id=collName, partition_key=PartitionKey(path="/category"))

try:
    while True:        
        task['id'] = str(uuid.uuid4())
        task['category'] = category
        task['name'] = str(uuid.uuid4())
        task['description'] = str(uuid.uuid4())        
        task['createTimestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        task['priority'] = random.randint(1, 9)

        #Insert document
        resultInsert = container.create_item(task)
        responseHeaders = container.client_connection.last_response_headers
        print("[" + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "] ... create_item task {id:" + resultInsert['id'] + ", category:" + resultInsert['category'] + "}, ActivityId:" + responseHeaders['x-ms-activity-id'] +", consumed: " + responseHeaders['x-ms-request-charge'] + " RUs" )
        time.sleep(intervalTimeinSec) #sec

        #Read document
        resultRead = container.read_item(item=task['id'], partition_key=task['category'])
        responseHeaders = container.client_connection.last_response_headers
        print("[" + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "] ... read_item   task {id:" + resultRead['id'] + ", category:" + resultRead['category'] + "}, ActivityId:" + responseHeaders['x-ms-activity-id'] +", consumed: " + responseHeaders['x-ms-request-charge'] + " RUs" )
        time.sleep(intervalTimeinSec) #sec

        #Query document
        query = "SELECT * FROM c WHERE c.category=@category and c.id=@id"
        items = list(container.query_items(
            query=query,
            parameters=[
                {"name": "@category", "value": task['category']},
                {"name": "@id", "value": task['id']}
            ],
            max_item_count=-1,
            enable_cross_partition_query=True,
            populate_query_metrics=True
        ))
        responseHeaders = container.client_connection.last_response_headers
        query_metrics = str(responseHeaders['x-ms-documentdb-query-metrics']).split(';')
        print("[" + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "] ... query_items")
        for item in items:
            print("[" + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "] ... task {id:" + item['id'] + ", category:" + item['category'] + "}, ActivityId:" + responseHeaders['x-ms-activity-id'] +", consumed: " + responseHeaders['x-ms-request-charge'] + " RUs" )
        
        print("[" + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "] ... query_metrics")
        for prop in query_metrics:
            print("[" + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "]     " + prop)
        time.sleep(intervalTimeinSec) #sec

        #Delete document
        resultDelete = container.delete_item(item=task['id'], partition_key=task['category'])
        responseHeaders = container.client_connection.last_response_headers
        print("[" + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "] ... delete_item task {id:" + task['id'] + ", category:" + task['category'] + "}, ActivityId:" + responseHeaders['x-ms-activity-id'] +", consumed: " + responseHeaders['x-ms-request-charge'] + " RUs" )
        time.sleep(intervalTimeinSec) #sec

except Exception as e:
    print("Error occurred, need to check further")

finally:
    print("Finished")
