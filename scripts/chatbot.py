# -*- coding:utf-8 -*-
'''
@File    :   chatbot.py
@Time    :   2023/05/11 21:07:20
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
from scripts.chat import Chat,OpenAIChat
from scripts.knowledgeDB import MyPinecone

class ChatBot(object):
    chatbase:Chat = None
    database:MyPinecone = None
    def __init__(self):
        self.docsearch = self.database.read()

    def chat(self,query):
        docs = self.docsearch.similarity_search(query, include_metadata = True, k = 5)
        print("done with search")
        return self.chatbase.respond(input = query,docs=docs)

class OpenAIChatBot(ChatBot):
    def __init__(self,api_key):
        self.chatbase = OpenAIChat(api_key)
        self.database = MyPinecone()
        self.docsearch = self.database.read()

if __name__ == '__main__':
    pass
