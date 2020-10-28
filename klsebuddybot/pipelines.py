# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.http.request import Request
from scrapy.pipelines.files import FilesPipeline
import datetime
import html


class KlsebuddybotPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
           yield Request(file_url, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        original_path = super(KlsebuddybotPipeline, self).file_path(request)
        sha1_and_extension = original_path.split('/')[1] # delete 'full/' from the path
        # filename = request.meta.get('filename','')[0] + "_" + sha1_and_extension
        item = request.meta['item']
        today = datetime.date.today().strftime("%d_%m_%Y")
        filename = today + '/' + item['file_title'] + '_' + sha1_and_extension
        # filename = 'posts/' + today + '/' + sha1_and_extension
        return filename