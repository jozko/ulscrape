from scrapy import Spider
from scrapy import FormRequest, Request
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from enum import Enum
import pika
from pprint import pprint
from scrapy.http import Response, HtmlResponse
from ulscrape.settings import AMQP_URL
from pdb import set_trace
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.serialize import ScrapyJSONEncoder
from json import dumps, loads
import pickle


class UlSpiderModes(Enum):
    Standalone, Master, Slave = range(3)


class UlSpider(Spider):
    mode = UlSpiderModes.Standalone
    channel = None
    channel_name = 'scraping'

    def __init__(self, mode=None, *args, **kwargs):
        super(UlSpider, self).__init__(*args, **kwargs)
        if mode: self.mode = UlSpiderModes[mode]
        self.setup_rabbitmq()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)

        if spider.mode == UlSpiderModes.Slave:
            spider.crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)

        return spider

    def spider_idle(self):
        if self.mode == UlSpiderModes.Slave:
            self.process_request_from_queue()
            raise DontCloseSpider

    def process_request_from_queue(self):
        method_frame, header_frame, raw_q = self.channel.basic_get(queue=self.channel_name)
        if raw_q:
            self.logger.info("Got something on {}".format(self.channel_name))
            request = pickle.loads(raw_q)
            self.crawler.engine.crawl(request, spider=self)
            self.channel.basic_ack(method_frame.delivery_tag)

    def setup_rabbitmq(self):
        self.logger.info("Scraper running in {} mode.".format(self.mode))
        if self.mode != UlSpiderModes.Standalone:
            self.channel = UlSpider.channel_from_settings(self.channel_name)

    @staticmethod
    def channel_from_settings(queue_name):
        connection = {
            'blocking': pika.BlockingConnection,
            'twiseted': pika.TwistedConnection
        }['blocking'](pika.URLParameters(AMQP_URL))

        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        return channel


class Dispersable(object): pass


class DisperseFormRequest(Dispersable, FormRequest):
    pass


class DisperseRequest(Dispersable, Request):
    pass


class UlScrapeDownloaderMiddleware(object):
    crawler = None

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        if isinstance(request, Dispersable) and spider.mode == UlSpiderModes.Master:
            publish = spider.channel.basic_publish(exchange='', routing_key='scraping', body=pickle.dumps(request))
            spider.logger.info("Request was sent to MQ ~> {} = {}".format(request.url, publish))
            return HtmlResponse(request=request, url=request.url, encoding='utf-8', body=dumps({}))

        return None
