# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import json

from simplecrawler.items import SimpleItem

class SimpleImagePipeline(ImagesPipeline):

	def get_media_requests(self, item, info):
		for image_url in item['image_urls']:
			yield scrapy.Request(image_url)

	def item_completed(self, results, item, info):
		image_paths = []
		for ok, x in results:
			if ok:
				image_paths.append(x['path'])
		
		if len(image_paths) == 0:
			raise DropItem("Site contains no images")
		item['image_paths'] = image_paths
		return item


class JsonWriterPipeline(object):

	def __init__(self, output_path):
		self.output_path = output_path

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			output_path=crawler.settings.get('JSON_OUTPUT_PATH'),
		)

	def open_spider(self, spider):
		self.file = open(self.output_path, 'w')

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + "\n"
		self.file.write(line)
		return item
