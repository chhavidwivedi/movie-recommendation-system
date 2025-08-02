import streamlit as st
import pickle
import pandas as pd
import requests

# --- UTIL FUNCTION ---
def fetch_file_from_gdrive(gdrive_url, filename):
    import gdown
    file_id = gdrive_url.split("/d/")[1].split("/")[0]
    gdown.download(f"https://drive.google.com/uc?id={file_id}", filename, quiet=False)

# --- DOWNLOAD FILES IF NOT PRESENT ---
if not os.path.exists("similarity.pkl"):
    fetch_file_from_gdrive("https://drive.google.com/file/d/1zKUw0M_wxrx9ohSHnbE2CohI6hHWGuad/view?usp=sharing", "similarity.pkl")

if not os.path.exists("movies_dict.pkl"):
    fetch_file_from_gdrive("https://drive.google.com/file/d/1iMr7oPInLqoIZEBlLw--mIfLqKmZNti-/view?usp=sharing", "movies_dict.pkl")

# --- LOAD FILES ---
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# --- RECOMMENDER FUNCTION ---
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = [movies.iloc[i[0]].title for i in distances[1:6]]
    return recommended_movies

# --- STREAMLIT UI ---
st.title("Movie Recommender System")

selected_movie = st.selectbox("Type or select a movie from the dropdown", movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie)
    for i in recommendations:
        st.write(i)
