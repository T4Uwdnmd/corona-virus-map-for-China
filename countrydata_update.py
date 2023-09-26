import requests
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm
from pymongo import MongoClient

# 1.读取本地json文件
filename = 'countrydata.json'
with open(filename, encoding='utf-8') as f:
    countrydata = json.load(f)

# mongodb

mongo_url = "mongodb+srv://SunSiYuan:david20020304@cluster0.tqtvmeb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_url)
db = client.coronavirus
collection = db.countrydata
collection.delete_many({})

# 4.解析各省疫情json字符串，并添加列表中 https://www.bejson.com/jsonviewernew/
statistics_data = countrydata['RECORDS']
for country in tqdm(statistics_data, "采集各省疫情数据"):
    country_total = {
        "id": country['id'],
        "confirmedCount": country['confirmedCount'],
        "confirmedIncr": country['confirmedIncr'],
        "curedCount": country['curedCount'],
        "curedIncr": country['curedIncr'],
        "currentConfirmedCount": country['currentConfirmedCount'],
        "currentConfirmedIncr": country['currentConfirmedIncr'],
        "dateId": country['dateId'],
        "deadCount": country['deadCount'],
        "deadIncr": country['deadIncr'],
        "suspectedCount": country['suspectedCount'],
        "suspectedCountIncr": country['suspectedCountIncr'],
        "countryName": country['countryName'],
        "countryShortCode": country['countryShortCode'],
        "continent": country['continent'],
        "countryFullName": country['countryFullName']
    }
    collection.insert_one(country_total)
print(collection.count_documents({}))