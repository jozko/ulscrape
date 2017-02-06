# -*- coding: utf-8 -*-
import re
from datetime import datetime
import scrapy


class UradniListSpider(scrapy.Spider):
    name = "uradni-list"
    base_url = 'https://www.uradni-list.si'
    allowed_domains = ["uradni-list.si"]
    search_url = 'https://www.uradni-list.si/glasilo-uradni-list-rs/rezultati-iskanja-tabele'

    def start_requests(self):
       return [scrapy.http.FormRequest(
                url='https://www.uradni-list.si/glasilo-uradni-list-rs/rezultati-iskanja-tabele',
                formdata={'year': str(year)}
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

    def search_years(self):
        return list(range(1991, datetime.now().timetuple()[0]+1))