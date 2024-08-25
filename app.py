from copyreg import pickle
from http.client import responses

import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=6639c8933135aa75387631bcb6b4f137&language=en-US'.format(movie_id))
    data=response.json()
    print(data)
    if "poster_path" in data and data["poster_path"]:
        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


def recommend(movie):  #given movie
  movie_indecies=movies[movies['title']==movie].index[0] #find the index
  distances=similarity[movie_indecies]   #finding the distance
  movies_list=sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1]) [1:6]

  recommended_movies=[]
  recommmended_movies_posters=[]
  for i in movies_list:
      movies_id=movies.iloc[i[0]].movie_id
      recommended_movies.append(movies.iloc[i[0]].title)
      # fetch poster from api
      recommmended_movies_posters.append(fetch_poster(movies_id))
  return recommended_movies,recommmended_movies_posters

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name=st.selectbox(
    'how would you like to be contacted?',
    movies['title'].values
)
if st.button('Recommend'):
    name,posters=recommend(selected_movie_name)
    print(posters)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])
    with col2:
        st.text(name[1])
        st.image(posters[1])
    with col3:
        st.text(name[2])
        st.image(posters[2])
    with col4:
        st.text(name[3])
        st.image(posters[3])
    with col5:
        st.text(name[4])
        st.image(posters[4])
