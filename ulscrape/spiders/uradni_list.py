# -*- coding: utf-8 -*-
import re
from datetime import datetime
import scrapy


class UradniListSpider(scrapy.Spider):
    name = "uradni-list"
    base_url = 'https://www.uradni-list.si'
    allowed_domains = ["uradni-list.si"]
    search_url = 'https://www.uradni-list.si/glasilo-uradni-list-rs/rezultati-iskanja-tabele'
    initial_years = []

    def __init__(self, years=None, *args, **kwargs):
        """ Initialize original Scrapy spider. Then load arguments passed via CLI. """
        super(UradniListSpider, self).__init__(*args, **kwargs)

        if years is not None and years is not '':
            self.initial_years = [int(y) for y in years.split(",") if y != '']

    def start_requests(self):
       return [scrapy.http.FormRequest(
           url=self.search_url, formdata={'year': str(year)}, meta={'year': str(year)}
       ) for year in self.search_years()]

    def parse(self, response):
        if 'page' not in response.meta:
            return self.parse_archive_index_page(response)
        elif 'page' in response.meta:
            return self.parse_archive_page(response)
        else:
            raise Exception('No match for parsing the UL index or archive page, strange.')

    def parse_archive_index_page(self, response):
        pages_re = re.compile('.*val\(\'(?P<page>[0-9]+)\'\).*')
        pages = []
        if response.css('a[href*=javascript]::attr(href)').extract():
            for r in response.css('a[href*=javascript]::attr(href)').extract():
                if 'val' in r:
                    pages.append(int(re.match(pages_re, r).group('page')))
        else:
            pages = [1]

        year = response.meta['year']
        archive_pages = range(1, max(pages)+1)

        for p in archive_pages:
            yield scrapy.http.FormRequest(url=self.search_url, formdata={'year': year, 'page': str(p)}, meta={'year': str(year), 'page': str(p)})

    def parse_archive_page(self, response):
        yield {
                'urls': [ self.base_url + url for url in response.css('a[href*=_pdf]::attr(href)').extract() ],
                'meta': response.meta 
              }

    def search_years(self, initial_years=None):
        """ If initial_years are set, use that. Otherwise use list from 1991 till Today."""
        return self.initial_years if self.initial_years else range(1991, datetime.now().timetuple()[0]+1)
