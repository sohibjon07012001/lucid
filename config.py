import os
from  dotenv import load_dotenv

load_dotenv()


class JWT:
    ALGORITHM = "HS256"
    EXPIRY = 60 * 60 * 24
    SECRET = "my-32-character-ultra-secure-and-ultra-long-secret"

class Database:
    MODULES = ['db.users', 'db.partners']
    CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")


class AzureStorage:
    CONNECTION_STR = "DefaultEndpointsProtocol=https;AccountName=zyplstorage;AccountKey=SJQqgSxLubqJF5/zMesYG6rnRHpVb1FDPWfqXe7cjnc3PDtRlJHzzBCYJJfYxRMS+N3gybqSQi6L+AStHMqV5g==;EndpointSuffix=core.windows.net"
