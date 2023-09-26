#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/26 14:48
# @Author : way
# @Site :
# @Describe:
from pymongo import MongoClient
import json
from flask import Flask,render_template,request,Response,redirect,url_for
app = Flask(__name__)
from sklearn.linear_model import  LinearRegression



class SourceDataDemo:

    def __init__(self):
        self.title = '疫情大数据可视化展板'
        # 两个小的form看板
        self.client = MongoClient(
            "mongodb+srv://SunSiYuan:david20020304@cluster0.tqtvmeb.mongodb.net/")
        self.db = self.client.coronavirus
        self.collection1 = self.db.chinaprovince
        self.chinaprovincecusor = self.collection1.find().sort('dataID')
        self.collection2 = self.db.countrydata
        self.countrydatacusor = self.collection2.find().sort('dataID')
        self.outputapp = []
        self.data_list1 = []
        self.data_list2 = []
        self.data_list3_1 = [{"name": "0", "value": 0},
                             {"name": "1-99", "value": 0},
                             {"name": "100-999", "value": 0},
                             {"name": "1000-9999", "value": 0},
                             {"name": "10000以上", "value": 0}]
        self.data_list3_2 = [{"name": "0", "value": 0},
                             {"name": "1-99", "value": 0},
                             {"name": "100-999", "value": 0},
                             {"name": "1000-9999", "value": 0},
                             {"name": "10000以上", "value": 0}]
        self.data_list3_3 = [{"name": "0", "value": 0},
                             {"name": "1-99", "value": 0},
                             {"name": "100-999", "value": 0},
                             {"name": "1000-9999", "value": 0},
                             {"name": "10000以上", "value": 0}]

        self.data_list4 = []
        self.data_list5 = []
        self.data_list6 = []

        self.data_dict1 = {}
        self.data_dict2 = {}
        self.data_dict3 = {}
        self.data_dict4 = {}
        self.count1 = 0
        self.count2 = 0
        for s in self.chinaprovincecusor:
            if s['dateId']== '20200702':
                self.count1 += int(s['currentConfirmedCount'])
                self.count2 += int(s['confirmedCount'])
                self.data_list1.append({'name': s['provinceShortName'], 'value': int(s['currentConfirmedCount'])})
                if int(s['currentConfirmedCount'])==0:
                    self.data_list3_1[0]['value'] += 1
                if 100>int(s['currentConfirmedCount'])>0:
                    self.data_list3_1[1]['value'] += 1
                if 1000>int(s['currentConfirmedCount'])>99:
                    self.data_list3_1[2]['value'] += 1
                if 10000>int(s['currentConfirmedCount'])>999==0:
                    self.data_list3_1[3]['value'] += 1
                if int(s['currentConfirmedCount'])>9999==0:
                    self.data_list3_1[4]['value'] += 1

                if int(s['confirmedCount'])==0:
                    self.data_list3_2[0]['value'] += 1
                if 100>int(s['confirmedCount'])>0:
                    self.data_list3_2[1]['value'] += 1
                if 1000>int(s['confirmedCount'])>99:
                    self.data_list3_2[2]['value'] += 1
                if 10000>int(s['confirmedCount'])>999==0:
                    self.data_list3_2[3]['value'] += 1
                if int(s['confirmedCount'])>9999==0:
                    self.data_list3_2[4]['value'] += 1

                if int(s['curedCount'])==0:
                    self.data_list3_3[0]['value'] += 1
                if 100>int(s['curedCount'])>0:
                    self.data_list3_3[1]['value'] += 1
                if 1000>int(s['curedCount'])>99:
                    self.data_list3_3[2]['value'] += 1
                if 10000>int(s['curedCount'])>999==0:
                    self.data_list3_3[3]['value'] += 1
                if int(s['curedCount'])>9999==0:
                    self.data_list3_3[4]['value'] += 1

                if s['provinceShortName'] == '北京':
                    self.data_list6.append({'name': s['provinceShortName'], 'value': int(s['currentConfirmedCount']),"value2":400-int(s['currentConfirmedCount']),"color": '01',"radius": ['59%', '70%']})
                if s['provinceShortName'] == '天津':
                    self.data_list6.append({'name': s['provinceShortName'], 'value': int(s['currentConfirmedCount']),"value2":400-int(s['currentConfirmedCount']),"color": '02',"radius": ['49%', '60%']})
                if s['provinceShortName'] == '上海':
                    self.data_list6.append({'name': s['provinceShortName'], 'value': int(s['currentConfirmedCount']),"value2":400-int(s['currentConfirmedCount']),"color": '03',"radius": ['39%', '50%']})
                if s['provinceShortName'] == '重庆':
                    self.data_list6.append({'name': s['provinceShortName'], 'value': int(s['currentConfirmedCount']),"value2":400-int(s['currentConfirmedCount']),"color": '04',"radius": ['29%', '40%']})

            if s['provinceShortName'] == "北京" and (s['dateId'][5] == '6' or s['dateId'][5] == '5'):
                self.data_dict3.setdefault(s['provinceShortName'], []).append(int(s['currentConfirmedCount']))
                self.data_dict4.setdefault(s['provinceShortName'], []).append(int(s['dateId']))

        for u in self.countrydatacusor:
            if u['dateId']== '20200702':
                self.data_list5.append({'name': u['countryName'], 'value': int(u['currentConfirmedCount'])})
            if  u["countryName"]== "中国" and (u['dateId'][5] == '6' or u['dateId'][5] == '5'):
                self.data_dict1.setdefault(u['countryName'], []).append(int(u['currentConfirmedCount']))
                self.data_dict2.setdefault(u['countryName'],[]).append(int(u['dateId']))
        for v in self.data_dict3.items():
            self.data_list4.append({'name': v[0], 'value': v[1]})

        self.regr = LinearRegression()
        self.x=[]
        self.y=[]
        for l in range(0,8):
            self.x.append(self.data_dict1['中国'][(len(self.data_dict1['中国'])//10)*l:(len(self.data_dict1['中国'])//10)*(l+1)-1])
            self.y.append(self.data_dict1['中国'][(len(self.data_dict1['中国'])//10)*(l+1):((len(self.data_dict1['中国'])//10)*(l+1))+7])
        self.regr.fit(self.x,self.y)
        self.data_list21=self.regr.predict([self.data_dict1['中国'][(len(self.data_dict1['中国'])//10)*9:(len(self.data_dict1['中国'])//10)*(10)-1]])
        self.data_list2.append({'name': '中国', 'value': list(list(self.data_list21)[0])})

        self.counter = {'name': '全国现有确诊人数', 'value': self.count1}
        self.counter2 = {'name': '全国累计确诊人数', 'value': self.count2}
        # 总共是6个图表，数据格式用json字符串，其中第3个图表是有3个小的图表组成的



        #全国前八省份疫情分布
        self.data_list1=sorted(self.data_list1,key=lambda x:x['value'],reverse=True)
        self.echart1_data = {
            'title': '全国现有确诊前八省份分布',
            'data':self.data_list1[0:8]
        }
        #全国疫情死亡人数身份分布
        self.echart2_data = {'title': '中国未来七天疫情趋势预测',
            'data': self.data_list2,
            'xAxis':['01', '02', '03', '04', '05', '06', '07']
        }

        self.echarts3_1_data = {
            'title': '当日现有确诊区间分布',
            'data': self.data_list3_1
        }
        self.echarts3_2_data = {
            'title': '累计确诊区间分布',
            'data': self.data_list3_2
        }
        self.echarts3_3_data = {
            'title': '累计治愈区间分布',
            'data': self.data_list3_3
        }

        self.echart4_data = {
            'title': '近两月北京疫情趋势图',
            'data': self.data_list4
            ,
            'xAxis': self.data_dict4["北京"],
        }

        self.data_list5=sorted(self.data_list5,key=lambda x:x['value'],reverse=True)
        self.echart5_data = {
            'title': '全球现有确诊前八国家分布',
            'data': self.data_list5[0:8]
        }
        # 这是一个环状图，有颜色的加上没颜色的正好等于100，半径是外圈直径和内圈直径，猜测是左闭右开
        self.echart6_data = {
            'title': '直辖市现有确诊分布情况',
            'data': self.data_list6
        }
        # 这个在哪里用了？？？
        self.map_1_data = {
            'symbolSize': 1000,
            'data': [
                {'name': '海门', 'value': 239},
                {'name': '鄂尔多斯', 'value': 231},
                {'name': '招远', 'value': 203},
            ]
        }

    @property
    def echart1(self):
        data = self.echart1_data
        echart = {
            'title': data.get('title'),
            # 第一次get获取到的是许多键值对，所以需要对每个键值对再次get
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')]
        }
        # 返回的是标题和对应的数据，并没有说用什么方式展现！
        return echart

    @property
    def echart2(self):
        data = self.echart2_data
        echart = {
            'title': data.get('title'),
            'names': [i.get("name") for i in data.get('data')],
            'xAxis': data.get('xAxis'),
            'data': data.get('data'),
        }
        return echart

    @property
    def echarts3_1(self):
        data = self.echarts3_1_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echarts3_2(self):
        data = self.echarts3_2_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echarts3_3(self):
        data = self.echarts3_3_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echart4(self):
        data = self.echart4_data
        echart = {
            'title': data.get('title'),
            'names': [i.get("name") for i in data.get('data')],
            'xAxis': data.get('xAxis'),
            'data': data.get('data'),
        }
        return echart

    @property
    def echart5(self):
        data = self.echart5_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echart6(self):
        data = self.echart6_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def map_1(self):
        data = self.map_1_data
        echart = {
            'symbolSize': data.get('symbolSize'),
            'data': data.get('data'),
        }
        return echart


class SourceData(SourceDataDemo):

    def __init__(self):
        """
        按照 SourceDataDemo 的格式覆盖数据即可
        """
        super().__init__()
        self.title = '疫情大数据展板'

# @app.route('/')
# def index():
#     # 新建一个实例
#     data = SourceData()
#     # 传入一个实例，和实例的标题
#     return render_template('index_ajax.html', form=data, title=data.title)
#
# if __name__ == "__main__":
#     app.run(host='127.0.0.1', debug=True)
