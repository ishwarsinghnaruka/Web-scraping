import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy_xlsx
import pandas as pd

class School(scrapy.Spider):
    name = "school_data"

    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    
    FEED_EXPORTERS = {'xlsx': 'scrapy_xlsx.XlsxItemExporter'}
    
    custom_settings = {'FEED_EXPORTERS' :FEED_EXPORTERS,'FEED_FORMAT': 'xlsx','FEED_URI': 'sool.xlsx'}

    def start_requests(self):
        url = "https://www.collegesimply.com/colleges/search?sort=&place=&fr=&fm=&gpa=&sat=&act=&admit=comp&field=&major=&radius=300&zip=&state=&size=&tuition-fees=&net-price=&start=1"
        yield scrapy.Request(url=url,headers = self.headers,callback=self.parse)

    def parse(self,response):
        colleges = response.xpath('//div[@class="w-100"]')
        
        for college in colleges:
            url = college.xpath('.//div/a[@class="tile-link"]/@href').extract_first()
            Enrollment = college.xpath('.//ul/li[contains(text(),"enrollment")]/span/text()').extract_first()
            net_price = college.xpath('.//ul/li[contains(text(),"net price")]/span/text()').extract_first()
            avg_Gpa = college.xpath('.//ul/li[contains(text(),"Avg GPA")]/span/text()').extract_first()

            yield response.follow(url= url,headers=self.headers,callback=self.info,meta = {"Enrollment":Enrollment,"net_price":net_price,"avg_Gpa":avg_Gpa})
        link = "https://www.collegesimply.com/colleges/search?sort=&place=&fr=&fm=&gpa=&sat=&act=&admit=comp&field=&major=&radius=300&zip=&state=&size=&tuition-fees=&net-price=&start={}"
        next_page = int(response.xpath('//a[@class="page-link"]/@href').extract()[-1].split("(")[1].split(")")[0])
        link_url = link.format(next_page)
        yield scrapy.Request(url = link_url,headers=self.headers,callback=self.parse)

    def info(self,response):
        Enrollment = response.meta["Enrollment"]
        net_price = response.meta["net_price"]
        avg_Gpa = response.meta["avg_Gpa"]
        Location = " ,".join(response.xpath('//tr[td[contains(text(),"Location")]]/td[2]/a/text()').extract())
        Online = " ,".join(response.xpath('//tr[td[contains(text(),"Online")]]/td[2]/a/@href').extract())
        school_type = " ,".join(response.xpath('//tr[td[contains(text(),"School Type")]]/td[2]/text()').extract())
        setting = " ,".join(response.xpath('//tr[td[contains(text(),"Setting")]]/td[2]/text()').extract())
        size = " ,".join(response.xpath('//tr[td[contains(text(),"Size")]]/td[2]/text()').extract())
        status = " ,".join(response.xpath('//tr[td[contains(text(),"Status")]]/td[2]/text()').extract())
        on_campus_housing = " ,".join(response.xpath('//tr[td[contains(text(),"On Campus Housing")]]/td[2]/text()').extract())
        level_of_study = " ,".join(response.xpath('//tr[td[contains(text(),"Level of Study")]]/td[2]/text()').extract())

        yield { "Enrollment":Enrollment, 
                "net_price":net_price,
                "avg_Gpa":avg_Gpa,
                "Location":Location,
                "Online":Online,
                "school_type":school_type,
                "setting":setting,
                "size":size,
                "status":status,
                "on_campus_housing":on_campus_housing,
                "level_of_study":level_of_study}


process = CrawlerProcess()
process.crawl(School)
process.start()
