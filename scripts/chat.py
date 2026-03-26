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
    PromptTemplate,
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory,ConversationBufferWindowMemory
import openai
import os
from scripts.config import *
from scripts.chain import MyConversationChain
from utils.tokenChecker import check_prompts

openai.api_key = OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

Prompt_template = """
The following is a friendly conversation between a human and an AI. 
The AI is talkative and provides lots of specific details from its context. 
The AI is also an expert in HVAC.
The AI is created by Tong Xiao and Peng Xu from Tongji University, China.
If the AI does not know the answer to a question, it truthfully says it does not know.

{context}

{chat_history}

Human:{human_input}
Chatbot:"""
prompt = PromptTemplate(
    input_variables=["chat_history","human_input","context"],template=Prompt_template
)
"""ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(Prompt_template),
    MessagesPlaceholder(variable_name="context"),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{human_input}"), #用中文的效果不太好
])"""

class Chat(object):
    def __init__(self):
        self.llm = None
        self.memory = ConversationBufferWindowMemory(k=10,memory_key="chat_history",return_messages=True,input_key="human_input")
        #self.conversation = MyConversationChain(memory=self.memory, prompt=prompt, llm=self.llm)
        self.conversation = load_qa_chain(memory=self.memory, prompt=prompt, llm=self.llm, chain_type="stuff")
    def respond(self,input,docs=None):
        if docs != None:
            info = [each.page_content for each in docs]
            inputtext = "Here are the information you may need:"+" ".join(info)#+"\n Please ansewer: "
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
        try:
            return self.conversation({"input_documents": docs, "human_input": input},return_only_outputs=True)["output_text"]#input = inputtext + input)#information = inputtext, input = input)
        except:
            self.clear_memory()
            return "I would like to stop this conversation. Let's start a new topic."
    def clear_memory(self):
        self.memory.clear()

class OpenAIChat(Chat):
    def __init__(self,model_name="gpt-3.5-turbo",api_key=None,base_url="https://api.chatanywhere.com.cn/v1"):
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        self.llm = ChatOpenAI(model_name=model_name,temperature=0,base_url=base_url)
        self.memory = ConversationBufferWindowMemory(k=10,memory_key="chat_history",return_messages=True,input_key="human_input")
        self.conversation = load_qa_chain(memory=self.memory, prompt=prompt, llm=self.llm,chain_type="stuff")
        #self.conversation = ConversationChain(memory=self.memory, prompt=prompt, llm=self.llm)

class SingleChat(object):
    pass

if __name__ == '__main__':
    chat = OpenAIChat()
    print(chat.respond("Hi"))
    print(chat.respond("I'm doing well! Just having a conversation with an AI."))
    print(chat.respond("Tell me about yourself."))