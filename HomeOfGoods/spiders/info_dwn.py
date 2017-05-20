# -*- decoding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from HomeOfGoods.items import CommonInfoItem
import urlparse
from scrapy.http import Request


class InfoSpider(CrawlSpider):
    name = "inf"

    allowed_domains = ["market.yandex.ru","avatars.mds.yandex.net"]

    with open("urls.txt", "rt") as f:
        start_urls = [url.strip() for url in f.readlines()]

    rules = (
       Rule(LinkExtractor(allow=('spec')), callback='parse_item'),
    )

    def parse_item(self, response):
        hxs = Selector(response)

        Item = CommonInfoItem()

        model = hxs.xpath("//div[@class='n-title__text']/h1/a/text()").extract()[0]
        print model
        link_mfr = hxs.xpath("//div[@class='product-spec-wrap__body']/ul/li/a[contains(text(),'www')]/@href").extract()
        print link_mfr
        if link_mfr != []:
            Item['link_mfr'] = link_mfr[0]
        else: Item['link_mfr'] = ''

        dimens = hxs.xpath(u'//div[@class="layout__col layout__col_size_p75 n-product-spec-wrap"]/div/dl[dt/span[contains(text(),"\u0428x\u0413x\u0412") or contains(text(),"\u0420\u0430\u0437\u043C\u0435\u0440")]]/dd/span/text()').extract()
        Item['model'] = model[len(model.split(" ")[0])+ 1:len(model)]
        Item['mfr'] = model.split(" ")[0]
        with open("primary_key.txt", "r") as f:
            pk = int(f.readline())
        with open("primary_key.txt", "w") as f:
            f.write(str(pk+1))
        Item['pk'] = pk
        Item['type'] = hxs.xpath("//div[@class='n-product-headline__content']/ul/li/a/@title").extract()[0]
        Item['shop'] = ''
        Item['link_shop'] = ''
        if dimens != []:
            Item['dimensions'] = dimens[0]
            Item['width'] = dimens[0].split("x")[0] + " " + dimens[0].split(" ")[1]
            Item['height'] = dimens[0].split("x")[2]
            Item['deep'] = dimens[0].split("x")[1] + " " + dimens[0].split(" ")[1]
        else:
            Item['dimensions'] = ''
            Item['width'] = ''
            Item['height'] = ''
            Item['deep'] = ''
        weig = hxs.xpath(u'//div[@class="layout__col layout__col_size_p75 n-product-spec-wrap"]/div/dl[dt/span/text()="\u0412\u0435\u0441"]/dd/span/text()').extract()
        if weig != []:
            Item['weight'] = weig[0]
        else: Item['weight'] = ''
        Item['url'] = response.url
        Item['image_urls'] = [urlparse.urljoin(response.url, u) for u in response.xpath("//img[contains(@alt,'"+model+"')]/@src").extract()]
        Item['instruction'] = ''
        yield Item