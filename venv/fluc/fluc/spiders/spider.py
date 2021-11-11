from typing import Type
import scrapy
import json
from fluc.items import FlucItem
import re

class FlucSpider(scrapy.Spider):
    name="fluc"
    start_urls=['https://www.fluc.at/programm/2021_Flucwoche10.html']

    def parse(self, response):
        item = FlucItem()
        item['title'] = response.xpath('//text()').getall()

        with open("data_file.json", "w") as filee:
            json.dump(item['title'], filee)

        clearstring=ClearDataString('data_file.json')
        #print(clearstring)
        daylist=DayList(clearstring)
        #print(daylist)
        finished_data=JsonList(daylist)
        print(finished_data)
        WriteJson(finished_data)



def ClearDataString(json_path):
    strdata=str(json.load(open(json_path))) 
    strdata=re.sub(r"\\n|\\t| |\\xa0","",strdata)
    strdata=re.sub(r"'',","",strdata)
    strdata=re.sub(r"'","",strdata)
    #strdata=re.sub(r","," ",strdata)
    return strdata

def DayList(clearstring):
    clear_data=[]
    data=re.split(",Montag,|,Dienstag,|,Mittwoch,|,Donnerstag,|,Freitag,|,Samstag,|,Sonntag,",clearstring)
    for d in data:
        clear_data.append(d.split(','))
    return clear_data

def JsonList(daylist):
    finished_data={}
    finished_data["data"]=[]
    for i in range(len(daylist)):
        if i!=0:
            date=daylist[i][0]+" "+weekyear
            right=""
            left=""
            rightbool=False
            for ii in range(len(daylist[i])):
                if ii!=0:
                    if rightbool==False:
                        if re.search("fluc_wanne",daylist[i][ii])==None:
                            left+=daylist[i][ii]+" "
                        else:
                            rightbool=True
                    else:
                        right+=daylist[i][ii]+" "
            if re.search("&nbsp",left)==None:
                finished_data['data'].append({
                'EventName:': left,
                'Beginn:': date,
                'Ort:': "Fluc"
                })
            if right!="":
                finished_data['data'].append({
                'EventName:': right,
                'Beginn:': date,
                'Ort:': "Fluc_Wanne"
                })
        else:
            weekyear=daylist[0][1]
    return finished_data

def WriteJson(finished_data):
    with open("data_file_finish.json", "a") as filee:
        json.dump(finished_data, filee)