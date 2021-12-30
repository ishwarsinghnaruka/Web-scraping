import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import scrapy_xlsx
import pandas as pd

class FahRad(scrapy.Spider):
    name = "fahrrad_data"
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    FEED_EXPORTERS = {'xlsx': 'scrapy_xlsx.XlsxItemExporter'}
    custom_settings = {'FEED_EXPORTERS' :FEED_EXPORTERS,'FEED_FORMAT': 'xlsx','FEED_URI': 'fahrrad.xlsx'}

    def start_requests(self):
        df = pd.read_excel('fahrrad-xxl-urls.xlsx')
        urls = df["Fahrrad XXL"]
        for url in urls[1:100]:
            print(url)
            yield scrapy.Request(url=url,headers = self.headers,callback=self.parse)

    def parse(self,response):
        name = response.xpath('//h1/text()').extract_first()
        try:
            price = response.xpath('//div[@class="fxxl-artikel-detail__price-and-discount"]/div[1]/div[2]/text()').extract()[-1]
        except:
            price = ""
        try:
            Akkukapa = response.xpath('//div[div[contains(text(),"Akkukapazität")]]/div[2]/text()').extract_first()
        except:
            Akkukapa = ""
        try:
            Gewicht_laut_Hersteller = response.xpath('//div[div[contains(text(),"Gewicht laut Hersteller")]]/div[2]/text()').extract_first()
        except:
            Gewicht_laut_Hersteller = ""
        try:
            Gabel = response.xpath('//div[div[contains(text(),"Gabel")]]/div[2]/text()').extract_first()
        except:
            Gabel = ""
        try:    
            Motor_Drehmoment = response.xpath('//div[div[contains(text(),"Motor Drehmoment")]]/div[2]/text()').extract_first()
        except:
            Motor_Drehmoment = ""
        try:
            Akku = response.xpath('//div[div[contains(text(),"Akku")]]/div[2]/text()').extract()[-1]
        except:
            Akku = ""
        try:
            Display = response.xpath('//div[div[contains(text(),"Display")]]/div[2]/text()').extract_first()
        except:
            Display = ""
        try:
            Ladegert = response.xpath('//div[div[contains(text(),"Ladegerät")]]/div[2]/text()').extract_first()
        except:
            Ladegert = ""
        try:
            Schaltung = response.xpath('//div[div[contains(text(),"Schaltung")]]/div[2]/text()').extract_first()
        except:
            Schaltung = ""
        try:    
            Schaltwerk = response.xpath('//div[div[contains(text(),"Schaltwerk")]]/div[2]/text()').extract_first()
        except:
            Schaltwerk = ""
        try:
            Schalthebel = response.xpath('//div[div[contains(text(),"Schalthebel")]]/div[2]/text()').extract_first()
        except:
            Schalthebel = ""
        try:
            Bremse_vorn = response.xpath('//div[div[contains(text(),"Bremse vorn")]]/div[2]/text()').extract_first()
        except:
            Bremse_vorn = ""
        try:
            Bremse_hinten = response.xpath('//div[div[contains(text(),"Bremse hinten")]]/div[2]/text()').extract_first()
        except:
            Bremse_hinten = ""
        try:
            E_Bike_Motor_Hersteller = response.xpath('//div[div[contains(text(),"E-Bike Motor Hersteller")]]/div[2]/text()').extract_first()
        except:
            E_Bike_Motor_Hersteller = ""
        try:
            E_Bike_Motorposition = response.xpath('//div[div[contains(text(),"E-Bike Motorposition")]]/div[2]/text()').extract_first()
        except:
            E_Bike_Motorposition = ""
        try:
            Marke = response.xpath('//div[div[contains(text(),"Marke")]]/div[2]/text()').extract_first()
        except:
            Marke = ""
        try:
            Rahmenform = response.xpath('//div[div[contains(text(),"Rahmenform")]]/div[2]/text()').extract_first()
        except:
            Rahmenform = ""
        try:    
            Rahmenmaterial = response.xpath('//div[div[contains(text(),"Rahmenmaterial")]]/div[2]/text()').extract_first()
        except:
            Rahmenmaterial = ""
        try:
            Saison = response.xpath('//div[div[contains(text(),"Saison")]]/div[2]/text()').extract()[-1]
        except:
            Saison = "" 
        try:
            Schaltart = response.xpath('//div[div[contains(text(),"Schaltart")]]/div[2]/text()').extract()[-1]
        except:
            Schaltart = ""
        url = response.url
        
        yield { "name":name, 
                "price":price,
                "Akkukapazität":Akkukapa,
                "Gewicht laut Hersteller":Gewicht_laut_Hersteller,
                "Gabel":Gabel,
                "Motor Drehmoment":Motor_Drehmoment,
                "Akku":Akku,
                "Display":Display,
                "Ladegerät":Ladegert,
                "Schaltung":Schaltung,
                "Schaltwerk":Schaltwerk,
                "Schalthebel":Schalthebel,
                "Bremse vorn":Bremse_vorn,
                "Bremse hinten":Bremse_hinten,
                "E-Bike Motor Hersteller":E_Bike_Motor_Hersteller,
                "E-Bike Motorposition":E_Bike_Motorposition,
                "Marke":Marke,
                "Rahmenform":Rahmenform,
                "Rahmenmaterial":Rahmenmaterial,
                "Saison":Saison,
                "Schaltart":Schaltart,
                "url":url}

process = CrawlerProcess()
process.crawl(FahRad)
process.start()