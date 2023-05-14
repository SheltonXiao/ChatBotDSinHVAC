# -*- coding:utf-8 -*-
'''
@File    :   config.py
@Time    :   2023/05/11 12:07:34
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
import os

# device config
OPENAI_API_KEY = "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" #"填入专属的API key"  

# vector storage config
PINECONE_API_KEY = "08e28b00-6c98-4c8f-9c2f-40a4280e62ef"
PINECONE_ENV = "us-west1-gcp-free"
PINE_CONE_DB_NAME = "ds-hvac"

# init model config
init_llm = "ChatGLM-6B-int8"
init_embedding_model = "text2vec-base"

# model config
embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "ernie-medium": "nghuyong/ernie-3.0-medium-zh",
    "ernie-xbase": "nghuyong/ernie-3.0-xbase-zh",
    "text2vec-base": "GanymedeNil/text2vec-base-chinese",
    'simbert-base-chinese': 'WangZeJun/simbert-base-chinese',
    'paraphrase-multilingual-MiniLM-L12-v2': "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
}


llm_model_dict = {
    "gpt": {
        "GPT-3.5": "gpt-3.5-turbo",
    },
    "vicuna": {
        "Vicuna-7b": "vicuna-7b-v1.1",
    }
}


if __name__ == '__main__':
    pass
