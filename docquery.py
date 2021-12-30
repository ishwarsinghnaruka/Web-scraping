import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import scrapy_xlsx

class DocQuery(scrapy.Spider):
    name = "docquery_data"
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    FEED_EXPORTERS = {'xlsx': 'scrapy_xlsx.XlsxItemExporter'}
    custom_settings = {'FEED_EXPORTERS' :FEED_EXPORTERS,'FEED_FORMAT': 'xlsx','FEED_URI': 'docquery.xlsx'}
                       # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1,'DOWNLOAD_DELAY': 2}

    def start_requests(self):
        url = "https://docquery.fec.gov/cgi-bin/forms/C00580100/1440266/sa/ALL/1"
        yield scrapy.Request(url=url,headers = self.headers,callback=self.parse)

    def parse(self,response):
        data =  response.xpath('//table[@id="sadetails"]/tbody/tr')
        for dt in data:
            Contributor_Name = " , ".join(dt.xpath('.//td[1]/text()').extract()).strip()
            Contributor_Address = " , ".join(dt.xpath('.//td[2]/text()').extract()).strip()
            Occupation = " , ".join(dt.xpath('.//td[3]/text()').extract()).strip()
            description = " , ".join(dt.xpath('.//td[4]/text()').extract()).strip()
            memo = " , ".join(dt.xpath('.//td[5]/text()').extract()).strip()
            text =  " , ".join(dt.xpath('.//td[6]/text()').extract()).strip()
            date = " , ".join(dt.xpath('.//td[7]/text()').extract()).strip()
            amount = " , ".join(dt.xpath('.//td[8]/text()').extract()).strip()
            aggregate =  " , ".join(dt.xpath('.//td[9]/text()').extract()).strip()
            limits = " , ".join(dt.xpath('.//td[10]/text()').extract()).strip()

            yield {"Contributor_Name":Contributor_Name,
                    "Contributor_Address":Contributor_Address,
                    "Occupation":Occupation,
                    "description":description,
                    "memo":memo,
                    "text":text,
                    "date":date,
                    "amount":amount,
                    "aggregate":aggregate,
                    "limits":limits}
        next_page = response.xpath('//div[@id="pagination"]/ul/li/font/a[contains(text()," Next Page ")]/@href').extract_first()
        yield response.follow(url = next_page,headers=self.headers,callback = self.parse)

process = CrawlerProcess()
process.crawl(DocQuery)
process.start()