import configparser
import certifi
import os

env = configparser.ConfigParser()
env.read(os.getcwd() + os.sep + 'config.ini', encoding='utf-8')

SECRET_KEY = env['FLASK_SECRET_KEY']['KEY']
MONGO_URI = env['DB_CONFIG']['URI']
TLS_CA_FILE = certifi.where()
