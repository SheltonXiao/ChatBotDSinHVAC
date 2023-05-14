# -*- coding:utf-8 -*-
'''
@File    :   backend.py
@Time    :   2023/05/11 20:48:32
@Author  :   SheltonXiao
@Version :   1.0
@Contact :   pi620903@163.com
@Desc    :   None
@License :

    (c) Copyright 2022 SheltonXiao

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or(at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY;without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
    GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with this program.If not, see < https: //www.gnu.org/licenses/>.
'''

# here put the import lib
from flask import jsonify
from flask import Flask, request
from scripts.chatbot import OpenAIChatBot
from baseclass import Pool
import json
import time
import os

log_file = "log.json"
def json_append(filename, dic):
    try:
        if os.path.exists(filename):
            dic_json=json.dumps(dic,indent=4, ensure_ascii=False)
            ch1=", "
            ch2="}"
            dic1=ch1+dic_json[1:(len(dic_json)-1)]+ch2
            try:
                with open(filename,"rb+") as f:
                    f.seek(-1,2)
                    f.write(bytes(dic1,encoding = 'utf-8'))
                    return 0
            except IOError:
                print("写入%s失败"%filename)
                return -1
        else:
            try:
                with open(filename,"w") as f:
                    json.dump(dic,f, indent=4, ensure_ascii=False)
                    return 0
            except IOError:
                print("写入%s失败"%filename)
                return -1
    except IOError:
        print("调用io模块查找%s失败"%filename)
        return -2

def write_log(request,json_dict):
    dic = {}
    dic["time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    dic.update(request.json)
    dic.update(json_dict)
    dicin = {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()):dic}
    json_append(log_file, dicin)

app = Flask(__name__)
chat_pool = Pool()

@app.route("/query/", methods=['POST', 'GET'])
def query():
    api_key = request.headers.get('Api-Key')
    user_stamp = request.json['user_stamp']
    user_query = request.json['user_query']
    print(
        "api_key", api_key,
        "user_stamp", user_stamp,
        "user_query", user_query
    )

    bot = None
    if user_stamp not in chat_pool:
        print(f"User {user_stamp} not in pool, creating new chatpdf")
        # Initialize the ChatPDF
        bot = OpenAIChatBot(
            api_key=api_key,
            #engine=DEFAULT_ENGINE,
            #proxy=None,
            #max_tokens=4000,
            #temperature=DEFAULT_TEMPERATURE,
            #top_p=DEFAULT_TOP_P,
            #presence_penalty=DEFAULT_PRESENCE_PENALTY,
            #frequency_penalty=DEFAULT_FREQUENCY_PENALTY,
            #reply_count=DEFAULT_REPLY_COUNT
        )

        chat_pool[user_stamp] = bot
    else:
        print("user_stamp", user_stamp, "already exists")
        bot = chat_pool[user_stamp]

    try:
        print("Here")
        response = bot.chat(user_query)
        code = 200
        json_dict = {
            "code": code,
            "response": response
        }
    except Exception as e:
        print("Somethingwrong")
        code = 500
        json_dict = {
            "code": code,
            "response": str(e)
        }
    write_log(request,json_dict) #写入日志
    return jsonify(json_dict)


@app.route("/", methods=['GET'])
def index():
    return "Hello World!"



if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)