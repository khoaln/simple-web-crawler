import scrapy
from scrapy.utils.httpobj import urlparse

class SimpleSpider(scrapy.Spider):
  name = "simple"

  def __init__(self, *args, **kwargs):
    self.start_urls = [kwargs.get('start_url', '')]
    allowed_domains = kwargs.get('allowed_domains', '').split(',') or []
    if len(allowed_domains) > 0 and allowed_domains[0] != '':
      self.allowed_domains = [d.strip() for d in allowed_domains]

  # def start_requests(self):
  #   start_url = self.settings['START_URL']
  #   yield scrapy.Request(url=start_url, callback=self.parse)

  def parse(self, response):
    """
    @url http://quotes.toscrape.com
    @returns items 0 16
    @returns requests 50 60
    """
    print("Processing url:", response.url)
    following_links = response.css('a::attr(href)').getall()
    if following_links is not None:
      for link in following_links:
        url = response.urljoin(link)
        print(url)
        yield scrapy.Request(url, callback=self.parse)
    