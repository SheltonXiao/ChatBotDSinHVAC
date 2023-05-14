# -*- coding:utf-8 -*-
'''
@File    :   chat.py
@Time    :   2023/05/11 12:46:38
@Author  :   SheltonXiao
@Version :   1.0
@Contact :   pi620903@163.com
@Desc    :   None

'''

# here put the import lib
from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import openai
import os
from scripts.config import *
from utils.tokenChecker import check_prompts

openai.api_key = OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

Prompt_template = """
The following is a friendly conversation between a human and an AI. 
The AI is talkative and provides lots of specific details from its context. 
The AI is also an expert in HVAC.
If the AI does not know the answer to a question, it truthfully says it does not know.
"""
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(Prompt_template),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}"), #用中文的效果不太好
])

class Chat(object):
    def __init__(self):
        self.llm = None
        self.memory = ConversationBufferMemory(return_messages=True)
        self.conversation = ConversationChain(memory=self.memory, prompt=prompt, llm=self.llm)

    def respond(self,input,docs=None):
        if docs != None:
            info = [each.page_content for each in docs]
            inputtext = "Here are the information you may need:"+" ".join(info)+"\n Please ansewer: "
            #checkprom = check_prompts(inputtext)
            #if checkprom:
            #    step = len(inputtext) // checkprom + 1 #还是有问题的，token数不一样
            #    for i in range(checkprom):
            #        left = i * step
            #        right = min(len(inputtext),(i+1)*step)
            #        inputtext = inputtext + " "
            #        if i > 0:
            #            self.conversation.predict(input = "Here is the continue information: "+inputtext[left:right])
            #        else:
            #            self.conversation.predict(inputtext[left:right])
            #else:
            #    self.conversation.predict(input = inputtext)
        return self.conversation.predict(input = inputtext + input)

class OpenAIChat(Chat):
    def __init__(self,api_key=None):
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        self.llm = ChatOpenAI(temperature=0)
        self.memory = ConversationBufferMemory(return_messages=True)
        self.conversation = ConversationChain(memory=self.memory, prompt=prompt, llm=self.llm)

if __name__ == '__main__':
    chat = OpenAIChat()
    print(chat.respond("Hi"))
    print(chat.respond("I'm doing well! Just having a conversation with an AI."))
    print(chat.respond("Tell me about yourself."))