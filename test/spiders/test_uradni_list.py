#!/usr/bin/env python
import unittest
from test.helpers import response_from
from ulscrape.spiders.uradni_list import UradniListSpider
from pprint import pprint


class TestUradniListSpider(unittest.TestCase):
    spider = None

    def setUp(self):
        self.spider = UradniListSpider()

    def test_parse_simple_index(self):
        response_2017 = self.spider.parse(response_from('002-rezultati-2017.html', formdata={'year': '2017'}))
        self.assertEqual(len(response_2017), 1)

    def test_parse_with_more_index(self):
        response = self.spider.parse(response_from('001-rezultati-2016.html', formdata={'year': '2016'}))
        self.assertEqual(len(response), 11)


