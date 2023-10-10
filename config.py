import os
from  dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_PASS")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

class JWT:
    ALGORITHM = "HS256"
    EXPIRY = 60 * 60 #60 * 60 * 24
    SECRET = "my-32-character-ultra-secure-and-ultra-long-secret"

class Database:
    MODULES = ['db.users', 'db.partners', 'db.ml_models']
    
    #local postgres 
    # CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
    
    # CONNECTION_STRING = f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    #local in render
    CONNECTION_STRING = "postgres://sohibjon:nNI0w7YH1saKTjyLi5i3jzI4E41hwRCo@dpg-ck1ghhmru70s73dhe5u0-a/lucid_tvrn"
    
    #global postgres db render
    # CONNECTION_STRING ="postgres://sohibjon:nNI0w7YH1saKTjyLi5i3jzI4E41hwRCo@dpg-ck1ghhmru70s73dhe5u0-a.oregon-postgres.render.com/lucid_tvrn"
class AzureStorage:
    CONNECTION_STR = "DefaultEndpointsProtocol=https;AccountName=zyplstorage;AccountKey=SJQqgSxLubqJF5/zMesYG6rnRHpVb1FDPWfqXe7cjnc3PDtRlJHzzBCYJJfYxRMS+N3gybqSQi6L+AStHMqV5g==;EndpointSuffix=core.windows.net"
