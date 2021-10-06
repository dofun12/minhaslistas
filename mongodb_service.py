import re

from pymongo import MongoClient
from pprint import pprint
import json
from bson import json_util
import uuid


class MongoDBService:
    client: MongoClient
    db = None

    def sanitize(self, object):
        return json.loads(json_util.dumps(object))

    def init_connection(self):
        self.client = MongoClient(host="localhost", port=27017, username="root", password="example")
        self.db = self.client['workshop']

    def __init__(self):
        pass

    def create_list(self, list_name):
        self.init_connection()
        filter = {"list_name": list_name}
        collection = self.db['lists']
        items = list(collection.find(filter))
        if items is None or len(items) == 0:
            collection.insert_one({"list_name": list_name})
            self.client.close()
            return
        collection.update_one(filter, {"$set": {"list_name": list_name}})
        self.client.close()

    def add_list_item(self, list_name, item_value):
        self.init_connection()
        list_item = {"id": str(uuid.uuid4()), "value": item_value.value}
        filter = {"list_name": list_name}
        collection = self.db['lists']
        items = list(collection.find(filter))
        if items is None or len(items) == 0:
            val = {"list_name": list_name, "list_items": [list_item]}
            collection.insert_one(self.sanitize(val))
            self.client.close()
            return
        collection.update_one(filter, {"$push": {"list_items": self.sanitize(list_item)}})
        self.client.close()

    def list(self):
        self.init_connection()
        cursor = self.db['lists'].find({})
        list_items = list(cursor)
        self.client.close()
        return list_items

    def cleanJson(self, text: str):
        replaced = text.replace("\"", "")
        cleaned = re.sub(r'^"|"$', '', replaced)
        return cleaned

    def list_by_name(self, list_name):
        self.init_connection()
        cursor = self.db['lists'].find({"list_name": list_name})
        list_items = list(cursor)
        self.client.close()
        return list_items
