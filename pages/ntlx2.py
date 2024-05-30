import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import re
import random
# st.set_page_config(page_title="NTLX", page_icon="", layout="wide")

# Set up the title and description
st.title("NASA-TLX Workload Assessment")
st.write("""
### Please rate your recent interaction with the chatbot on a scale from 1 (Very Low) to 7 (Very High):
""")

st.session_state.mental_demand = ""
st.session_state.physical_demand = ""
st.session_state.attention_check = ""
st.session_state.temporal_demand = ""
st.session_state.performance = ""
st.session_state.effort = ""
st.session_state.frustration = ""

st.session_state.choice_problem = ""
st.session_state.match_c = ""
st.session_state.match_d = ""
st.session_state.extracted_text_c = ""
st.session_state.extracted_text_d = ""
st.session_state.alternatives_list = ""

# Define the scale options
scale = ["1 - Very Low", "2 - Low", "3 - Somewhat Low", "4 - Moderate", "5 - Somewhat High", "6 - High", "7 - Very High"]

#attention check prep.
st.session_state.choice_problem = st.session_state.chat2[-3]['content']

pattern_for_c = r'c\)(.*?)d\)'
pattern_for_d = r'd\)\s*(.*)'

# Use re.search to find the pattern in the text
st.session_state.match_c = re.search(pattern_for_c, st.session_state.choice_problem, re.DOTALL)
st.session_state.match_d = re.search(pattern_for_d, st.session_state.choice_problem, re.DOTALL)

# Extract the text if a match is found
if st.session_state.match_c and st.session_state.match_d:
    st.session_state.extracted_text_c = st.session_state.match_c.group(1).strip().replace('College C:', '').replace('<br>', '')
    st.session_state.extracted_text_d = st.session_state.match_d.group(1).strip().replace('College D:', '').replace('<br>', '')
    st.session_state.alternatives_list = [st.session_state.extracted_text_c, st.session_state.extracted_text_d]


# Attention Check 
st.session_state.attention_check = st.radio("During your last chat, identify the last alternative between the two:", st.session_state.alternatives_list, index=None)

# Mental Demand
st.session_state.mental_demand = st.radio("Mental Demand: How mentally demanding was the task?", scale, index=None)
# Physical Demand
st.session_state.physical_demand = st.radio("Physical Demand: How physically demanding was the task?", scale, index=None)
# Temporal Demand
st.session_state.temporal_demand = st.radio("Temporal Demand: How hurried or rushed was the pace of the task?", scale, index=None)
# Performance
st.session_state.performance = st.radio("Performance: How successful were you in accomplishing what you were asked to do?", scale, index=None)
# Effort
st.session_state.effort = st.radio("Effort: How hard did you have to work to accomplish your level of performance?", scale, index=None)
# # Attention Check 
# st.session_state.attention_check = st.radio("Load Test: Select 3 on the scale", scale)
# Frustration
st.session_state.frustration = st.radio("Frustration: How insecure, discouraged, irritated, stressed, and annoyed were you?", scale, index=None)

# st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

# Convert scale to numeric values
def scale_to_numeric(scale_response):
    if scale_response != None:
        return int(scale_response.split(" - ")[0])
    else:
        return None

if st.button("Submit"):
    results = {
        "Mental Demand": scale_to_numeric(st.session_state.mental_demand),
        "Physical Demand": scale_to_numeric(st.session_state.physical_demand),
        "Temporal Demand": scale_to_numeric(st.session_state.temporal_demand),
        "Performance": scale_to_numeric(st.session_state.performance),
        "Effort": scale_to_numeric(st.session_state.effort),
        "Frustration": scale_to_numeric(st.session_state.frustration),
    }
    # st.session_state.ac2 = scale_to_numeric(st.session_state.attention_check) == 3
    st.session_state.ac2 = st.session_state.attention_check == st.session_state.extracted_text_d

    # st.write("### Your NASA-TLX Scores:")
    st.session_state.ntlx2 = results
    switch_page("chat3")
    # You can add further processing or storage of the results as needed
