# -*- coding: utf-8 -*-

from .sitemap import SitemapSpider
from scrapenews.items import ScrapenewsItem
from datetime import datetime
import pytz

SAST = pytz.timezone('Africa/Johannesburg')


class IOLSpider(SitemapSpider):
    name = 'iol'
    allowed_domains = ['www.iol.co.za']

    sitemap_urls = ['https://www.iol.co.za/robots.txt']
    sitemap_follow = [
        'www.iol.co.za/sitemap-1.xml',
        'www.iol.co.za/sitemap-0.xml',
        'www.iol.co.za/news/sitemap.xml',
        'www.iol.co.za/politics/sitemap.xml',
        'www.iol.co.za/business-report/sitemap.xml',
        'www.iol.co.za/personal-finance/sitemap.xml',
        'https://www.iol.co.za/sport/sitemap.xml',
        'https://www.iol.co.za/entertainment/sitemap.xml',
        'www.iol.co.za/lifestyle/sitemap.xml',
        'www.iol.co.za/motoring/sitemap.xml',
        'www.iol.co.za/travel/sitemap.xml',
    ]

    publication_name = 'IOL News'

    def parse(self, response):
        title = response.xpath('//header/h1/text()').extract_first()
        self.logger.info('%s %s', response.url, title)
        article_body = response.css('div.article-widget-text')
        if article_body:
            body_html = article_body.extract_first()
            byline = response.xpath('//span[@itemprop="author"]/strong/text()').extract_first()
            publication_date_str = response.xpath('//span[@itemprop="datePublished"]/@content').extract_first()

            publication_date = datetime.strptime(publication_date_str, '%Y-%m-%dT%H:%M')
            publication_date = SAST.localize(publication_date)

            item = ScrapenewsItem()
            item['body_html'] = body_html
            item['title'] = title
            item['byline'] = byline
            item['published_at'] = publication_date.isoformat()
            item['retrieved_at'] = datetime.utcnow().isoformat()
            item['url'] = response.url
            item['file_name'] = response.url.split('/')[-1]
            item['spider_name'] = self.name

            item['publication_name'] = self.publication_name

            yield item
