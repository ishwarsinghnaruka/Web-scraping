import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy_xlsx
import pandas as pd
import re

class Echa(scrapy.Spider):
    name = "echa_europa_data"

    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    
    FEED_EXPORTERS = {'xlsx': 'scrapy_xlsx.XlsxItemExporter'}
    
    custom_settings = {'FEED_EXPORTERS' :FEED_EXPORTERS,'FEED_FORMAT': 'xlsx','FEED_URI': 'echa_europa.xlsx'}

    def start_requests(self):
        url = "https://echa.europa.eu/information-on-chemicals/cl-inventory-database"
        yield scrapy.Request(url=url,headers = self.headers,callback=self.parse)

    def parse(self,response):
    	data = response.xpath('//tbody[@class="table-data"]/tr')[:-1]
    	next_page = response.xpath('//li/a[contains(text(),"Next")]/@href').extract_first()
    	for dt in data:
    		name = dt.xpath('.//td/a/text()').extract_first() + "," + dt.xpath('.//td/a/@href').extract_first()
    		EC_List_no = dt.xpath('.//td[@class="table-cell "]/text()').extract()[0]
    		cas_no = dt.xpath('.//td[@class="table-cell "]/text()').extract()[1]
    		classification = dt.xpath('.//td[@class="table-cell "]/div/div/div/span/text()').extract_first()
    		yield { "name":name,
    		        "EC/List_no":EC_List_no,
    		        "cas_no":cas_no,
    		        "classification":classification}
    	yield scrapy.Request(url = next_page,headers = self.headers,callback = self.parse)

process = CrawlerProcess()
process.crawl(Echa)
process.start()
