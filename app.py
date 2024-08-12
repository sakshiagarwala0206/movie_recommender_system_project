import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/movie_id={movie_id}?language=en-US   "
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer 87f89e2d93df66650b82291baccbbec1"
    }
    response = requests.get(url, headers=headers)
    data=response.json()
    return data


movies = pickle.load(open('movies.pkl', 'rb'))
movies_df=pd.DataFrame(movies)
st.title('Movie Recommender')
similarity=pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
  movie_index=movies_df[movies_df['title']==movie].index[0]
  distances=similarity[movie_index]
  movie_rec=sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])
  recommended_movies=[]
  for i in movie_rec[1:6]:
      # fetch the movie poster
      movie_id = movies.iloc[i[0]].movie_id
      recommended_movies.append(movies.iloc[i[0]].title)
  return recommended_movies


option = st.selectbox(
    "How would you like to be contacted?",
    movies_df['title'],
)

if st.button('Recommend'):
    rec=recommend(option)
    for i in rec:
        st.write(i)

