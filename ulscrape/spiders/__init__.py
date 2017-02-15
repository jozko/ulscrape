from scrapy.spider import Spider
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from enum import Enum
import pika
from pprint import pprint
from ulscrape.settings import AMQP_URL


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

    def setup_rabbitmq(self):
        self.logger.info("Running in {} mode".format(self.mode))

        if self.mode != UlSpiderModes.Standalone:
            self.channel = UlSpider.channel_from_settings(self.channel_name)
            self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

    def schedule_next_request(self):
        req = self.get_next_request()

        print("-----------------------------")
        print("--> schedule_next_request <--")

        # if req:
        #    self.crawler.engine.crawl(req, spider=self)

    def get_next_request(self):
        method_frame, header_frame, url = self.server.basic_get(queue=self.channel_name)
        pprint(url)

        if url:
            return self.make_requests_from_url(url)

    def spider_idle(self):
        self.schedule_next_request()
        raise DontCloseSpider

    def listen(self):
        self.logger.info("Listening to channel {}".format(self.channel_name))

    def slave_listen(self):
        self.logger.info("Slave listening to channel {}".format(self.channel_name))
        return []

    @staticmethod
    def channel_from_settings(queue_name):
        connection = {
            'blocking': pika.BlockingConnection,
            'twiseted': pika.TwistedConnection
        }['blocking'](pika.URLParameters(AMQP_URL))

        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        return channel
