import streamlit as st
import time
import re
import random
from pymongo.mongo_client import MongoClient
from markdownify import markdownify as md
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime



if st.button('Start Chat'):
    chatbot2 = st.session_state.chatStatus
    expcode = str(st.session_state.expcode).split('_')[1].split('&')[chatbot2].replace("$", "_") ##<<<<<<******************************** very important make deligent changes in the chatbot2 and chatbot3 files. 

    st.session_state['utterances'] = ""
    f = open(f"utterances/{expcode}.txt", "r")
    st.session_state.utterances = f.read().split("\n")

    st.session_state.chat_pilli = True
    st.session_state.messages_counter = 0

def finishAndProceed():
    st.session_state.disable_chat_input = False
    st.session_state.chat2 = st.session_state['messages']
    st.session_state.messages = []  # Clear the chat history
    st.session_state.chat_pilli = False  # Reset the chat state
    st.session_state.messages_counter = 0
    st.session_state.utterances = ""
    st.session_state.chatFinish = 0

def get_current_timestamp():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

if st.session_state.chat_pilli:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]): 
            st.markdown(md(message["content"]))

    if prompt := st.chat_input(disabled= st.session_state.disable_chat_input):
        st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": get_current_timestamp()})
        with st.chat_message("user"):
            st.markdown(prompt)


        if st.session_state.messages_counter < len(st.session_state.utterances):
            # for message in st.utterances:
            st.session_state.messages.append({"role": "assistant", "content": st.session_state.utterances[st.session_state.messages_counter], "timestamp": get_current_timestamp()})
            with st.chat_message("assistant"):
                    st.markdown(md(st.session_state.utterances[st.session_state.messages_counter]))

        st.session_state.messages_counter += 1

        if st.session_state.messages_counter == len(st.session_state.utterances):
            st.session_state.disable_chat_input = True

        if st.session_state.messages_counter == len(st.session_state.utterances)+1:
            #create button to go to the next page
            #save the messages
            st.session_state.messages.append({"role": "assistant", "content": "Click on Finish & Proceed", "timestamp": get_current_timestamp()})
            with st.chat_message("assistant"):
                st.markdown("Click on Finish & Proceed")

            st.button("Finish & Proceed", on_click=finishAndProceed)



if st.session_state.chatFinish == 0:
    st.session_state.chatFinish = -1
    st.session_state.chatStatus += 1
    switch_page("ntlx2")
