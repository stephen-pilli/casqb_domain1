import streamlit as st
import time
import re
import random
from pymongo.mongo_client import MongoClient
from markdownify import markdownify as md
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(page_title="Survey", page_icon=":speech_balloon:", layout="wide")


st.title("Welcome to the Survey")

#local variables
if "chat_pilli" not in st.session_state:
    st.session_state['chat_pilli'] = False
if "messages_counter" not in st.session_state:
    st.session_state.messages_counter = 0
if "utterances" not in st.session_state:
    st.session_state['utterances'] = ""
if "chatFinish" not in st.session_state:
    st.session_state['chatFinish'] = -1
if "chatStatus" not in st.session_state:
    st.session_state['chatStatus'] = 0

if "mental_demand" not in st.session_state:
    st.session_state['mental_demand'] = ""
if "physical_demand" not in st.session_state:
    st.session_state['physical_demand'] = ""
if "attention_check" not in st.session_state:
    st.session_state['attention_check'] = ""
if "temporal_demand" not in st.session_state:
    st.session_state['temporal_demand'] = ""
if "performance" not in st.session_state:
    st.session_state['performance'] = ""
if "effort" not in st.session_state:
    st.session_state['effort'] = ""
if "frustration" not in st.session_state:
    st.session_state['frustration'] = ""


##Seting up database
if "uri" not in st.session_state:
    st.session_state['uri'] = ""
if "client" not in st.session_state:
    st.session_state['client'] = ""
if "db" not in st.session_state:
    st.session_state['db'] = ""
if "collexp_code" not in st.session_state:
    st.session_state['collexp_code'] = ""
if "collexp_data" not in st.session_state:
    st.session_state['collexp_data'] = ""

try:
    st.session_state.uri = st.secrets["mongo"]['uri']
    st.session_state.client = MongoClient(st.session_state.uri)
    st.session_state.client.server_info()
    st.session_state.db = st.session_state.client["Replication"]
    st.session_state.collexp_code = st.session_state.db.exp_code
    st.session_state.collexp_data = st.session_state.db.exp_data
except:
    st.warning("Unable to establish connection with the server. Make sure your internet connection is out of proxy.")



#participant data
if "prolific_pid" not in st.session_state:
    st.session_state['prolific_pid'] = ""
if "study_id" not in st.session_state:
    st.session_state['study_id'] = ""
if "session_id" not in st.session_state:
    st.session_state['session_id'] = ""
if "consent" not in st.session_state:
    st.session_state['consent'] = ""
if "expcode" not in st.session_state:
    st.session_state['expcode'] = ""
if "chat1" not in st.session_state:
    st.session_state['chat1'] = ""
if "chat2" not in st.session_state:
    st.session_state['chat2'] = ""
if "chat3" not in st.session_state:
    st.session_state['chat3'] = ""
if "ntlx1" not in st.session_state:
    st.session_state['ntlx1'] = ""
if "ntlx2" not in st.session_state:
    st.session_state['ntlx2'] = ""
if "ntlx3" not in st.session_state:
    st.session_state['ntlx3'] = ""
if "ac1" not in st.session_state:
    st.session_state['ac1'] = ""
if "ac2" not in st.session_state:
    st.session_state['ac2'] = ""
if "ac3" not in st.session_state:
    st.session_state['ac3'] = ""
if "serious" not in st.session_state:
    st.session_state['serious'] = ""



# Get URL parameters
params = st.experimental_get_query_params()

if params:
    # Create a formatted display for each parameter
    for key, value in params.items():
        st.write(str(f"**{key.capitalize()}:** {value[0]}").replace("_pid:", " ID:").replace("_id:", " ID:"))

        st.session_state.prolific_pid = params['PROLIFIC_PID'][0]
        st.session_state.study_id = params['STUDY_ID'][0]
        st.session_state.session_id = params['SESSION_ID'][0]
else:
    st.session_state.prolific_pid = st.text_input('Enter Participant ID', key='pid')




# Set up the title and description
st.title("Consent Form")
st.write("""
For ethical reasons it is extremely important that you give your fully informed consent to participate in this study. If you would like to participate, please complete this section.

DECLARATION

I have read the information sheet (previous page) and have had time to consider whether to take part in this study. I understand that my participation is voluntary (it is my choice) and that I am free to withdraw from the research at any time without disadvantage or penalty. I confirm that I am over the age of 18. I agree to take part in this research. I agree that the data arising from this research can be published and that I will not be identified in any way. 

If you have any questions about this research, please contact me at vivek.nallur@ucd.ie 

I consent and would like to continue with the survey.


""")

# Checkbox for user consent
st.session_state.consent = st.checkbox("I have read and understood the above information \
                                       and I agree to participate in this study.", key='cnst')
# Radio buttons for user consent
# consent = st.radio("Do you agree to participate in this study?", ("Yes", "No"))



def getExpCode(value_to_find = 'EMPTY'):

    # The specific value you're looking for
    

    def contains_value(doc, value):
        # Recursively check if any field in the document contains the value
        if isinstance(doc, dict):
            for key, val in doc.items():
                if contains_value(val, value):
                    return True
        elif isinstance(doc, list):
            for item in doc:
                if contains_value(item, value):
                    return True
        else:
            return doc == value
        return False

    # Iterate over all documents in the collection
    for doc in st.session_state.collexp_code.find():
        if contains_value(doc, value_to_find):
            return list(doc)[1]
    else:
        return -1 
    
def updateRecord(key, value, newValue):
    criteria = {key: value }
    update_operation = {"$set": {key: newValue}}
    return st.session_state.collexp_code.update_one(criteria, update_operation, upsert=False)

# Yes (please continue to the next section and complete the survey)

# No (your information will NOT be kept or analysed. Please close this window)




if st.session_state.consent:
    st.success("Thank you for your consent. You may now proceed with the study.")   
    if st.button("Next", key='btn1'):
            if params or st.session_state.prolific_pid != "":
                st.session_state.expcode = getExpCode()
                if st.session_state.expcode != -1:
                    # print(st.session_state.expcode)
                    updateRecord(st.session_state.expcode, "EMPTY", st.session_state.prolific_pid )
                    #update the record to CONSENT
                    #based on the exp select the utterances and randomly select the scenario.
                    #if the survey is successful and recorded update with prolific id
                    switch_page("chat1")
                else:
                    st.warning("Make sure your internet connection is out of proxy.")
            else:
                st.warning("You must provide your Participant ID to proceed.")

    # You can add further steps or redirection after consent is given
    # st.write("Proceed with the next steps...")
else:
    st.warning("You must provide your consent to proceed.")

