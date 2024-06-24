import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(page_title='Flick Finder', layout='wide')

############################################
# LOAD THE SAVED MODEL AND MOVIE LIST
############################################
movies = pickle.load(open('assets/movies.pkl', 'rb'))
similarity = pickle.load(open('assets/similarity.pkl', 'rb'))
movies = pd.DataFrame(movies)

st.title('Flick Finder')
st.image('assets/movie.jpg')


def get_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=fb10192a0f29f8c7185ffd9cbb2e8df4&language=en-US".format(
        movie_id)
    try:
        data = requests.get(url).json()
        path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        return path
    except:
        return "https://via.placeholder.com/500?text=No+Image"


############################################
# RECOMMENDER FUNCTION
############################################
def get_recommendations(movie_name):
    index = movies[movies['title'] == movie_name].index[0]
    distance = similarity[index]
    recommendations = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:13]
    movie, poster = [], []
    for i in recommendations:
        movie_id = movies.iloc[i[0]]['id']
        movie.append(movies.iloc[i[0]]['title'])
        poster.append(get_poster(movie_id))
    return movie, poster


query = st.selectbox(
    label='Select Movie',
    options=movies['title'],
    placeholder='Select Movie',
    label_visibility='collapsed',
    index=None
)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = get_recommendations(query)
    cols = st.columns(4)
    for i in range(len(recommended_movie_names)):
        with cols[i % 4]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i], use_column_width=True)
