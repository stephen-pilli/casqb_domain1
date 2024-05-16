import streamlit as st
import time
import re
import random
from pymongo.mongo_client import MongoClient
from markdownify import markdownify as md

uri = st.secrets["mongo"]['uri']



if "chat_pilli" not in st.session_state:
    st.session_state['chat_pilli'] = False
if "messages_counter" not in st.session_state:
    st.session_state.messages_counter = 0
if "utterances" not in st.session_state:
    st.session_state['utterances'] = ""
if "random_codes" not in st.session_state:
    st.session_state['random_codes'] = ""
if "participant_id" not in st.session_state:
    st.session_state['participant_id'] = ""

st.set_page_config(page_title="Emma", page_icon=":speech_balloon:")


st.title("Emma the Career Counseling Chatbot")

def to_raw(string):
    return fr"{string}"

if st.button("Start"):

    st.session_state['utterances'] = ""
    f = open("utterances.txt", "r")
    st.session_state.utterances = f.read().split("\n")


    st.session_state['random_codes'] = ""
    f = open("random_codes.txt", "r")
    st.session_state.random_codes = f.read().split("\n")

    st.session_state.chat_pilli = True
    st.session_state.messages_counter = 0

if st.sidebar.button("Finish"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.chat_pilli = False  # Reset the chat state
    st.session_state.messages_counter = 0

if st.session_state.chat_pilli:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]): 
            st.markdown(message["content"])

    if prompt := st.chat_input("Say, Hi!!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)


        if st.session_state.messages_counter < len(st.session_state.utterances):
            # for message in st.utterances:
            st.session_state.messages.append({"role": "assistant", "content": st.session_state.utterances[st.session_state.messages_counter]})
            with st.chat_message("assistant"):
                    st.markdown(md(st.session_state.utterances[st.session_state.messages_counter]))

        st.session_state.messages_counter += 1

        if st.session_state.messages_counter == len(st.session_state.utterances)+1:
                st.session_state.messages.append({"role": "assistant", "content": "Enter Your Participant ID"})
                with st.chat_message("assistant"):
                    st.markdown("Enter Your Participant ID")
                
        if st.session_state.messages_counter == len(st.session_state.utterances)+2:
                st.session_state.participant_id = str(prompt)
                sycode = str(random.choice(st.session_state.random_codes))
                content = "Your Survey Code is: " + sycode + "\n" + "You may click on Finish button or Close the window."
                st.session_state.messages.append({"role": "assistant", "content": content})
                with st.chat_message("assistant"):
                    st.markdown(content)

        # if (st.session_state.participant_id != ""):
            # f = open("data/"+str(st.session_state.participant_id)+".json", "w")
            # f.write(str(st.session_state['messages']))
            # f.close()
            # Create a new client and connect to the server

            # Define the query criteria
            # criteria = {"pid": st.session_state.participant_id}
            #pid, amt hit id etcc. 

            # Define the update operation
            # update_operation = {"$set": {"dialogue": str(st.session_state['messages'])}}
            # client = MongoClient(uri)
            # db = client["CASQB"]
            # TEST = db.TEST
            # TEST.update_one(criteria, update_operation, upsert=True)
            # TEST.insert_one({"pid": str(st.session_state.participant_id ), "dialogue": str(st.session_state['messages'])})


