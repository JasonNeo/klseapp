# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KlsebuddybotItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_title = scrapy.Field()
    date = scrapy.Field()
    # pass
