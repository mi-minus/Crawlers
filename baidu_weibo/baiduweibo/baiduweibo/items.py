# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Topic_Item(scrapy.Item):
    topic_url = scrapy.Field()
    topic_title = scrapy.Field()
    topic_content = scrapy.Field()
    topic_pt_time = scrapy.Field()
    topic_st_time = scrapy.Field()
    topic_id = scrapy.Field()
    topic_kw = scrapy.Field()
    topic_site_id = scrapy.Field()
    topic_site_name = scrapy.Field()

