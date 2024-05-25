import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import json
# st.set_page_config(page_title="NTLX", page_icon="", layout="wide")

# Set up the title and description
st.title("NASA-TLX Workload Assessment")
st.write("""
### Please rate your experience on the following dimensions from 1 (Very Low) to 7 (Very High).
""")

st.session_state.mental_demand = ""
st.session_state.physical_demand = ""
st.session_state.attention_check = ""
st.session_state.temporal_demand = ""
st.session_state.performance = ""
st.session_state.effort = ""
st.session_state.frustration = ""

# Define the scale options
scale = ["1 - Very Low", "2 - Low", "3 - Somewhat Low", "4 - Moderate", "5 - Somewhat High", "6 - High", "7 - Very High"]

# Mental Demand
st.session_state.mental_demand = st.radio("Mental Demand: How mentally demanding was the task?", scale)
# Physical Demand
st.session_state.physical_demand = st.radio("Physical Demand: How physically demanding was the task?", scale)
# Attention Check 
st.session_state.attention_check = st.radio("Free Test: Select 6 on the scale", scale)
# Temporal Demand
st.session_state.temporal_demand = st.radio("Temporal Demand: How hurried or rushed was the pace of the task?", scale)
# Performance
st.session_state.performance = st.radio("Performance: How successful were you in accomplishing what you were asked to do?", scale)
# Effort
st.session_state.effort = st.radio("Effort: How hard did you have to work to accomplish your level of performance?", scale)
# Frustration
st.session_state.frustration = st.radio("Frustration: How insecure, discouraged, irritated, stressed, and annoyed were you?", scale)

# st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

# Convert scale to numeric values
def scale_to_numeric(scale_response):
    return int(scale_response.split(" - ")[0])

if st.button("Submit"):
    results = {
        "Mental Demand": scale_to_numeric(st.session_state.mental_demand),
        "Physical Demand": scale_to_numeric(st.session_state.physical_demand),
        "Temporal Demand": scale_to_numeric(st.session_state.temporal_demand),
        "Performance": scale_to_numeric(st.session_state.performance),
        "Effort": scale_to_numeric(st.session_state.effort),
        "Frustration": scale_to_numeric(st.session_state.frustration)
    }   


    st.session_state.ac1 = scale_to_numeric(st.session_state.attention_check) == 6

    # st.write("### Your NASA-TLX Scores:")
    st.session_state.ntlx1 = results
    switch_page("chat2")
    # You can add further processing or storage of the results as needed
