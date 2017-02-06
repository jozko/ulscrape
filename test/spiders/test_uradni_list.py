#!/usr/bin/env python
import unittest
from test.helpers import response_from
from ulscrape.spiders.uradni_list import UradniListSpider


class TestUradniListSpider(unittest.TestCase):
    spider = None

    def setUp(self):
        self.spider = UradniListSpider()

    def test_parse_simple_index(self):
        fd = {'year': '2017'}
        res = self.spider.parse(response_from('002-rezultati-2017.html', fd))
        self.assertEqual(len(res), 1)

    def test_parse_with_more_index(self):
        fd = {'year': '2016'}
        res = self.spider.parse(response_from('001-rezultati-2016.html', fd))
        self.assertEqual(len(res), 11)
