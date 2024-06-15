import streamlit as st
import pandas as pd
import numpy as np
from main import *
# Function to be triggered by user input

def newfun():
    st.session_state['data']='jabi'
    #video_id = str(youtube_url).split('=')[1]
    #return video_id
    # youtube_url = str(st.session_state['youtube_url'])
    # print(youtube_url)
    
    # print(video_id)
    # df = main.comment_downloader(main.youtube,  video_id)
    # st.session_state['data'] = df

# Title of the web app
st.title('YouTube Video Sentiment Analysis Web App')

# Description
st.write("This is a simple Streamlit app to demonstrate its capabilities.")

# Sidebar for user input
#st.sidebar.header('User Input')
#if 'max_rows' not in st.session_state:
 #   st.session_state['num_rows'] = st.sidebar.slider('Number of rows to display', min_value=5, max_value=50, value=10, step=5)

# Field box for YouTube Video URL input
youtube_url = st.text_input(label="YouTube", placeholder="Video URL", on_change=newfun)

# Display a sample of the data if it exists

if 'data' in st.session_state:
    video_id = str(youtube_url).split("=")[1]
    data = comment_downloader(youtube, video_id)
    st.session_state['max_rows'] = len(data['Comments'])
    st.session_state['num_rows'] = 10
    st.sidebar.header('Filters')
    st.session_state['num_rows'] = st.sidebar.slider('No. of rows to display', min_value=5, max_value=st.session_state['max_rows'], value=10, step=10, label_visibility='visible')
    st.header(f"Displaying {st.session_state['num_rows']} rows of the data:", divider="blue")
    st.write(data.head(st.session_state['num_rows']))
    st.header('Line Chart', divider='blue')
    st.bar_chart(data=data, x= 'Like_Counts', y = 'Reply_Comments')

else:
    st.write("Kindly Enter Youtube Video URL to Proceed Further!")