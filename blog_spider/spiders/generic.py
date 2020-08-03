import scrapy
from scrapy.spiders import SitemapSpider
from urllib.parse import urlparse, urljoin
import logging

class GenericSpider(SitemapSpider):
    name = 'generic'
    custom_settings = {
        'LOG_LEVEL': 'INFO'
    }

    def __init__(self, *args, **kwargs):
        super(GenericSpider, self).__init__(*args, **kwargs)
        endpoints = kwargs.get('start_urls').split(',')
        self.sitemap_urls = [urljoin(x, "/sitemap.xml") for x in endpoints]
        logging.info(" ".join(self.start_urls))
        self.allowed_domains = [urlparse(x).netloc for x in endpoints]

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
        item['html'] = container.extract()
        item['domain'] = response.meta['download_slot']
        item['url'] = response.url
        return item
