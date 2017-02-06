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

        if years is not None or years is not '':
            self.initial_years = [int(y) for y in years.split(",") if y != '']

    def start_requests(self):
       return [scrapy.http.FormRequest(
           url=self.search_url, formdata={'year': str(year)}
       ) for year in self.search_years()]


    def parse(self, response):
        pages_re = re.compile('.*val\(\'(?P<page>[0-9]+)\'\).*')
        page = []
        if response.css('a[href*=javascript]::attr(href)').extract():
            for p in response.css('a[href*=javascript]::attr(href)').extract():
                if 'val' in p:
                    page.append(int(re.match(pages_re, p).group('page')))
        else:
            page = [1]
        #p_range = range(1, max(page)+1)
        #print(list(range(1, max(page)+1)), response.url, response.request.body)
        yield { 'pages': list(range(1, max(page)+1)),
                'response_url': str(response.url),
                'archive_year': str(response.request.body),
              }
            
        #pass

    def search_ul(self, response):
        pass

    def search_years(self, initial_years=None):
        """ If initial_years are set, use that. Otherwise use list from 1991 till Today."""
        return self.initial_years if self.initial_years else list(range(1991, datetime.now().timetuple()[0]+1))