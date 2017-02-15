# -*- coding: utf-8 -*-

from os import getenv

BOT_NAME = 'ulscrape'

SPIDER_MODULES = ['ulscrape.spiders']
NEWSPIDER_MODULE = 'ulscrape.spiders'

# USER_AGENT = 'ulscrape (+http://www.yourdomain.com)'

ROBOTSTXT_OBEY = False

# CONCURRENT_REQUESTS = 32
# DOWNLOAD_DELAY = 3
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16
# COOKIES_ENABLED = False

TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

AMQP_URL = getenv("AMQP_URL", "amqp://ulscrape:ulscrape@rabbitmq")

# SPIDER_MIDDLEWARES = {}

DOWNLOADER_MIDDLEWARES = {
    'ulscrape.spiders.UlScrapeDownloaderMiddleware': 0,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}

ITEM_PIPELINES = {
    'scrapy.pipelines.files.FilesPipeline': 1,
}

FILES_STORE = getenv('FILES_STORE', './data/files')

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

DUPEFILTER_DEBUG = True
