# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class UlscrapeItem(Item):
    scrapped_at = Field()
    archive_year = Field()
    archive_page = Field()
    file_urls = Field()
