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
titles_df = pd.read_csv(path+titles_url.split('/')[-2])

# Download the image using requests
response = requests.get(logo_url)
image_bytes = response.content

# Open the image using PIL
logo = Image.open(BytesIO(image_bytes))

st.set_page_config(page_title='WBSFlix', page_icon=logo)

st.header("Find awesome movies")

st.sidebar.header('What do you wanna do?')


custom = st.sidebar.checkbox('Personalized Experience', value=False, key='custom', help='Click this to get Custom recommendations')

if custom == True:
    rec_select = st.sidebar.radio(
        "What kind of recommendation do you like",
        ('Similar Movies', 'Similar Taste', 'Movies that are hot right now', 'All at once'), key='rec_select')
else:
    st.write('Basic Bitch!')
    rec_select = ''
    

if rec_select == 'Similar Movies':
    movie_like = st.sidebar.selectbox('Movie like', titles_df['title'], key = 'movie_like')
elif rec_select == 'Similar Taste':
    user_like = st.sidebar.selectbox('Who are you', rating_df['userId'], key = 'user_like')
elif rec_select == 'Movies that are hot right now':
    st.write('Lets find some lit Movies.')
elif rec_select == 'All at once':
    st.write('Sure we can do all together!')
else:
    st.write('These movies are lit!!!!')

# st.popular_movies("My text here", value="Default text" * 100, height=100)



# st.markdown(
#     """
# <style>
# popular_movies {
#     white-space: nowrap;
# }
# """,
#     unsafe_allow_html=True,
# )
with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
       st.header("A cat")
       st.image("https://static.streamlit.io/examples/cat.jpg")
    
    with col2:
       st.header("A dog")
       st.image("https://static.streamlit.io/examples/dog.jpg")
    
    with col3:
       st.header("An owl")
       st.image("https://static.streamlit.io/examples/owl.jpg")

# /* Style columns */
[data-testid="column"] {
    box-shadow: rgb(0 0 0 / 20%) 0px 2px 1px -1px, rgb(0 0 0 / 14%) 0px 1px 1px 0px, rgb(0 0 0 / 12%) 0px 1px 3px 0px;
    border-radius: 15px;
    padding: 5% 5% 5% 10%;
} 

# /* Style containers */
[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    border: 20px groove red; white-space: nowrap;
}
