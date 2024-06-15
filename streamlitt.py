import streamlit as st
import pandas as pd
import numpy as np
from main import *
# Function to be triggered by user input
st.set_page_config(page_title="Youtube Sentiment Analysis || Streamlit", layout="wide", initial_sidebar_state='collapsed', page_icon='Title_icon.png')

def newfun():
    st.session_state['data']='jabi'

# Title of the web app
st.title('YouTube Video Sentiment Analysis Web App')

# Description
st.write("This is a simple Streamlit app to demonstrate its capabilities.")

# Field box for YouTube Video URL input
youtube_url = st.text_input(label="YouTube", placeholder="Video URL", on_change=newfun)

# Display a sample of the data if it exists

if 'data' in st.session_state:
    try:
        video_id = str(youtube_url).split("=")[1]
        data = comment_downloader(youtube, video_id)
        st.session_state['max_rows'] = len(data['Comments'])
        st.session_state['num_rows'] = 10
        st.sidebar.header('Filters')
        st.session_state['num_rows'] = st.sidebar.slider('No. of rows to display', min_value=5, max_value=st.session_state['max_rows'], value=10, step=10, label_visibility='visible')
        st.header(f"View {st.session_state['num_rows']} of the Comments:", divider="blue")
        st.write(data.head(st.session_state['num_rows']))
        data = read_comments()
        st.header('Scatter Chart', divider='blue')
        for x, index in enumerate(data["Comments"]):
            data.at[x,'id'] = x
        st.write("Positive Comments")
        pos = data[data['pos']>0]
        st.scatter_chart(data=pos, x='id', y ='pos',color='#34F480', size='pos')
        st.write("Negative Comments")
        neg = data[data['neg']>0]
        st.scatter_chart(data=neg, x='id', y ='neg',color='#F48034', size='neg')
    except:
        st.write("Check Video URL")
else:
    st.write("Kindly Enter Youtube Video URL to Proceed Further!")