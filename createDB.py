# -*- coding:utf-8 -*-
'''
@File    :   createDB.py
@Time    :   2023/05/11 19:25:15
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
from scripts.createDB import CreateDBPinecone,UpdateDB,CreateDBWeaviate
import os

if __name__ == '__main__':
    #CreateDB().create()

    #fatherpath = "data/new/"
    #file_list = os.listdir(fatherpath)
    #file_list = [os.path.join(fatherpath,each) for each in file_list]
    file_list = [r"E:\Document\github\ChatBotDSinHVAC\data\高效机房.txt"]
    UpdateDB().update(file_list)

    #CreateDBWeaviate().create(file_list)