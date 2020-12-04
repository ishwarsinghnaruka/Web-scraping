import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy_xlsx
import json
import requests

class Axial(scrapy.Spider):
    name = "axial_data"
    
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    
    
    custom_settings = {'FEED_FORMAT': 'csv','FEED_URI': 'axial.csv'}

    def start_requests(self):
        url = "https://www.axial.net/forum/companies/private-equity-firms/"
        yield scrapy.Request(url=url,headers = self.headers,callback=self.parse)

    def parse(self,response):
        url = "https://www.axial.net/forum/companies/private-equity-firms/"
        pages = int(response.xpath('//li[@class = "-page"]/a/span/text()').extract()[1])
        for page in range(1,pages+1):
            page_url = url + "{}/".format(page)
            yield scrapy.Request(url = page_url,headers = self.headers,callback = self.details)

    def details(self,response):
        data =  response.xpath('//article[@class="teaser1"]/a/@href').extract()
        for dt in data:
            page_url = "https://api.axial.net/account/accounts/?slug={}".format(dt.replace("https://network.axial.net/company/",""))
            yield scrapy.Request(url = page_url,headers = {"authority": "api.axial.net","accept": "application/json;v=1","accept-encoding": "gzip, deflate, br",
                "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,hi;q=0.7","referer": "https://network.axial.net/","sec-fetch-dest": "empty","sec-fetch-mode": "core",
                "sec-fetch-site": "same-site","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"},callback = self.data_parse)

    def data_parse(self,response):
        data = json.loads(response.body)
        Overview = data['data'][0]['description'].strip()
        website = data['data'][0]['website']
        Firm_name = data['data'][0]['name']
        Category = data['data'][0]['account_type']
        ids = data['data'][0]['id']
        dat = requests.get("https://api.axial.net/account/accounts/{}/industries".format(ids))
        dat = dat.json()
        Industries = []
        for i in dat['data']:
            Industries.append(i['name'])
        tms = requests.get("https://api.axial.net/account/accounts/{}/members?is_active=false".format(ids))
        tms = tms.json()
        teams = []
        for i in tms['data']:
            teams.append([{"first_name":i['first_name'],"last_name":i["last_name"],"title":i["title"]}])
        yield {"Overview":Overview,"website":website,"Firm_name":Firm_name,"Category":Category,"Industries":Industries,"teams":teams}




process = CrawlerProcess()
process.crawl(Axial)
process.start()