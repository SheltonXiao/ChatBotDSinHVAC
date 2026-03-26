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
#import os
#os.chdir(r"E:\Document\github\ChatBotDSinHVAC")

# here put the import lib
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeEmbeddings
from langchain_community.vectorstores import Chroma,Weaviate #,Pinecone
from langchain_pinecone import PineconeVectorStore as PineconeVS
#from langchain.document_loaders import PyPDFLoader#,UnstructuredPDFLoader
from langchain_community.document_loaders import PyPDFLoader,UnstructuredFileLoader
#from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA
from transformers import GPT2TokenizerFast
#import weaviate
#import pinecone
from pinecone import Pinecone #as pinecone
import os
import json
#from chat import OpenAIChat
#from config import *
from scripts.chat import OpenAIChat
from scripts.config import *
import time


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
pc = Pinecone(
        api_key=PINECONE_API_KEY,
        environment = PINECONE_ENV
    )
#pinecone.init(
#    api_key = PINECONE_API_KEY,
#    environment = PINECONE_ENV
#)
client = None#weaviate.Client(
#    url = WEAVIATE_URL,  # Replace with your endpoint
#    auth_client_secret = weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY),  # Replace w/ your Weaviate instance API key
#)
#client.schema.get()

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

persist_directory = ""

# Split the document into chunks base on markdown headers.
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]
metadata_name = [each[1] for each in headers_to_split_on]
text_splitter_md = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on,)

text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 800,#1000, #500 #250 1000效果还可以但是中文会报错
        chunk_overlap = 50,#10
        #length_function = len,
    )

embeddings = OpenAIEmbeddings(base_url="https://api.chatanywhere.com.cn/v1")

#model_name = "text-embedding-ada-002"  
#embeddings = PineconeEmbeddings(  
#    model=model_name,  
#    pinecone_api_key=os.environ.get("PINECONE_API_KEY")  
#)  
index_name = PINE_CONE_DB_NAME

class MyDataLoader(object):
    def __init__(self,path = ""):
        self.loader = ...
    def split(self):
        return None

class MyPDFLoader(MyDataLoader):
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

class MyMarkdownLoader(MyDataLoader):
    def __init__(self,path = ""):
        self.loader = UnstructuredFileLoader(path)#UnstructuredMarkdownLoader(path,mode="elements") #
        self.text = self.split()
    def split(self):
        self.pages = self.loader.load()
        text = text_splitter_md.split_text(self.pages[0].page_content)
        text = text_splitter.split_documents(text)
        text = self.check_metadata(text)
        return text
    def check_metadata(self,text):
        #new_text = []
        for doc in text:
            base_info = doc.metadata
            missing_metadata = set(metadata_name).difference(base_info)
            if len(missing_metadata) > 0:
                ## fill with unknown
                for each in missing_metadata:
                    doc.metadata[each] = "unknown"
            #new_text.append(doc)
        return text#new_text

class MyVectorDB(object):
    config_json = ""
    def __init__(self):
        pass
    def add_data(self,file_list=[]):
        ...
    def read(self):
        return None
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

class MyPinecone(MyVectorDB):
    config_json = "PineconeDataInfo.json"
    def __init__(self):
        self.index_name = index_name
    def add_data(self,file_list=[],namespace=None):
        text = []
        for file in file_list:
            loader = MyMarkdownLoader(file)#MyPDFLoader(file)
            self.docsearch = PineconeVS.from_documents(loader.text, embeddings, index_name = self.index_name,
                                                        pinecone_api_key=os.environ.get("PINECONE_API_KEY"),
                                                        namespace = namespace )
            self._write_status([file])

            #text.extend(loader.text)
        #self.docsearch = Pinecone.from_texts(text, embeddings, index_name = self.index_name)
        #self._write_status(file_list)
    def add_documents(self, documents_list=[],namespace=None):
        for document in documents_list:
            self.docsearch = PineconeVS.from_documents(document, embeddings, index_name = self.index_name,
                                                       pinecone_api_key=os.environ.get("PINECONE_API_KEY"),
                                                       namespace = namespace )

    def read(self):
        self.docsearch = PineconeVS(pinecone_api_key=os.environ.get("PINECONE_API_KEY"), embedding=embeddings,
                                    index_name=self.index_name)
                         #PineconeVS.from_existing_index(self.index_name,embeddings,
                         #                               pinecone_api_key=os.environ.get("PINECONE_API_KEY") )
        return self.docsearch

class MyWeaviate(MyVectorDB):
    config_json = "WeaviateDataInfo.json"
    def __init__(self):
        self.client = client
    def add_data(self,file_list=[]):
        for file in file_list:
            loader = MyPDFLoader(file)
            print("finishLoading")
            self.docsearch = Weaviate.from_documents(loader.text, embeddings, client=self.client)
            self._write_status([file])
    def read(self):
        self.docsearch = Weaviate(client = self.client, embedding=embeddings)
        return self.docsearch

class MyChroma(MyVectorDB):
    def __init__(self):
        self.persist_directory = persist_directory
    def add_data(self,file_list=[]):
        for file in file_list:
            loader = MyPDFLoader(file)
            self.docsearch = Chroma.from_documents(loader.text, embeddings, persist_directory=self.persist_directory)
    def read(self):
        self.docsearch = Chroma(persist_directory=self.persist_directory,embedding_function=embeddings)
        return self.docsearch

if __name__ == '__main__':
    
    docsearch = MyPinecone().read()
    #docsearch = MyWeaviate().read()

    #query = "What does a typical data driven approcah include?"
    #query = "How to compute a performance driven design?"
    query = "在其他条件相同时，下列关于室内人员显热冷负荷的说法，哪一项是错误的？ A.人员的群集系数越大，室内人员的显热冷负荷则越大 B.围护结构的放热衰减倍数越大，室内人员显热冷负荷则越大 C.人员在室时间越长，室内人员显热冷负荷则越大 D.随着室内温度的增高，室内人员的显热散热量减少"
    #query = "primary air"
    #query = "什么是一次回风"
    docs = docsearch.similarity_search(query, k = 3)
    #chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
    
    #print(chain.run(input_documents=docs, question=query))

    print(docs)

    #c = OpenAIChat()
    #print(query)
    #print(c.respond(input = query,docs=docs))