from pymongo import MongoClient
import os

class Db:
    def __init__(self, cses_client, collection_name):
        self.cses_client = cses_client

        username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
        password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

        client = MongoClient(f'mongodb://{username}:{password}@127.0.0.1:27017')
        db = client.cses
        self.users = db[collection_name]

    def add_user(self, cses_id):
        user = {
            'cses_id': cses_id,
            'tasks': self.cses_client.get_user_tasks(cses_id)
        }
        self.users.insert_one(user)

    def update_user(self, cses_id):
        try:
            user = self.users.find_one({'cses_id': cses_id})
            if (user == None):
                self.add_user(cses_id)
            else:
                new_tasks = self.cses_client.get_user_tasks(cses_id)
                self.users.update_one({'cses_id': cses_id}, {'$set': {'tasks': new_tasks}})
        except Exception as e:
            print(f"[ERROR] Failed to update user {cses_id}: {e}")
    
    def get_user_tasks(self, cses_id):
        user = self.users.find_one({'cses_id': cses_id})
        return user["tasks"]
