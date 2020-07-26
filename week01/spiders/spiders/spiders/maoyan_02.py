# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from spiders.items import SpidersItem

class MaoyanSpider(scrapy.Spider):
    
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']
    
    # 获取详情页链接

    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="channel-detail movie-item-title"]')
        
        for movie in movies[0:10]:
            item = SpidersItem()
            movie_title = movie.xpath('./a/text()').extract_first()
            movie_link = 'https://maoyan.com' + movie.xpath('./a/@href').extract_first()
            item['movie_title'] = movie_title
            item['movie_link'] = movie_link
            yield scrapy.Request(url=movie_link, meta={'item': item}, callback=self.parse2)
    
    def parse2(self,response):
        item = response.meta['item']
        info = Selector(response=response).xpath('//div[@class="movie-brief-container"]/ul')
        movie_tpye = info.xpath('./li[1]/*/text()').extract()
        release_time = info.xpath('./li[3]/text()').extract_first()

        item['movie_tpye'] = movie_tpye
        item['release_time'] = release_time
        yield item