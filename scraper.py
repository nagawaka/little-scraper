# scrapy runspider scraper.py -o file.json

import logging

import scrapy

class Line(scrapy.Item):
  title = scrapy.Field()
  link = scrapy.Field()
  pdf = scrapy.Field()

class QuotesSpider(scrapy.Spider):
  name = 'quotes'
  start_urls = [
    'https://datassette.org/revistas/acao-games',
  ]

  custom_settings = {
    'ITEM_PIPELINES': {'scrapy.pipelines.files.FilesPipeline': 1},
    'FILES_STORE': 'downloads'
  }

  BASE_URL = 'https://datassette.org'

  def parse(self, response):
    for quote in response.css('.view-content td'):
      link = quote.css('.views-field-title a::attr("href")').extract()[0]
      absolute_url = self.BASE_URL + link
      line = Line(
        title=quote.css('.views-field-title a::text').extract()[0],
        link=link
      )

      pdfRequest = scrapy.Request(absolute_url, callback=self.parseLink, cb_kwargs=line)


      yield pdfRequest

    next_page = response.css('li.pager-next a::attr("href")').extract()
    if next_page[1] is not None:
      yield response.follow(next_page[1], self.parse)
  
  def parseLink(self, response, title, link):

    yield {
      'link': response.url,
      'title': title,
      'file_urls': [response.css('.file a::attr("href")').extract()[0]]
    }
    # return 
  
