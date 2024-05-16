import streamlit as st
import time
import re
import random
from pymongo.mongo_client import MongoClient


uri = st.secrets["mongo"]['uri']


# Create a new client and connect to the server
client = MongoClient(uri)
db = client["CASQB"]
TEST = db.TEST

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


for x in TEST.find():
  print(x) 