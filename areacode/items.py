# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AreacodeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CpdcItem(scrapy.Item):
    region_id = scrapy.Field()
    region_name = scrapy.Field()
