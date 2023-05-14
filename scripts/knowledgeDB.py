# -*- coding:utf-8 -*-
'''
@File    :   knowledgeDB.py
@Time    :   2023/05/11 12:25:11
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
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma,Pinecone
from langchain.document_loaders import PyPDFLoader,UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from transformers import GPT2TokenizerFast
import pinecone
import os
import json
from scripts.chat import OpenAIChat
from scripts.config import *
import time


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
pinecone.init(
    api_key = PINECONE_API_KEY,
    environment = PINECONE_ENV
)

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

#text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(
#        tokenizer,
text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000, #500 #250
        chunk_overlap = 50,#10
        #length_function = len,
    )

embeddings = OpenAIEmbeddings()
index_name = PINE_CONE_DB_NAME

class MyPDFLoader(object):
    def __init__(self,path = ""):
        self.loader = PyPDFLoader(path) # 保留页码
        #self.loader = UnstructuredPDFLoader(path) #报错中pdf2image.exceptions.PDFPageCountError: Unable to get page count.
        self.text = self.split()
    
    def split(self):
        self.pages = self.loader.load_and_split() #PyPDF
        #self.split_docs = []
        #for eachpage in self.pages:
        #    self.split_docs.extend(text_splitter.split_text(eachpage.page_content))
        self.split_docs = text_splitter.split_documents(self.pages)
        #self.docs = self.loader.load() #unstructure
        #self.split_docs = text_splitter.create_documents(self.docs)
        return self.split_docs #[t.page_content for t in self.split_docs]

class MyPinecone(object):
    config_json = "PineconeDataInfo.json"
    def __init__(self):
        self.index_name = index_name
    def add_data(self,file_list=[]):
        text = []
        for file in file_list:
            loader = MyPDFLoader(file)
            #elf.docsearch = Pinecone.from_documents(loader.text, embeddings, index_name = self.index_name)
            self._write_status([file])

            #text.extend(loader.text)
        #self.docsearch = Pinecone.from_texts(text, embeddings, index_name = self.index_name)
        #self._write_status(file_list)
    def read(self):
        self.docsearch = Pinecone.from_existing_index(self.index_name,embeddings)
        return self.docsearch
    def _write_status(self,file_list):
        try:
            with open(self.config_json,'r') as load_f:
                status_dict = json.load(load_f)
        except:
            status_dict = {}
        i = len(status_dict)
        for file in file_list:
            status_dict[str(i)]=(file,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            i += 1
        with open(self.config_json,"w") as f:
            json.dump(status_dict,f)


if __name__ == '__main__':
    
    docsearch = MyPinecone().read()

    #query = "What does a typical data driven approcah include?"
    #query = "How to compute a performance driven design?"
    query = "How to compute a building-to-grid modelling?"
    docs = docsearch.similarity_search(query, include_metadata = True, k = 3)
    #chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
    
    #print(chain.run(input_documents=docs, question=query))
    c = OpenAIChat()
    print(query)
    print(c.respond(input = query,docs=docs))