from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.python import to_bytes
from scrapy.utils.job import job_dir
import hashlib
import pymongo
from pymongo.errors import DuplicateKeyError
from datetime import datetime
import logging

class VisitedSiteFilter(RFPDupeFilter):
  """A filter to prevent the crawler from visiting a site twice"""

  collection_name = 'visited_sites'

  def __init__(self, debug=False, mongo_uri='127.0.0.1', mongo_db='simple_crawler'):
    self.debug = debug
    self.mongo_uri = mongo_uri
    self.mongo_db = mongo_db
    self.logger = logging.getLogger()
    self.file = None

  @classmethod
  def from_settings(cls, settings):
    debug = settings.getbool('DUPEFILTER_DEBUG')
    mongo_uri = settings.get('MONGO_URI')
    mongo_db = settings.get('MONGO_DATABASE', 'simple_crawler')
    return cls(debug, mongo_uri, mongo_db)

  def request_fingerprint(self, request):
    """Return case insensitive request fingerprint"""
    fingerprint = hashlib.sha1()
    fingerprint.update(to_bytes(request.url.lower()))
    return fingerprint.hexdigest()

  def request_seen(self, request):
    """Check whether the url is already visited or not"""
    client = pymongo.MongoClient(self.mongo_uri)
    db = client[self.mongo_db]

    key = self.request_fingerprint(request)
    seen = False
    if db[self.collection_name].find_one({"_id": key}):
      self.logger.info("URL {} is already visited".format(request.url))
      seen = True
    else:
      try:
        db[self.collection_name].insert_one({"_id": key, "url": request.url, "time": datetime.now()})
      except DuplicateKeyError:
        self.logger.info("URL {} is already visited".format(request.url))
        seen = True
    
    client.close()
    return seen

