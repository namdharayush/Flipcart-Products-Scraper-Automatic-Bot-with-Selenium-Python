import pymongo
from datetime import datetime
class Flipcart_Mongo:
    def __init__(self):
        self.create_connections()
        self.create_unique_index()

    def create_connections(self):
        self.mongo_url = 'mongodb://localhost:27017/'
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client['flipcart']
        self.collection = self.db['products']

    def insert_data(self,data):
        data['created_at'] = datetime.now()
        data['status'] = "PENDING"
        insert_result = self.collection.insert_one(data)
        return insert_result.inserted_id

    def create_unique_index(self):
        self.collection.create_index([('product_link', pymongo.ASCENDING)], unique=True)
