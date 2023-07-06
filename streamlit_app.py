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

# Download the image using requests
response = requests.get(logo_url)
image_bytes = response.content

# Open the image using PIL
logo = Image.open(BytesIO(image_bytes))

st.set_page_config(page_title='WBSFlix', page_icon=logo)

st.header("Find awesome movies")


