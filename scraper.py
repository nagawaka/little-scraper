# scrapy runspider scraper.py -o file.json

import scrapy

class QuotesSpider(scrapy.Spider):
  name = 'quotes'
  start_urls = [
    'https://datassette.org/revistas/acao-games',
  ]

  def parse(self, response):
    for quote in response.css('.view-content td'):
      yield {
        'text': quote.css('.views-field-title a::text').get(),
        'author': quote.css('.views-field-title a::attr("href")').get(),
      }

    next_page = response.css('li.pager-next a::attr("href")').getall()
    if next_page[1] is not None:
      yield response.follow(next_page[1], self.parse)