from typing import Type
import scrapy
import json
from fluc.items import FlucItem
import re

class FlucSpider(scrapy.Spider):
    name="fluc"
    start_urls=['http://flex.at/flex_frontend/index.php?selected=programm&mode=11&id=1171']

    def parse(self, response):
        item = FlucItem()
        item['title'] = response.xpath('//table[@class="halle"]//*/text()').getall()

        with open("data_file.json", "w") as filee:
            json.dump(item['title'], filee)

        clearstring=ClearDataString('data_file.json')
        print(clearstring)
        daylist=DayList(clearstring)
        #print(daylist)
        finished_data=JsonList(daylist)
        #print(finished_data)
        WriteJson(finished_data)


def ClearDataString(json_path):
    strdata=str(json.load(open(json_path))) 
    strdata=re.sub(r"\\n|\\t| |\\xa0","",strdata)
    strdata=re.sub(r"'',","",strdata)
    strdata=re.sub(r"'","",strdata)
    #strdata=re.sub(r","," ",strdata)
    return strdata

def DayList(clearstring):
    #data=re.split(",Montag,|,Dienstag,|,Mittwoch,|,Donnerstag,|,Freitag,|,Samstag,|,Sonntag,",clearstring)
    #for d in data:
    clear_data=clearstring.split(',')
    return clear_data

def JsonList(daylist):
    finished_data={}
    finished_data["data"]=[]
    finished_data['data'].append({
    'EventName:': daylist[1],
    'Beginn:': daylist[0][2:]
    })
    return finished_data

def WriteJson(finished_data):
    with open("data_file_finish.json", "a") as filee:
        json.dump(finished_data, filee)