from scrapy.item import Item, Field

class CommonInfoItem(Item):
    pk = Field()
    model = Field()
    type = Field()
    shop = Field()
    width = Field()
    height = Field()
    deep = Field()
    mfr = Field()
    link_mfr = Field()
    link_shop = Field()
    dimensions = Field()
    weight = Field()
    url = Field()
    img = Field()
    #image_urls = Field()
    #image = Field()