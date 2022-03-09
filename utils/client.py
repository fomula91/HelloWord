from pymongo import MongoClient
from utils.env import MONGO_URI
from utils.env import TLS_CA_FILE

client = MongoClient(MONGO_URI, tlsCAFile=TLS_CA_FILE)
db = client.dbsparta
