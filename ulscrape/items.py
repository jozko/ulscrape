# -*- coding: utf-8 -*-

from scrapy import Item, Field
from datetime import datetime


class Document(Item):
    scrapped_at = Field()
    archive_year = Field()
    archive_page = Field()
    file_urls = Field()
    files = Field()

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.setdefault('scrapped_at', datetime.utcnow())
