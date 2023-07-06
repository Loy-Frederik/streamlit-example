from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from PIL import Image
import requests
from urllib.request import urlopen
from io import BytesIO

logo_url = 'https://img.freepik.com/premium-vector/cute-couple-panda-watching-movie-eating-popcorn-cartoon-vector-icon-illustration-animal-food_138676-6443.jpg'

rating_url = 'https://drive.google.com/file/d/1JBolFNkww-nRO_PTAHeXGE3KSVY4_7dl/view?usp=sharing'
titles_url = 'https://drive.google.com/file/d/1Z3vHbjAeTAmFp-NeM-j4zYJjLz-fpqfn/view?usp=sharing'

path = 'https://drive.google.com/uc?export=download&id='
rating_df = pd.read_csv(path+rating_url.split('/')[-2])
titles = pd.read_csv(path+titles_url.split('/')[-2])

# Download the image using requests
response = requests.get(logo_url)
image_bytes = response.content

# Open the image using PIL
logo = Image.open(BytesIO(image_bytes))

st.set_page_config(page_title='WBSFlix', page_icon=logo)

st.header("Find awesome movies")

st.sidebar.header('What do you wanna do?')

movie_like = st.sidebar.selectbox('Movie like', titles['title'], key = 'movie_like')
