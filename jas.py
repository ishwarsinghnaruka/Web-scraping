import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import scrapy_xlsx
import pandas as pd
class JASANZ(scrapy.Spider):
    name = "jasanz_data"
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    FEED_EXPORTERS = {'xlsx': 'scrapy_xlsx.XlsxItemExporter'}
    custom_settings = {'FEED_EXPORTERS' :FEED_EXPORTERS,'FEED_FORMAT': 'xlsx','FEED_URI': 'jas.xlsx'}
                       # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1,'DOWNLOAD_DELAY': 2}

    def start_requests(self):
        url = 'https://www.jas-anz.org/our-directory/certified-organisations?combine=&country%5B%5D=Australia&location=&standard_selective%5B%5D=AS%252FNZS%2B4801%253A2001&standard_selective%5B%5D=AS%252FNZS%2BISO%2B14001%253A2004&standard_selective%5B%5D=AS%252FNZS%2BISO%2B9001%253A2008&standard_selective%5B%5D=ISO%2B45001%253A2018&standard_selective%5B%5D=ISO%252FIEC%2B27001%253A2013&standard_selective%5B%5D=OHSAS%2B18001%253A2007&scope='
        yield scrapy.Request(url = url,headers=self.headers,callback = self.parse)
    
    def parse(self,response):
        table_data = response.xpath('//table/tbody/tr')
        for row in table_data:
            Certification_Body = row.xpath('.//td[@class="views-field views-field-accredited-body"]/text()').extract_first().strip()
            Organisation_Name = row.xpath('.//td[@class="views-field views-field-name"]/a/text()').extract_first().strip()
            suburb_city = row.xpath('.//td[@class="views-field views-field-location"]/text()').extract_first().strip()
            country = row.xpath('.//td[@class="views-field views-field-country"]/text()').extract_first().strip()
            status = row.xpath('.//td[@class="views-field views-field-status"]/text()').extract_first().strip()

            yield {"Certification Body":Certification_Body,
                    "Organisation Name":Organisation_Name,
                    "suburb/city":suburb_city,
                    "country":country,
                    "status":status}

        next_page = row.xpath('//a[@title="Go to next page"]/@href').extract_first()
        yield response.follow(url = next_page,headers=self.headers,callback=self.parse)

process = CrawlerProcess()
process.crawl(JASANZ)
process.start()