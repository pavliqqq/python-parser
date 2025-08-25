import logging
from parser.items import QuestionAnswerItem
import scrapy


class KreuzwortSpider(scrapy.Spider):
    name = "kreuzwort"
    allowed_domains = ["kreuzwort-raetsel.net"]
    start_urls = ["https://www.kreuzwort-raetsel.net/uebersicht.html"]

    def parse(self, response):
        letter_links = response.css('ul.dnrg li a::attr(href)').getall()
        for link in letter_links:
            yield response.follow(link, callback=self.parse_letter)

    def parse_letter(self, response):
        letter_links = response.css('ul.dnrg li a::attr(href)').getall()
        for link in letter_links:
            yield response.follow(link, callback=self.parse_data)

    def parse_data(self, response):
        rows = response.css('#Searchresults table tbody tr')
        result = []
        for row in rows:
            question = row.css('td.Question a::text').get()
            answer = row.css('td.AnswerShort a::text').get()
            if question and answer:
                result.append({
                    'question': question,
                    'answer': answer
                })
                
        yield QuestionAnswerItem(
            data_rows = result
        )