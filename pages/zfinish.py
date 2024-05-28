import streamlit as st
import json
import io
from pymongo.mongo_client import MongoClient
from markdownify import markdownify as md
from streamlit_extras.switch_page_button import switch_page
import webbrowser

st.set_page_config(page_title="Survey", page_icon=":speech_balloon:")

# st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)


st.title("Survey Submission")

st.write("Please contact me, Vivek Nallur (vivek.nallur@ucd.ie), \
         if there is anything at all that you would like to discuss \
         regarding issues raised in this survey.")

st.header("How serious are you while interacting with the chatbot?")
st.session_state.serious = st.radio(
    "To what extent did you seriously consider the scenarios presented in the chatbot?",
    ('1 - Not serious at all', '2', '3', '4', '5', '6', '7 - Very serious')
)

def getData():
    results = {
        "prolific_pid": st.session_state.prolific_pid,
        "study_id": st.session_state.study_id,
        "session_id": st.session_state.session_id,
        "consent": st.session_state.consent,
        "expcode": st.session_state.expcode,
        "chat1": st.session_state.chat1,
        "chat2": st.session_state.chat2,
        "chat3": st.session_state.chat3,
        "ntlx1": st.session_state.ntlx1,
        "ntlx2": st.session_state.ntlx2,
        "ntlx3": st.session_state.ntlx3,
        "ac1": st.session_state.ac1,
        "ac2": st.session_state.ac2,
        "ac3": st.session_state.ac3,
        "serious": st.session_state.serious[0]
    }
    
    return json.dumps(results, indent=4)

def updateRecord(key, value, newValue):
    criteria = {key: value }
    update_operation = {"$set": {key: newValue}}
    return st.session_state.collexp_code.update_one(criteria, update_operation, upsert=False)



if st.button('Submit'):
    st.warning('Please wait while your submission is in progress.')
    data = getData()
    data = data.strip()
    try:
        updateRecord(st.session_state.expcode, st.session_state.prolific_pid , data)
        # Convert the dictionary to a JSON string
        # json_data = json.dumps(data, indent=4)

        # Create a BytesIO object and write the JSON string to it
        json_bytes = io.BytesIO(data.encode('utf-8'))
        json_bytes.seek(0)
        st.download_button(
            label="Download Your Copy",
            data=json_bytes,
            file_name=f'{st.session_state.prolific_pid}.json',
            mime='application/json'
        )
        
                # Function to open a link   
        def open_link(url):
            webbrowser.open_new_tab(url)

        open_link('https://app.prolific.com/submissions/complete?cc=C291VV82')

        st.success("Click on the button below to download your responses. Please share the file if requested. Thank you for completing the survey! You may close this window.")


    except:
        st.warning("You submission has failed. Please download the file and share it with the above mentioned email-id. In addition, use the code C291VV82 to complete your submission.")
        
        # Convert the dictionary to a JSON string
        # json_data = json.dumps(data, indent=4)

        # Create a BytesIO object and write the JSON string to it
        json_bytes = io.BytesIO(data.encode('utf-8'))
        json_bytes.seek(0)
        st.download_button(
            label="Download Your Copy",
            data=json_bytes,
            file_name=f'{st.session_state.prolific_pid}.json',
            mime='application/json'
        )




# #features
# #before the session starts, fetch participants ID and put the participant in bucket.

# if "chat_pilli" not in st.session_state:
#     st.session_state['chat_pilli'] = False
# if "messages_counter" not in st.session_state:
#     st.session_state.messages_counter = 0
# if "utterances" not in st.session_state:
#     st.session_state['utterances'] = ""



# #only once you fully complete the survey your data will be stored in the database
# #fetch the database and assign a condition to the user


# if st.button('Start Chat'):

#     st.session_state['utterances'] = ""
#     f = open("utterances/s1c1.txt", "r")
#     st.session_state.utterances = f.read().split("\n")

#     st.session_state.chat_pilli = True
#     st.session_state.messages_counter = 0


# # if st.sidebar.button("Finish"):
# #     st.session_state.messages = []  # Clear the chat history
# #     st.session_state.chat_pilli = False  # Reset the chat state
# #     st.session_state.messages_counter = 0

# if st.session_state.chat_pilli:
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]): 
#             st.markdown(message["content"])

#     if prompt := st.chat_input("Say, Hi!!"):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)


#         if st.session_state.messages_counter < len(st.session_state.utterances):
#             # for message in st.utterances:
#             st.session_state.messages.append({"role": "assistant", "content": st.session_state.utterances[st.session_state.messages_counter]})
#             with st.chat_message("assistant"):
#                     st.markdown(md(st.session_state.utterances[st.session_state.messages_counter]))

#         st.session_state.messages_counter += 1

#         if st.session_state.messages_counter == len(st.session_state.utterances)+1:
            #create button to go to the next page
            #save the messages
            
                # st.session_state.messages.append({"role": "assistant", "content": "Enter Your Participant ID"})
                # with st.chat_message("assistant"):
                #     st.markdown("Enter Your Participant ID")
                
        # if st.session_state.messages_counter == len(st.session_state.utterances)+2:
        #         st.session_state.participant_id = str(prompt)
        #         sycode = str(random.choice(st.session_state.random_codes))
        #         content = "Your Survey Code is: " + sycode + "\n" + "You may click on Finish button or Close the window."
        #         st.session_state.messages.append({"role": "assistant", "content": content})
        #         with st.chat_message("assistant"):
        #             st.markdown(content)

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


