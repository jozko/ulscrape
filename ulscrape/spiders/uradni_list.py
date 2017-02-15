# -*- coding: utf-8 -*-
import re
from datetime import datetime
import scrapy
from ulscrape.spiders import UlSpider, UlSpiderModes, DisperseRequest, DisperseFormRequest
from scrapy.exceptions import DontCloseSpider


class UradniListSpider(UlSpider):
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
        if self.mode != UlSpiderModes.Slave:
            return self.initial_requests()
        else:
            return []

    def initial_requests(self):
        return [DisperseFormRequest(self.search_url,
                                    formdata={'year': str(year)},
                                    meta={'year': year}) for year in self.search_years()]

    def parse(self, response):
        if 'page' not in response.meta:
            return self.parse_archive_index_page(response)
        elif 'page' in response.meta:
            return self.parse_archive_page(response)
        else:
            raise Exception('No match for parsing the UL index or archive page, strange.')

    def parse_archive_index_page(self, response):
        pages = re.findall(r'.*val\(\'(\d+)\'\).*/g', response.text)

        if len(pages) > 0:
            pages_max = max([int(p) for p in pages])
        else:
            pages_max = 1

        year = response.meta['year']
        archive_pages = range(1, pages_max + 1)

        for p in archive_pages:
            yield DisperseFormRequest(self.search_url,
                                      formdata={'year': str(year), 'page': str(p)},
                                      meta={'year': year, 'page': p})

    def parse_archive_page(self, response):
        yield {
            'urls': [self.base_url + url for url in response.css('a[href*=_pdf]::attr(href)').extract()],
            'meta': response.meta
        }

    def search_years(self, initial_years=None):
        """ If initial_years are set, use that. Otherwise use list from 1991 till Today."""
        return self.initial_years if self.initial_years else range(1991, datetime.now().year + 1)
