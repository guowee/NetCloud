# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NetcloudItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    artist_id = scrapy.Field()
    artist_name = scrapy.Field()
    artist_url = scrapy.Field()
    album_url = scrapy.Field()
    pass
