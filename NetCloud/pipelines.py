# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings

from NetCloud.items import NetcloudItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class NetcloudPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(settings['MONGODB_HOST'],settings['MONGODB_PORT'])
        db_name = settings['MONGODB_DBNAME']
        self.db = client[db_name]
        self.artist = self.db[settings['MONGODB_COL_ARTIST']]
        pass
    def process_item(self, item, spider):
        if isinstance(item, NetcloudItem):
            artist_info = dict(item)
            self.artist.insert_one(artist_info)
            print("NetcloudArtist----->SUCCESS")

        return item
