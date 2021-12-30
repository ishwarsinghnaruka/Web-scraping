import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import scrapy_xlsx
import json

class PhilaGov(scrapy.Spider):
    name = "philagov_data"
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    FEED_EXPORTERS = {'xlsx': 'scrapy_xlsx.XlsxItemExporter'}
    custom_settings = {'FEED_EXPORTERS' :FEED_EXPORTERS,'FEED_FORMAT': 'xlsx','FEED_URI': 'phila_total.xlsx'}

    def start_requests(self):
        b = 1
        while b<=581466:
            url = "https://phl.carto.com/api/v2/sql?q=select+*+from+opa_properties_public_pde+WHERE+cartodb_id+IN+({})".format(b)
            b = b+1
            yield scrapy.Request(url=url,headers = self.headers,callback=self.parse)

    def parse(self,response):
        data = json.loads(response.text)["rows"]
        for dt in data:
            cartodb_id = dt['cartodb_id']
            the_geom = dt['the_geom']
            the_geom_webmercator = dt['the_geom_webmercator']
            address_std = dt['address_std']
            assessment_date = dt['assessment_date']
            basements = dt['basements']
            beginning_point = dt['beginning_point']
            book_and_page = dt['book_and_page']
            building_code = dt['building_code']
            building_code_description = dt['building_code_description']
            category_code = dt['category_code']
            category_code_description = dt['category_code_description']
            census_tract = dt['census_tract']
            central_air = dt['central_air']
            council_district_2016 = dt['council_district_2016']
            cross_reference = dt['cross_reference']
            date_exterior_condition = dt['date_exterior_condition']
            depth = dt['depth']
            elementary_school = dt['elementary_school']
            exempt_building = dt['exempt_building']
            exempt_land = dt['exempt_land']
            exterior_condition = dt['exterior_condition']
            fireplaces  = dt["fireplaces"]
            frontage  = dt["frontage"]
            garage_spaces  = dt["garage_spaces"]
            garage_type  = dt["garage_type"]
            general_construction  = dt["general_construction"]
            geocode_lat  = dt["geocode_lat"]
            geocode_lon  = dt["geocode_lon"]
            high_school  = dt["high_school"]
            homestead_exemption  = dt["homestead_exemption"]
            house_extension  = dt["house_extension"]
            house_number  = dt["house_number"]
            interior_condition  = dt["interior_condition"]
            location  = dt["location"]
            mailing_address_1  = dt["mailing_address_1"]
            mailing_address_2  = dt["mailing_address_2"]
            mailing_care_of  = dt["mailing_care_of"]
            mailing_city_state  = dt["mailing_city_state"]
            mailing_street  = dt["mailing_street"]
            mailing_zip  = dt["mailing_zip"]
            market_value  = dt["market_value"]
            market_value_date  = dt["market_value_date"]
            middle_school  = dt["middle_school"]
            number_of_bathrooms  = dt["number_of_bathrooms"]
            number_of_bedrooms  = dt["number_of_bedrooms"]
            number_of_rooms  = dt["number_of_rooms"]
            number_stories  = dt["number_stories"]
            off_street_open  = dt["off_street_open"]
            other_building  = dt["other_building"]
            owner_1  = dt["owner_1"]
            owner_2  = dt["owner_2"]
            parcel_number  = dt["parcel_number"]
            parcel_shape  = dt["parcel_shape"]
            police_district  = dt["police_district"]
            political_district  = dt["political_district"]
            political_ward  = dt["political_ward"]
            pwd_parcel_id  = dt["pwd_parcel_id"]
            quality_grade  = dt["quality_grade"]
            recording_date  = dt["recording_date"]
            registry_number  = dt["registry_number"]
            sale_date  = dt["sale_date"]
            sale_price  = dt["sale_price"]
            separate_utilities  = dt["separate_utilities"]
            site_type  = dt["site_type"]
            state_code  = dt["state_code"]
            street_code  = dt["street_code"]
            street_designation  = dt["street_designation"]
            street_direction  = dt["street_direction"]
            street_name  = dt["street_name"]
            suffix  = dt["suffix"]
            taxable_building  = dt["taxable_building"]
            taxable_land  = dt["taxable_land"]
            topography  = dt["topography"]
            total_area  = dt["total_area"]
            total_livable_area  = dt["total_livable_area"]
            type_heater  = dt["type_heater"]
            unfinished  = dt["unfinished"]
            unit  = dt["unit"]
            view_type  = dt["view_type"]
            year_built  = dt["year_built"]
            year_built_estimate  = dt["year_built_estimate"]
            zip_code  = dt["zip_code"]
            zoning  = dt["zoning"]
            objectid  = dt["objectid"]
    
        yield { "cartodb_id" : cartodb_id,
                "the_geom" : the_geom,
                "the_geom_webmercator" : the_geom_webmercator,
                "address_std" : address_std,
                "assessment_date" : assessment_date,
                "basements" : basements,
                "beginning_point" : beginning_point,
                "book_and_page" : book_and_page,
                "building_code" : building_code,
                "building_code_description" : building_code_description,
                "category_code" : category_code,
                "category_code_description" : category_code_description,
                "census_tract" : census_tract,
                "central_air" : central_air,
                "council_district_2016" : council_district_2016,
                "cross_reference" : cross_reference,
                "date_exterior_condition" : date_exterior_condition,
                "depth" : depth,
                "elementary_school" : elementary_school,
                "exempt_building" : exempt_building,
                "exempt_land" : exempt_land,
                "exterior_condition" : exterior_condition,
                "fireplaces" : fireplaces,
                "frontage" : frontage,
                "garage_spaces" : garage_spaces,
                "garage_type" : garage_type,
                "general_construction" : general_construction,
                "geocode_lat" : geocode_lat,
                "geocode_lon" : geocode_lon,
                "high_school" : high_school,
                "homestead_exemption" : homestead_exemption,
                "house_extension" : house_extension,
                "house_number" : house_number,
                "interior_condition" : interior_condition,
                "location" : location,
                "mailing_address_1" : mailing_address_1,
                "mailing_address_2" : mailing_address_2,
                "mailing_care_of" : mailing_care_of,
                "mailing_city_state" : mailing_city_state,
                "mailing_street" : mailing_street,
                "mailing_zip" : mailing_zip,
                "market_value" : market_value,
                "market_value_date" : market_value_date,
                "middle_school" : middle_school,
                "number_of_bathrooms" : number_of_bathrooms,
                "number_of_bedrooms" : number_of_bedrooms,
                "number_of_rooms" : number_of_rooms,
                "number_stories" : number_stories,
                "off_street_open" : off_street_open,
                "other_building" : other_building,
                "owner_1" : owner_1,
                "owner_2" : owner_2,
                "parcel_number" : parcel_number,
                "parcel_shape" : parcel_shape,
                "police_district" : police_district,
                "political_district" : political_district,
                "political_ward" : political_ward,
                "pwd_parcel_id" : pwd_parcel_id,
                "quality_grade" : quality_grade,
                "recording_date" : recording_date,
                "registry_number" : registry_number,
                "sale_date" : sale_date,
                "sale_price" : sale_price,
                "separate_utilities" : separate_utilities,
                "site_type" : site_type,
                "state_code" : state_code,
                "street_code" : street_code,
                "street_designation" : street_designation,
                "street_direction" : street_direction,
                "street_name" : street_name,
                "suffix" : suffix,
                "taxable_building" : taxable_building,
                "taxable_land" : taxable_land,
                "topography" : topography,
                "total_area" : total_area,
                "total_livable_area" : total_livable_area,
                "type_heater" : type_heater,
                "unfinished" : unfinished,
                "unit" : unit,
                "view_type" : view_type,
                "year_built" : year_built,
                "year_built_estimate" : year_built_estimate,
                "zip_code" : zip_code,
                "zoning" : zoning,
                "objectid" : objectid}

process = CrawlerProcess()
process.crawl(PhilaGov)
process.start()