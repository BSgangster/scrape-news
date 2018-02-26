# -*- coding: utf-8 -*-
import scrapy


class ScrapenewsItem(scrapy.Item):
    publication_name = scrapy.Field()
    url = scrapy.Field()
    scraped_date = scrapy.Field()
    byline = scrapy.Field()
    publication_date = scrapy.Field()
    title = scrapy.Field()
    body_html = scrapy.Field()
