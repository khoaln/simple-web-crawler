import unittest
import pymongo

class BaseDBTest(unittest.TestCase):
  mongo_uri = '127.0.0.1'
  mongo_db = 'test'

  def setUp(self):
    client = pymongo.MongoClient(self.mongo_uri)
    db = client[self.mongo_db]
    # Drop all collections in test DB before running each testcase
    for collection_name in db.list_collection_names():
      db[collection_name].drop()

    client.close()
