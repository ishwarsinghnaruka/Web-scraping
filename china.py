import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy_xlsx
import pandas as pd
import re

class ChinaNoobWatches(scrapy.Spider):
    name = "chinanoobwatch_data"

    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    
    FEED_EXPORTERS = {'xlsx': 'scrapy_xlsx.XlsxItemExporter'}
    
    custom_settings = {'FEED_EXPORTERS' :FEED_EXPORTERS,'FEED_FORMAT': 'xlsx','FEED_URI': 'chinanoobwath.xlsx'}

    def start_requests(self):
        url = "https://www.chinanoobwatch.io/"
        yield scrapy.Request(url=url,headers = self.headers,callback=self.parse)

    def parse(self,response):
        category_urls = response.xpath('//div[@class="block_content"]/ul/li/a/@href').extract()
        
        for category in category_urls[1:2]:
            yield scrapy.Request(url= category,headers=self.headers,callback=self.product_url_extract)

    def product_url_extract(self,response):
        product_urls = response.xpath('//div[@class="products row"]/article/div/div/div/a[@class="product-flags"]/@href').extract()
        for product in product_urls:
            yield scrapy.Request(url = product,headers = self.headers,callback = self.info)

        try:
            next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
            yield scrapy.Request(url = next_page,headers = self.headers,callback = self.product_url_extract)
        except:
            pass    



    def info(self,response):
        product_title = response.xpath('//h1[@class="product_name"]/text()').extract_first()
        product_sku =  response.xpath('//div[label[contains(text(),"Reference")]]/span/text()').extract_first()
        price = response.xpath('//div[@class="current-price"]/span/text()').extract_first()
        des = " ".join(response.xpath('//div[@id="description"]/div[@class="product-description"]/p').extract())
        cleanr = re.compile('<.*?>')
        description = re.sub(cleanr, '', des)
        main_image = response.xpath('//div[@class="images-container"]/div[@class="product-cover"]/img/@src').extract_first()
        other_image = response.xpath('//div[@class="product-description"]/p/img/@src').extract()
        brand = response.xpath('//div[label[contains(text(),"Brand")]]/a/text()').extract_first()



        yield { "product_title":product_title, 
                "product_sku":product_sku,
                "price":price,
                "description":description,
                "main_image":main_image,
                "other_image":other_image,
                "brand":brand}


process = CrawlerProcess()
process.crawl(ChinaNoobWatches)
process.start()
