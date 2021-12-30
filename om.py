import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import scrapy_xlsx
import re

class OlaRm(scrapy.Spider):
    name = "olarm_data"
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    FEED_EXPORTERS = {'xlsx': 'scrapy_xlsx.XlsxItemExporter'}
    custom_settings = {'FEED_EXPORTERS' :FEED_EXPORTERS,'FEED_FORMAT': 'xlsx','FEED_URI': 'olarm.xlsx'}

    def start_requests(self):
        url = "https://www.olarm.co/resellers"
        yield scrapy.Request(url=url,headers = self.headers,callback=self.parse)

    def parse(self,response):
        urls = response.xpath('//a[@class="apg-grid-item"]/@href').extract()
        for url in urls:
            yield scrapy.Request(url = url,headers = self.headers,callback = self.details)

    def details(self,response):
        data = response.xpath('//div[@class="row"]')
        for dt in data:
            a = dt.xpath('.//div[@class="column"]')
            if len(a)==3:
                town = a[0].xpath('.//span/text()').extract_first()
                company = a[1].xpath('.//span/text()').extract_first()
                b = a[2].xpath('.//p').extract_first()
                s = re.sub('<[^>]+>', ',', b).replace(",","split").split("split")
                z = []
                for i in s:
                    if len(i)>3:
                        z.append(i)
                # try:
                # address = z[0]
                # email = z[1]
                # phone = z[2]
                if len(z)==3:
                    address = z[0]
                    email = z[1]
                    phone = z[2]
                else:
                    try:

                        for i in z:
                            if (i.find('@')!=-1) or (i.find('.co')!=-1):
                                email = i
                            elif i.replace(" ","").isdigit():
                                phone = i
                            else:
                                address = i
                        if len(address)<4:
                            address = " "
                        if len(email)<4:
                            email = " "
                        if len(phone)<4:
                            phone = " "

                    except:
                        address = " "
                        email = " "
                        phone = " "

                yield  {'town': town,
                        'company': company,
                        'address': address,
                        'email':email,
                        'phone':phone}
        
process = CrawlerProcess()
process.crawl(OlaRm)
process.start()