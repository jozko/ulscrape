#!/usr/bin/env python
import unittest
from test.helpers import response_from
from ulscrape.spiders.uradni_list import UradniListSpider
from pprint import pprint


class TestUradniListSpider(unittest.TestCase):
    spider = None

    def setUp(self):
        self.spider = UradniListSpider()

    def test_years(self):
        spider = UradniListSpider(years="2000,2015")
        self.assertEqual(len(spider.search_years()), 2)

    def test_parse_simple_index(self):
        fd = {'year': '2017'}
        response = response_from('002-rezultati-2017.html', None, fd, fd)
        res = self.spider.parse(response)
        pprint(res)
        self.assertEqual(len(list(res)), 1)

    def test_parse_with_more_index(self):
        fd = {'year': '2016'}
        response = response_from('001-rezultati-2016.html', None, fd, fd)
        res = self.spider.parse(response)
        self.assertEqual(len(list(res)), 11)
