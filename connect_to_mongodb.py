
from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://estate1.fosbavf.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='certs/svc_001.pem',
                     server_api=ServerApi('1'))

db = client['real_estate_monitoring']
collection = db['properties']
doc_count = collection.count_documents({})
print(doc_count)

