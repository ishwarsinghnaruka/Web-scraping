import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import scrapy_xlsx

class cosme(scrapy.Spider):
    name = "cosme_data"
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    FEED_EXPORTERS = {'xlsx': 'scrapy_xlsx.XlsxItemExporter'}
    custom_settings = {'FEED_EXPORTERS' :FEED_EXPORTERS,'FEED_FORMAT': 'xlsx','FEED_URI': 'cosme.xlsx'}

    def start_requests(self):
        total_pages = 23
        for i in range(1,total_pages+1):
            url = "https://www.cosmebio.org/fr/infos-pro/annuaire-des-adherents/?name=&country=&department=&activities=&offset={}"
            url = url.format(i)
            yield scrapy.Request(url = url,headers = self.headers,callback = self.parse)

    def parse(self,response):
        urls =  response.xpath('//div[@class="subscribers__list brands__list"]/div/a/@href').extract()
        for url in urls:
            yield response.follow(url = url,headers = self.headers,callback = self.details)
        
    def details(self,response):
        company_name = response.xpath('//h1/text()').extract_first()
        address = " , ".join(response.xpath('//address/text()').extract()).strip().replace("\n","").replace("  ","")
        phone_number = response.xpath('//a[@title="Téléphone"]/text()').extract_first()
        email = response.xpath('//a[@title="Email"]/text()').extract_first()
        website =  response.xpath('//a[@title="Site-web"]/text()').extract_first()
        full_name = response.xpath('//div/div/strong/text()').extract_first()
        position = response.xpath('//div/div/span/text()').extract_first()
        phone_contact_section = response.xpath('//ul[@class="contact__list"]/li[@class="tel"]/a/text()').extract_first()
        email_contact_section = response.xpath('//ul[@class="contact__list"]/li[@class="email"]/a/text()').extract_first()
        yield { 'company_name': company_name,
                'address': address,
                'phone_number': phone_number,
                'email':email,
                'website':website,
                'full_name':full_name,
                'position':position,
                'email_contact_section':email_contact_section,
                'phone_contact_section':phone_contact_section}

process = CrawlerProcess()
process.crawl(cosme)
process.start()