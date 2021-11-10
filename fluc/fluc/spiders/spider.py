import scrapy
import json
from fluc.items import FlucItem
import re

class flucSpider(scrapy.Spider):
    name="fluc"
    start_urls=[
        'https://www.fluc.at/programm/2021_Flucwoche25.html']

    def parse(self, response):
        item = FlucItem()
        item['title'] = response.xpath('//text()').getall()

        with open("data_file.json", "w") as filee:
            json.dump(item['title'], filee)

        data=(json.load(open('data_file.json'))) 
        strdata=str(data)
        strdata=re.sub(r"\\n|\\t| ","",strdata)
        strdata=re.sub(r"'',","",strdata)
        strdata=re.sub(r",''","",strdata)
        print(strdata)
        #data2=data.split(',')
        #print(data2)
        #strdata=str(data)
        #data=re.split("\t",strdata)
        #print(data2)
        #with open("data_file2.json", "w") as filee:
        #    json.dump(data2,filee)
