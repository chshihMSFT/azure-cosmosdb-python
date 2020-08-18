# --------------------------------------------------------------------------------
# azure-cosmosdb-table 1.0.6
# Python SDK for 
#       Blob Storage - Table Service (i.e. Azure Table Storage)
#       Cosmos DB Table API
# --------------------------------------------------------------------------------
#  Service:     https://docs.microsoft.com/en-us/azure/cosmos-db/table-introduction
#  SDK:         https://pypi.org/project/azure-cosmosdb-table/
#  API Doc:     https://docs.microsoft.com/en-us/python/api/azure-cosmosdb-table/?view=azure-python
# --------------------------------------------------------------------------------

# Demo 1:
from azure.cosmosdb.table import TableService
from azure.cosmosdb.table.models import Entity

tablename = 'tasktable'
task = {'PartitionKey': 'tasksSeattle', 'RowKey': '001',
        'description': 'Take out the trash', 'priority': 200}

#Blob Storage - Table Service
print("Demo / Blob Storage - Table Service ... Start")
Blob_table_service = TableService(account_name='BlobStorageAccountName', account_key='BlobStorageAccountKey')
Blob_table_service.create_table(tablename)
Blob_table_service.insert_entity(tablename, task)
# get_table_service_stats()
# Retrieves statistics related to replication for the Table service. 
# IMPORTANT NOTE:
# It is only available when read-access geo-redundant replication is enabled for the storage account.
# ref: https://docs.microsoft.com/en-us/python/api/azure-cosmosdb-table/azure.cosmosdb.table.tableservice.tableservice?view=azure-python#get-table-service-stats-timeout-none-
Blob_table_service.get_table_service_stats()
print("Demo / Blob Storage - Table Service ... End")

#Cosmos DB - Table API
print("Demo / Cosmos DB - Table API ... Start")
connstring='DefaultEndpointsProtocol=https;AccountName=CosmosDBAccountName;AccountKey=CosmosDBAccountKey;TableEndpoint=https://CosmosDBAccountName.table.cosmos.azure.com:443/;'
Cosmos_table_service = TableService(endpoint_suffix = "table.cosmos.azure.com", connection_string = connstring)
Cosmos_table_service.create_table(tablename)
Cosmos_table_service.insert_entity(tablename, task)
print("Demo / Cosmos DB - Table API ... End")


# --------------------------------------------------------------------------------
# azure-cosmos 4.1.0
# Python SDK for 
#       Cosmos DB SQL API
# --------------------------------------------------------------------------------
#  Service:     https://docs.microsoft.com/azure/cosmos-db/
#  SDK:         https://pypi.org/project/azure-cosmos/
#  API Doc:     https://docs.microsoft.com/en-us/python/api/azure-cosmos/
#  Example:     https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/cosmos/azure-cosmos/samples
# --------------------------------------------------------------------------------

# Demo 2:
from azure.cosmos import exceptions, CosmosClient, PartitionKey

#Cosmos DB - SQL API
print("Demo / Cosmos DB - SQL API ... Start")
client = CosmosClient('https://CosmosDBAccountName.documents.azure.com:443/',  'CosmosDBAccountKey')
database = client.create_database_if_not_exists("testdb", offer_throughput=400)
container1 = database.create_container_if_not_exists(id="cont1", partition_key=PartitionKey(path="/pk"))
container2 = database.create_container_if_not_exists(id="cont2", partition_key=PartitionKey(path="/pk"))

for x in client.list_databases():
    print (x)
    print("collection : ")
    for y in database.list_containers():
        print (y)

for i in range(1, 10):
    container1.upsert_item({
            'id': 'item{0}'.format(i),
            'productName': 'Widget',
            'productModel': 'Model {0}'.format(i),
            'pk': 'test'
        }
    )

print("Demo / Cosmos DB - SQL API ... End")
