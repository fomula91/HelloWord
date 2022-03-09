from pymongo import MongoClient
from utils.env import MONGO_URI
from utils.env import TLS_CA_FILE

# MongoDB 연결
client = MongoClient(MONGO_URI, tlsCAFile=TLS_CA_FILE)
db = client.dbsparta
