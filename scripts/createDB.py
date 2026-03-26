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
from scripts.knowledgeDB import MyPDFLoader,MyPinecone,MyWeaviate
from scripts.config import *

import os

class AbstractCreateDB(object):
    def __init__(self):
        self.fatherpath = "data/"
        pass
    def create(self,file_list=[]):
        if len(file_list)==0:
            file_list = os.listdir(self.fatherpath)
            self.file_list = [os.path.join(self.fatherpath,each) for each in file_list if each.split(".")[1] == "pdf"]
        self.file_list = file_list
class UpdateDB(object):
    def __init__(self):
        pass
    def update(self,file_list,namespace=None):
        MyPinecone().add_data(file_list, namespace=namespace)
    def update_doc(self,documents_list,namespace=None):
        MyPinecone().add_documents(documents_list,namespace=namespace)

class CreateDBPinecone(AbstractCreateDB):
    def create(self,file_list=[]):
        super().create(file_list)
        MyPinecone().add_data(self.file_list)

class CreateDBWeaviate(AbstractCreateDB):
    def create(self,file_list=[]):
        super().create(file_list)
        MyWeaviate().add_data(self.file_list)

if __name__ == '__main__':
    AbstractCreateDB().create()
