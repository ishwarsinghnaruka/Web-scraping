import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import scrapy_xlsx
import json

class Akc(scrapy.Spider):
    name = "akc_data"
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    FEED_EXPORTERS = {'xlsx': 'scrapy_xlsx.XlsxItemExporter'}
    custom_settings = {'FEED_EXPORTERS' :FEED_EXPORTERS,'FEED_FORMAT': 'xlsx','FEED_URI': 'akcdata.xlsx'}

    def start_requests(self):
        url = "https://www.akc.org/dog-breeds/"
        yield scrapy.Request(url=url,headers = self.headers,callback=self.parse)

    def parse(self,response):
        urls =  response.xpath('//div[@class="grid-col"]/div/div')
        for url in urls:
            paragraph = url.xpath('.//p/text()').extract_first()
            para_url = url.xpath('.//a/@href').extract_first()
            yield response.follow(url = para_url,headers = self.headers,callback = self.details,meta = {"paragraph":paragraph})
        next_page_url = response.xpath('//a[@id="load-more-btn"]/@href').extract_first()
        yield scrapy.Request(url=next_page_url,headers=self.headers,callback=self.parse)

    def details(self,response):
        data = json.loads(response.xpath('//script[contains(text(),"characteristic")]/text()').extract_first().split("'characteristic',")[1].split(");")[0].strip())
        group = response.xpath('//script[contains(text(),"characteristic")]/text()').extract_first().split("'group',")[1].split(");")[0].strip()
        activity_level = response.xpath('//script[contains(text(),"characteristic")]/text()').extract_first().split("activity-level-")[1].split(",")[0].strip()
        barking_level = response.xpath('//script[contains(text(),"characteristic")]/text()').extract_first().split("barking-level-")[1].split(",")[0].strip()
        characteristic = [s.replace("characteristic-","") for s in data if "characteristic-" in s]
        coat_type = response.xpath('//script[contains(text(),"characteristic")]/text()').extract_first().split("coat-type-")[1].split(",")[0].strip()
        shedding = response.xpath('//script[contains(text(),"characteristic")]/text()').extract_first().split("shedding-")[1].split(",")[0].strip()
        size =  response.xpath('//script[contains(text(),"characteristic")]/text()').extract_first().split("'size',")[1].split(");")[0].strip()
        trainability = response.xpath('//script[contains(text(),"characteristic")]/text()').extract_first().split("trainability-")[1].split("]")[0].strip()
        paragraph = response.meta["paragraph"]
        breed_name =  response.xpath('//h1/text()').extract_first().strip()
        yield { 'group': group,
                'breed_name':breed_name,
                'activity level': activity_level,
                'barking_level': barking_level,
                'characteristic':characteristic,
                'coat_type':coat_type,
                'shedding':shedding,
                'size':size,
                'trainability':trainability,
                'paragraph':paragraph}

process = CrawlerProcess()
process.crawl(Akc)
process.start()