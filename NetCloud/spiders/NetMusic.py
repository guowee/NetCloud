# -*- coding: utf-8 -*-
import re
import scrapy

from NetCloud.items import NetcloudItem


class NetmusicSpider(scrapy.Spider):
    name = 'NetMusic'
    allowed_domains = ['music.163.com']
    # start_urls = ['http://music.163.com/discover/artist/cat?id={gid}&initial={initial}']
    group_ids = (1001, 1002, 1003, 2001, 2002, 2003, 6001, 6002, 6003, 7001, 7002, 7003, 4001, 4002, 4003)
    initials = [i for i in range(65, 91)] + [0]
    headers = {
        "Referer": "http://music.163.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3067.6 Safari/537.36",
    }

    def start_requests(self):
        for gid in self.group_ids:
            for initial in self.initials:
                url = "http://music.163.com/discover/artist/cat?id={gid}&initial={initial}". \
                    format(gid=gid, initial=initial)
                yield scrapy.Request(url=url, headers=self.headers, method='GET', callback=self.parse, dont_filter=True)
            yield scrapy.Request("http://music.163.com/#/discover/artist/cat?id={gid}&initial=0".format(gid=gid),
                                 callback=self.parse,
                                 dont_filter=True)

        pass

    def parse(self, response):

        lis = response.selector.xpath('//ul[@id="m-artist-box"]/li')

        for i in range(len(lis)):
            item = NetcloudItem()
            item['artist_name'] = lis[i].xpath('//a[@class="nm nm-icn f-thide s-fc0"]/text()').extract()[i]
            post_url = lis[i].xpath('//a[@class="nm nm-icn f-thide s-fc0"]/@href').extract()[i]
            p_url = post_url.lstrip()
            album_url = p_url.split('?')
            item['artist_id'] = int(re.compile(r'\d+').findall(p_url)[0])
            item['artist_url'] = 'http://music.163.com' + p_url
            item['album_url'] = 'http://music.163.com' + album_url[0] + '/album?' + album_url[1]
            yield item

        pass
