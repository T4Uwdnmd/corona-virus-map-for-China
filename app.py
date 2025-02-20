#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2020/8/26 14:48
# @Author : way
# @Site :
# @Describe:

from flask import Flask, render_template
from data import SourceData
from pymongo import MongoClient
import data
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask import jsonify
import time


app = Flask(__name__)

@app.route('/')
def index():
    # 新建一个实例
    data = SourceData()
    # 传入一个实例，和实例的标题
    return render_template('index_ajax.html', form=data, title=data.title)

@app.route("/chinaprovicne")
def chinaprovince():
	client = MongoClient("mongodb+srv://username:password@*****")
	db = client.coronavirus
	collection = db.chinaprovince
	chinaprovincecusor = collection.find({'dateId': "20200702"} )

	outputapp =[]
	for s in chinaprovincecusor:
		outputapp.append({'name':s['provinceShortName'],'value':s['currentConfirmedCount'],'currentConfirmedCount':s['currentConfirmedCount'],'confirmedCount':s['confirmedCount'],'curedCount':s['curedCount'],'deadCount':s['deadCount']})
	return jsonify(data=outputapp)



if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
