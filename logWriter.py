# -*- encoding: utf-8 -*-
'''
@File    :   logWriter.py
@Time    :   2023/10/18 20:41:12
@Author  :   SheltonXiao 
@Version :   1.0
@Contact :   pi620903@163.com
@License :   (C)Copyright 2023, SheltonXiao
@Desc    :   None
'''

# here put the import lib
import pymongo
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
    dic["time"] = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime())
    dic.update(request.json)
    dic.update(json_dict)
    dicin = {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()):dic}
    json_append(log_file, dicin)
    mycol = check_db()
    x = mycol.insert_one(dic)
    print(x)

def check_db():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["log"]
    dblist = myclient.list_database_names()
    # dblist = myclient.database_names() 
    if "log" in dblist:
        print("数据库已存在！")
    else:
        print('数据库不存在')

    date = time.strftime('%Y%m%d', time.localtime())

    mycol = mydb[date]

    collist = mydb. list_collection_names()
    if date in collist:   # 判断 sites 集合是否存在
        print("集合已存在！")
    else:
        print('集合不存在')

    return mycol

if __name__ == '__main__':
    pass