import scrapy


class GlassesSpider(scrapy.Spider):
    name = 'glasses'
    allowed_domains = ['apollo.de']
    start_urls = ['http://apollo.de/']

    def parse(self, response):
        links =  response.xpath('//a[@itemprop = "url"]/@href').extract()
        for link in links:
            absolute_url = "https://www.apollo.de/" + link
            yield scrapy.Request(absolute_url,callback=self.parse_product)

    def parse_product(self,response):
        GTIN =  response.xpath('//h1[@class = "c-heading-alpha c-product-name__title"]/text()').extract()[1]
        b = response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[0]
        c =  response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[1]
        d = response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[2]
        Material =  response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[3]
        Typ = response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[4]
        Form = response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[5]
        Frontfarbe =  response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[6]
        e =  response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[7]
        Scharniertyp = response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[8]
        f =  response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[9]
        g = response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[10]
        EAN = response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[11]
        h =  response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[12]
        Scheibenbreite = response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[13]
        Nasenstegweite = response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[14]
        i =  response.xpath('//h3[@class="c-heading-gamma c-product-detail-block__description"]/text()').extract()[15]

        yield {"GTIN":GTIN,"Geschlecht":b,"Geeignet für":c,"Brillengröße":d,"Material":Material,"Typ":Typ,"Form":Form,"Frontfarbe":Frontfarbe,
                "Bügelfarbe":e,"Scharniertyp":Scharniertyp,"Gleitsichtfähig":f,"Filter-Kategorie":g,"EAN":EAN,"Scheibenhöhe":h,
                "Scheibenbreite":Scheibenbreite,"Nasenstegweite":Nasenstegweite,"Bügellänge":i}
