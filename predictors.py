import streamlit as sl
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

import warnings
warnings.filterwarnings('ignore')

from datetime import timedelta, date, datetime
from dateutil.relativedelta import relativedelta

import sys

from bs4 import BeautifulSoup
import requests
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



def get_image(X):
    soup_url = "https://www.imdb.com/title/"
    headers = {'Accept-Language': 'en-US,en;q=0.8', 'user-agent': 'mozilla/5.0'}
    # headers= {}
    response = requests.get(f'{soup_url}{X}', headers = headers)

    if response.status_code != 200:# 200 status code means OK!   
        sys.exit(f"The Soup was to cold. Error: {response.status_code}")
    else:
        kitchen = ""

    soup = BeautifulSoup(response.content, "html.parser")
    img = soup.select("img", {'class': 'ipc-image'})[1]['src']

    return(img)

# def get_title(X):
#     soup_url = "https://www.imdb.com/title/"
#     headers = {'Accept-Language': 'en-US,en;q=0.8', 'user-agent': 'mozilla/5.0'}
#     # headers= {}
#     response = requests.get(f'{soup_url}{X}', headers = headers)
    
#     if response.status_code != 200:# 200 status code means OK!   
#         sys.exit(f"The Soup was to cold. Error: {response.status_code}")
#     else:
#         kitchen = ""
    
#     soup = BeautifulSoup(response.content, "html.parser")
#     entry=soup.select("title")[0].get_text().split(' -')[0] # Fetch Movie title
    
#     return(entry)
def get_title(X):

    titles_url = 'https://drive.google.com/file/d/1Z3vHbjAeTAmFp-NeM-j4zYJjLz-fpqfn/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id='
    tit_df = pd.read_csv(path+titles_url.split('/')[-2])
    
    title = tit_df.loc[tit_df['movieId'] == X,'title'].values[0]
    return(title)


#### Popular Ursula
def pop_movies(wf, alt = 10, period = 'all', time_mod = '2020-06-01'):     #period of time accepted: 'all', 'weeks', 'date', 'months', 'years', 'days'

    ok_period = ['all', 'weeks', 'date', 'months', 'years', 'days']

    if period in ok_period:
        if period == 'days':
            if type(time_mod)==int:
                filter_time = datetime.timestamp(datetime.utcnow()-timedelta(days=int(time_mod)))
                wf = wf.loc[wf['timestamp'] >= filter_time]
            else:
                sys.exit(f"time_mod has to be numeric to work with period = {period}")   
        if period == 'weeks':
            if type(time_mod)==int:
                filter_time = datetime.timestamp(datetime.utcnow()-timedelta(weeks=int(time_mod)))
                wf = wf.loc[wf['timestamp'] >= filter_time]
            else:
                sys.exit(f"time_mod has to be numeric to work with period = {period}")   
        if period == 'months':
            if type(time_mod)==int:
                filter_time = datetime.timestamp(datetime.utcnow()-relativedelta(months=int(time_mod)))
                wf = wf.loc[wf['timestamp'] >= filter_time]
            else:
                sys.exit(f"time_mod has to be numeric to work with period = {period}")   
        if period == 'years':
            if type(time_mod)==int:
                filter_time = datetime.timestamp(datetime.utcnow()-relativedelta(years=int(time_mod)))
                wf = wf.loc[wf['timestamp'] >= filter_time]
            else:
                sys.exit(f"time_mod has to be numeric to work with period = {period}")
        if period == 'date':
            if type(time_mod)==int:
                sys.exit(f"time_mod has to be a string like that: 'year-month-day' to work with period = {period}")
            else:
                if len(time_mod.split('-')) == 3:
                    if (time_mod.split('-')[0].isnumeric()) & (time_mod.split('-')[1].isnumeric()) & (time_mod.split('-')[2].isnumeric()) & (int(time_mod.split('-')[1]) in (range(1,13))) & (int(time_mod.split('-')[2]) in (range(1,32))):
                        f_year = int(time_mod.split('-')[0])
                        f_month = int(time_mod.split('-')[1])
                        f_day = int(time_mod.split('-')[2])
                        filter_time = datetime.timestamp(datetime(f_year, f_month, f_day))
                        wf = wf.loc[wf['timestamp'] >= filter_time]
                else:
                    sys.exit(f"time_mod has to be a string like that: 'year-month-day' to work with period = {period}")
        else:
            wf=wf
    else:
        sys.exit("Period input not supported. Supported are: 'all', 'week', 'date', 'month', 'year', 'days'")   

    wf['clean_rate']=(
        (wf['rating'])*(
            (
                wf.groupby('userId')['userId'].transform('count')   # How often does the User make Ratings
            ) * (
                (
                    wf.groupby('userId')['rating'].transform('max')-wf.groupby('userId')['rating'].transform('min')   # Span of User Ratings kicks out single ratings or users that alway rate the same
                )
            )
        )
    )

    clean_rating = pd.DataFrame(wf.groupby('movieId')['clean_rate'].mean())   #mean Rating per Place
    clean_rating['rating_count'] = wf.groupby('movieId')['rating'].count()    #amount of Ratings per place
    clean_rating['rating'] =  wf.groupby('movieId')['rating'].mean()

    clean_rating['recommendation']=(        #Multiplying Ratings and rating-amount
        (clean_rating['clean_rate'])
        ) * (
        (clean_rating['rating_count'])
        )

    result = clean_rating.copy()

    result = result.sort_values('recommendation', ascending=False)[['rating', 'rating_count']].head(alt)

    result.reset_index(inplace=True)
    result['title']= result['movieId'].apply(get_title)
    result['img'] = result['movieId'].apply(get_image)
    result.set_index('movieId', drop=True, inplace=True)
    
    return(result)


# your code here
#### All in One Function
def similar_movies(wf, alt = 10, movie_id= 'tt0372784', minbo = 80):

    ## Filter location visited min minbo times
    filtered_df = wf[wf['movieId'] == movie_id]
    visitors = filtered_df['userId'].unique()
    filtered_df = wf[wf['userId'].isin(visitors)]
    count_table = filtered_df['movieId'].value_counts().reset_index()
    count_table.columns = ['movieId', 'count']
    count_table=count_table.loc[count_table['count']>=minbo,'movieId']

    keeper = wf.copy()

    wf=wf.loc[wf['movieId'].isin(count_table)]


    wf['clean_rate']=(
        (wf['rating'])*(
            (
                keeper.groupby('userId')['userId'].transform('count')   # How often does the User make Ratings
            ) * (
                (
                    keeper.groupby('userId')['rating'].transform('max')-keeper.groupby('userId')['rating'].transform('min')   # Span of User Ratings kicks out single ratings or users that alway rate the same
                )
            )
        )
    )

    places_crosstab = pd.pivot_table(data=wf, values='clean_rate', index='userId', columns='movieId')

    also_there = places_crosstab[movie_id]
    also_there[also_there>=0] # exclude NaNs

    similar_ratings = places_crosstab.corrwith(also_there)

    corr_tab = pd.DataFrame(similar_ratings, columns=['PearsonR'])
    corr_tab.dropna(inplace=True)

    clean_rating = pd.DataFrame(wf.groupby('movieId')['clean_rate'].mean())   #mean Rating per Place
    clean_rating['rating_count'] = wf.groupby('movieId')['rating'].count()    #amount of Ratings per place
    clean_rating['rating'] =  wf.groupby('movieId')['rating'].mean()


    clean_rating['recommendation']=(        #Multiplying Ratings and rating-amount
        (clean_rating['clean_rate'])
        ) * (
        np.log(clean_rating['rating_count'])#/(clean_rating['rating_count'].max())
        )

    corr_tab_summary = corr_tab.join(clean_rating[['recommendation', 'rating_count', 'rating']])
    corr_tab_summary.drop(movie_id, inplace=True) # drop Tortas Locas itself
    corr_tab_summary['recommendation'] = corr_tab_summary['recommendation'] * corr_tab_summary['PearsonR']

    result = corr_tab_summary.sort_values('recommendation', ascending=False)[['rating', 'PearsonR', 'rating_count']].head(alt)

    result.reset_index(inplace=True)
    result['title'], result['img'] = result['movieId'].apply(get_title)
    result['img'] = result['movieId'].apply(get_image)
    result.set_index('movieId', drop=True, inplace=True)

    return(result)


# your code here

def similar_taste(wf, alt = 10, u_id= 'ur4592644', minbo = 30):
    

    ## Filter location visited min minbo times
    filtered_df = wf[wf['userId'] == u_id]
    movies = filtered_df['movieId'].unique()
    filtered_df = wf[wf['movieId'].isin(movies)]
    count_table = filtered_df['userId'].value_counts().reset_index()
    count_table.columns = ['userId', 'count']
    count_table=count_table.loc[count_table['count']>=minbo,'userId']

    keeper = wf.copy()

    wf=wf.loc[wf['userId'].isin(count_table)]

    only_known = wf.copy()
    only_known.loc[only_known['userId']==u_id,'movieId']
    only_known.loc[only_known['movieId'].isin(only_known.loc[only_known['userId']==u_id,'movieId'])]

    users_items = pd.pivot_table(
        data=wf,
        values='rating',
        index='userId',
        columns='movieId'
    )

    known_items = pd.pivot_table(
        data=only_known,
        values='rating',
        index='userId',
        columns='movieId'
    )

    users_items.fillna(0, inplace=True)
    known_items.fillna(0, inplace=True)

    user_similarities = pd.DataFrame(
        cosine_similarity(known_items),
        columns=known_items.index,
        index=known_items.index
    )

    weights = (
        user_similarities.query("userId!=@u_id")[u_id] / sum(user_similarities.query("userId!=@u_id")[u_id])
    )
        
    # select restaurants that the inputed user has not visited
    not_visited_restaurants = users_items.loc[users_items.index!=u_id, users_items.loc[u_id,:]==0]

    # dot product between the not-visited-restaurants and the weights
    weighted_averages = pd.DataFrame(not_visited_restaurants.T.dot(weights), columns=["predicted_rating"])

    result = weighted_averages.sort_values("predicted_rating", ascending=False).head(alt)

    result.reset_index(inplace=True)
    result['title'] = result['movieId'].apply(get_title)
    result['img'] = result['movieId'].apply(get_image)
    result.set_index('movieId', drop=True, inplace=True)
    
    return(result)


