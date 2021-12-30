import scrapy
from scrapy.crawler import CrawlerProcess
import csv
class GetApp(scrapy.Spider):
    name = "getapp_data"
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    custom_settings = {'FEED_FORMAT': 'csv','FEED_URI': 'getapp.csv'}

    def start_requests(self):
        urls = ['https://www.getapp.com/collaboration-software/remote-work/',
             'https://www.getapp.com/customer-management-software/crm/',
             'https://www.getapp.com/education-childcare-software/learning-management-system-lms/',
             'https://www.getapp.com/education-childcare-software/school-management/',
             'https://www.getapp.com/finance-accounting-software/',
             'https://www.getapp.com/healthcare-pharmaceuticals-software/telemedicine/',
             'https://www.getapp.com/hr-employee-management-software/applicant-tracking/',
             'https://www.getapp.com/it-communications-software/emergency-notification/',
             'https://www.getapp.com/it-communications-software/online-meetings/',
             'https://www.getapp.com/it-communications-software/video-conferencing/',
             'https://www.getapp.com/it-communications-software/web-conferencing/',
             'https://www.getapp.com/it-communications-software/webinars/',
             'https://www.getapp.com/operations-management-software/field-service-management/',
             'https://www.getapp.com/project-management-planning-software/project-management/',
             'https://www.getapp.com/security-software/backup/',
             'https://www.getapp.com/security-software/cloud-security/',
             'https://www.getapp.com/website-ecommerce-software/',
             'https://www.getapp.com/security-software/gdpr-compliance/',
             'https://www.getapp.com/hr-employee-management-software/payroll/',
             'https://www.getapp.com/collaboration-software/document-management/',
             'https://www.getapp.com/operations-management-software/contract-management',
             'https://www.getapp.com/hr-employee-management-software/performance-management-appraisal/',
             'https://www.getapp.com/security-software/vpn/',
             'https://www.getapp.com/collaboration-software',
             'https://www.getapp.com/collaboration-software/file-sharing-api',
             'https://www.getapp.com/marketing-software/marketing-automation/',
             'https://www.getapp.com/project-management-planning-software/time-tracking-expense',
             'https://www.getapp.com/hr-employee-management-software/training/',
             'https://www.getapp.com/it-communications-software/communication/',
             'https://www.getapp.com/it-management-software/devops/',
             'https://www.getapp.com/customer-service-support-software/customer-service/',
             'https://www.getapp.com/finance-accounting-software/payment-management',
             'https://www.getapp.com/hr-employee-management-software/',
             'https://www.getapp.com/sales-software/',
             'https://www.getapp.com/collaboration-software/cloud-storage/',
             'https://www.getapp.com/collaboration-software/productivity/',
             'https://www.getapp.com/hr-employee-management-software/training/',
             'https://www.getapp.com/operations-management-software/digital-signatures/',
             'https://www.getapp.com/marketing-software/social-media/',
             'https://www.getapp.com/marketing-software/lead-generation/']
        for url in urls:
            yield scrapy.Request(url=url,headers = self.headers,callback=self.parse)

    def parse(self,response):
        product_logo = response.xpath('//img[@class="listing-logo-img"]/@src').extract()[::2]
        product_names = response.xpath('//h2/a/text()').extract()[::2]
        product_titles = response.xpath('//div[@class="listing-tagline mb-md-1"]/text()').extract()[::2]
        product_subtitles =  response.xpath('//div[@class="listing-overview-expand"]/span/text()').extract()[::2]  
        apps_url =  response.xpath('//a[contains(text(),"Read more")]/@href').extract()[::2]
        for i in range(len(apps_url)):
            logo = product_logo[i]
            product_name = product_names[i]
            product_title = product_titles[i]
            product_subtitle = product_subtitles[i]
            app = apps_url[i]
            yield response.follow(url=app,headers=self.headers,callback=self.details,meta = {"Product_logo":logo,"Product_name":product_name,"Product_title":product_title,
                                    "Product_subtitle":product_subtitle})

        nex_page = response.xpath('//a[@data-evac="ua_pagination"]/@href').extract()[-2]
        yield response.follow(url=nex_page,headers=self.headers,callback=self.parse)

    def details(self,response):
        rating_stars = response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first()
        try:
            number_of_ratings = int(response.xpath('//a[@data-evla="text-link_number-reviews"]/text()').extract_first().split()[0].replace(",",""))
        except:
            number_of_ratings = ""
        try:
            price = response.xpath('//div[h4[contains(text(),"Pricing")]]/div[1]/div/text()')[-1].extract().split("/")[0]
        except:
            try:
                price = response.xpath('//div[h4[contains(text(),"Pricing")]]/div[1]/div/text()')[-1].extract()
            except:
                price = ""
        yield {"Product_logo":response.meta["Product_logo"],
               "Product_name":response.meta["Product_name"],
               "Product_title":response.meta["Product_title"],
               "Product_subtitle":response.meta["Product_subtitle"],
               "rating_stars":rating_stars,
               "number_of_ratings":number_of_ratings,
               "price":price}

process = CrawlerProcess()
process.crawl(GetApp)
process.start()