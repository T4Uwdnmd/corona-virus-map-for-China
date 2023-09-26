import requests
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm
from pymongo import MongoClient

# 1.读取本地json文件
filename = 'china_provincedata.json'
with open(filename, encoding='utf-8') as f:
    chinaprovince = json.load(f)

# mongodb

mongo_url = "mongodb+srv://SunSiYuan:david20020304@cluster0.tqtvmeb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_url)
db = client.coronavirus
collection = db.chinaprovince
collection.delete_many({})

# 4.解析各省疫情json字符串，并添加列表中 https://www.bejson.com/jsonviewernew/
statistics_data = chinaprovince['RECORDS']
for province in tqdm(statistics_data, "采集各省疫情数据"):
    province_total = {
        "id": province['id'],
        "confirmedCount": province['confirmedCount'],
        "confirmedIncr": province['confirmedIncr'],
        "curedCount": province['curedCount'],
        "curedIncr": province['curedIncr'],
        "currentConfirmedCount": province['currentConfirmedCount'],
        "currentConfirmedIncr": province['currentConfirmedIncr'],
        "dateId": province['dateId'],
        "deadCount": province['deadCount'],
        "deadIncr": province['deadIncr'],
        "suspectedCount": province['suspectedCount'],
        "suspectedCountIncr": province['suspectedCountIncr'],
        "provinceName": province['provinceName'],
        "provinceShortName": province['provinceShortName']
    }
    collection.insert_one(province_total)
print(collection.count_documents({}))