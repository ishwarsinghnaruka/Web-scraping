import scrapy
from scrapy.crawler import CrawlerProcess
import csv

class TheSilCareLibrary(scrapy.Spider):
    name = "care_library"
    
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    
    custom_settings = {'FEED_FORMAT': 'csv','FEED_URI': 'car_library.csv'}

    def start_requests(self):
        url = "https://www.thesill.com/pages/care-library"
        yield scrapy.Request(url=url,headers = self.headers,callback=self.parse)

    def parse(self,response):
        data = response.xpath('//li[@class="accordion-item"]')
        for dt in data:
            Plant_name = dt.xpath('.//h3[@class="plant-name"]/text()').extract_first().strip()
            Light = dt.xpath('.//p/text()').extract()[2].strip()
            Water = dt.xpath('.//p/text()').extract()[3].strip()
            Fun_Fact = dt.xpath('.//p/text()').extract()[4].strip()
            Sad_Plant = "".join(dt.xpath('.//p[@class="sad-plant-sign"]/span/text()').extract())
            image_url = dt.xpath('.//noscript/img/@src').extract_first()

            yield {'Plant_name': Plant_name,
                   'Light': Light,
                   'Water': Water,
                   'Fun_Fact':Fun_Fact,
                   'Sad_Plant':Sad_Plant,
                   'image_url':image_url}

process = CrawlerProcess()
process.crawl(TheSilCareLibrary)
process.start()