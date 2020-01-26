from scrapy.http import Request
from simplecrawler.filters import VisitedSiteFilter

from simplecrawler.tests.base import BaseDBTest

class VisitedSiteFilterTest(BaseDBTest):

  def test_request_seen(self):
    request1 = Request('https://a.com')
    request2 = Request('https://a.com')
    request3 = Request('https://b.com')

    vf = VisitedSiteFilter(mongo_uri=self.mongo_uri, mongo_db=self.mongo_db)
    self.assertFalse(vf.request_seen(request1))
    self.assertTrue(vf.request_seen(request2))
    self.assertFalse(vf.request_seen(request3))