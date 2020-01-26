import scrapy
from scrapy.utils.httpobj import urlparse
import re

from simplecrawler.items import SimpleItem

class SimpleSpider(scrapy.Spider):
  name = "simple"

  def __init__(self, *args, **kwargs):
    self.search = kwargs.get('search', '')
    allowed_domains = kwargs.get('allowed_domains', '').split(',') or []
    if len(allowed_domains) > 0 and allowed_domains[0] != '':
      self.allowed_domains = [d.strip() for d in allowed_domains]

  def start_requests(self):
    if hasattr(self, 'state') and ('last_url' in self.state) and (self.state['last_url'] is not None):
      start_url = self.state['last_url']
    else:
      start_url = self.settings['START_URL']
    yield scrapy.Request(url=start_url, callback=self.parse)

  def parse(self, response):
    """
    @url http://quotes.toscrape.com
    @returns items 0 16
    @returns requests 50 60
    """
    print("Processing url:", response.url)
    if hasattr(self, 'state'):
      self.state['last_url'] = response.url

    # Yield the data item
    item = SimpleItem()
    item['page_title'] = response.css('title::text').get()
    item['image_urls'] = []
    for img in response.css('img'):
      alt = img.attrib['alt']
      src = img.attrib['src']
      if re.search(self.search, item['page_title']) or re.search(self.search, alt) or re.search(self.search, src):
        item['image_urls'].append(src)

    yield item

    # Find and request the following links
    following_links = response.css('a::attr(href)').getall()
    if following_links is not None:
      for link in following_links:
        url = response.urljoin(link)
        yield scrapy.Request(url, callback=self.parse)
    