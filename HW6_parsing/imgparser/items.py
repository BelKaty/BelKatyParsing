# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose

def process_name(value):
   
    return value


class ImgparserItem(scrapy.Item):
   
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=Compose(process_name), output_processor=TakeFirst())
    path = scrapy.Field()
    category = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()

