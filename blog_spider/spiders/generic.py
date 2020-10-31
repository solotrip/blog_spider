import scrapy
from scrapy.spiders import SitemapSpider
from scrapy.exceptions import CloseSpider
from urllib.parse import urlparse, urljoin, urlunparse
import logging
from scrapy.http import Request, XmlResponse


class GenericSpider(SitemapSpider):
    name = 'generic'
    custom_settings = {
        'LOG_LEVEL': 'INFO'
    }
    count = 0
    def __init__(self, start_urls='', *args, **kwargs):
        super(GenericSpider, self).__init__(*args, **kwargs)
        endpoints = set(start_urls.split(','))
        self.sitemap_follow = [r'^((?!image|attachment).)*$']  # don't crawl image sitemaps
        self.sitemap_urls = [urljoin(urlunparse(urlparse(x)._replace(path='')), "/sitemap.xml") for x in endpoints]
        self.sitemap_urls.extend(
            [urljoin(urlunparse(urlparse(x)._replace(path='')), "/sitemap_index.xml") for x in endpoints])
        self.sitemap_urls.extend([urljoin(urlunparse(urlparse(x)._replace(path='')), "/robots.txt") for x in endpoints])
        self.allowed_domains = [urlparse(x).netloc for x in endpoints]

    def start_requests(self):
        requests = list(super(GenericSpider, self).start_requests())
        logging.info("Requests count: {}".format(len(requests)))
        return requests

    def parse(self, response):
        item = {}
        container = response.xpath('//article')
        if not container:
            container = response.css(".post")
        item['title'] = container.xpath('.//h1/text()').extract_first()
        if not item['title']:
            item['title'] = response.xpath('//head/title/text()').get()
        item['description'] = response.xpath("//head/meta[@property='og:description']/@content").extract_first()
        meta_tags = response.xpath("//head/meta[@property and @content]")
        item['meta'] = {tag.xpath("@property").get(): tag.xpath("@content").get() for tag in meta_tags}
        container.xpath('.//*[name(.) != "script" and name(.) != "style" ]').extract()
        item['text'] = "\n".join(
            container.xpath('.//*[name(.) != "script" and name(.) != "style" ]/text()').extract())
        item['html'] = response.text
        item['domain'] = response.meta['download_slot']
        item['url'] = response.url
        self.count+=1
        return item

