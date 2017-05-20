# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Session
import os
from HomeOfGoods.items import CommonInfoItem
from scrapy.exceptions import DropItem


Base = declarative_base()


class CommonTable(Base):
    __tablename__ = 'commondata'
    pk = Column(Integer, primary_key=True)
    type = Column(String)
    mfr = Column(String)
    model = Column(String)
    dimensions = Column(String)
    width = Column(String)
    height = Column(String)
    deep = Column(String)
    weight = Column(String)
    shop = Column(String)
    link_mfr = Column(String)
    link_shop = Column(String)
    url = Column(String)
    instruction = Column(String)

    def __init__(self, pk, type, mfr, model, dimensions, width, height, deep, weight, shop,
                 link_mfr, link_shop, url, instruction):
        self.pk = pk
        self.type = type
        self.mfr = mfr
        self.model = model
        self.dimensions = dimensions
        self.width = width
        self.height = height
        self.deep = deep
        self.weight = weight
        self.shop = shop
        self.link_mfr = link_mfr
        self.link_shop = link_shop
        self.url = url
        self.instruction = instruction

    def __repr__(self):
        return "<Data %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s>" % \
               (self.pk, self.type, self.mfr, self.model, self.dimensions, self.width,
                self.height, self.deep, self.weight, self.shop, self.link_mfr, self.link_shop,self.url,
                self.instruction)

class HomeofgoodsPipeline(object):
    def __init__(self):
        basename = 'data_scraped_common.db'
        self.engine = create_engine("sqlite:///%s" % basename, echo=True)
        if not os.path.exists(basename):
            Base.metadata.create_all(self.engine)
        self.pk = set()

    def process_item(self, item, spider):
        pk = item['pk']
        if pk not in self.pk:
            dt = CommonTable(item['pk'], item['type'], item['mfr'], item['model'], item['dimensions'], item['width'],
                             item['height'], item['deep'], item['weight'], item['shop'], item['link_mfr'],
                             item['link_shop'], item['url'], item['instruction']
                           )
            self.pk.add(pk)
            self.session.add(dt)

        return item

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def open_spider(self, spider):
        self.session = Session(bind=self.engine)

