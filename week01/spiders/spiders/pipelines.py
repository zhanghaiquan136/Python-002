# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SpidersPipeline:
    def process_item(self, item, spider):
        movie_title = item['movie_title']
        movie_tpye = item['movie_tpye']
        release_time = item['release_time']
        SaveToFile = f'{movie_title},{movie_tpye},{release_time}\n'
        with open('./top10_movies.csv','a+',encoding='utf-8') as Append:
            Append.write(SaveToFile)
        return item