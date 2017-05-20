# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import scrapy

class QSpider(scrapy.Spider):
    name = "query_ym"
    handle_httpstatus_list = [302]
    with open("model.txt", "r") as m:
        model = m.readline()
    keywords = model.replace(" ","%20", 100)
    allowed_domains = ["market.yandex.ru"]
    start_urls = (
        'https://market.yandex.ru/search?text='+ keywords,)
    def parse(self, response):
        product = response.xpath('//div[@class="snippet-card__col"]/h3/a/@href').extract()[0]
        product = str(product)
        link = "https://market.yandex.ru" + product

        f = open("urls.txt", "w")
        f.write(str(link))
        f.close()
