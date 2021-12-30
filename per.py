import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import scrapy_xlsx

class PerFume(scrapy.Spider):
    name = "perfume_data"
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    FEED_EXPORTERS = {'xlsx': 'scrapy_xlsx.XlsxItemExporter'}
    custom_settings = {'FEED_EXPORTERS' :FEED_EXPORTERS,'FEED_FORMAT': 'xlsx','FEED_URI': 'perfume.xlsx'}

    def start_requests(self):
        url = "https://perfumeonline.ca/pages/all-brands"
        yield scrapy.Request(url=url,headers = self.headers,callback=self.parse)

    def parse(self,response):
        urls =  response.xpath('//ul[@class="brs"]/li/a/@href').extract()
        for url in urls:
            url = "https://perfumeonline.ca" + url + "?view=all"
            yield response.follow(url = url,headers = self.headers,callback = self.details)

    def details(self,response):
        products = response.xpath('//div[@class="product__inside__image"]/a/@href').extract()
        for prod in products:
            yield response.follow(url = prod,headers=self.headers,callback=self.info)

    def info(self,response):
        product_name = response.xpath('//h1/text()').extract_first()
        product_type = response.xpath('//h1/span/text()').extract_first()
        variant_name = " , ".join(response.xpath('//label[@id = "datasafe"]/text()').extract()).strip().replace("  ","").replace("\n","").replace(",","")
        variant_price = response.xpath('//label[@id = "datasafe"]/span/span/text()').extract_first()
        variant_brand = response.xpath('//div[@itemprop="brand"]/span/a/text()').extract_first()
        product_image = response.xpath('//div[@class="product-main-image"]/div/img/@src').extract()
    
        yield { 'product_name': product_name,
                'product_type': product_type,
                'variant_name':variant_name,
                'variant_price':variant_price,
                'variant_brand':variant_brand,
                'product_image':product_image}

process = CrawlerProcess()
process.crawl(PerFume)
process.start()