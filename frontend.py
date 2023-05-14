# -*- coding:utf-8 -*-
'''
@File    :   frontend.py
@Time    :   2023/05/11 20:58:55
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
import datetime
import os
import streamlit as st
from streamlit_chat import message
import requests

st.set_page_config(
    page_title="ChatBotDSHVAC - Demo",
    page_icon=":robot:"
)

st.sidebar.markdown("## API Key")
api_key = st.sidebar.text_input(
    "OpenAI API Key", value="", label_visibility="hidden", help="Please enter your API key.")

def get_text():
    input_text = st.text_input(
        "User: ", "", help="Please ask any questions about Data Science in HVAC.")
    return input_text

st.header("ChatBotDSHVAC - Demo")
st.markdown(
        "<span style='color:black'>Try to ask some questions about BEM, UBEM, uncertainty analysis and data-driven model.</span>", unsafe_allow_html=True)

API_URL = "http://localhost:5000/query/"
header = {"api_key": ""}

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if "user_stamp" not in st.session_state:
    import datetime
    user_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state['user_stamp'] = user_stamp

if api_key:
    header['api_key'] = api_key
        
    user_query = get_text()
        
    if user_query:
        st.session_state.past.append(user_query)
        query_data = {"user_stamp": st.session_state.user_stamp, "user_query": user_query}
        print(query_data)
        response = requests.post(
                API_URL, headers=header, json=query_data, timeout=300)
        print("Hey")
        output = response.json()
        code = output['code']
        response = output['response']
        if code == 200:
            st.session_state.generated.append(response)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i],
                    key=str(i), avatar_style="fun-emoji")
            message(st.session_state['past'][i], is_user=True, key=str(
                i) + '_user', avatar_style="personas")
else:
    st.markdown(
        "<span style='color:red'>Please enter your API key.</span>", unsafe_allow_html=True)


if __name__ == '__main__':
    pass
