import os
import streamlit as st
import pickle
import pandas as pd
import requests

from dotenv import load_dotenv
load_dotenv()


st.markdown("""
<style>
body {
    background-color: #0E1117;
}

h1 {
    color: #FF4B4B;
    text-align: center;
}

.stSelectbox label {
    font-size: 18px;
    color: white;
}

.stButton>button {
    background-color: #FF4B4B;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 180px;
    font-size: 16px;
}

img {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)



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

def fetch_poster(movie_id):
    api_key = os.getenv("API_KEY")



    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
        data = requests.get(url).json()

        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        pass

    return "https://via.placeholder.com/500x750?text=No+Image"

    

# --- RECOMMENDER FUNCTION ---

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),
                       reverse=True,
                       key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


# --- STREAMLIT UI ---
st.title("Movie Recommender System")
st.markdown(
    "<h4 style='text-align: center;'>Get personalized movie recommendations instantly 🎬</h4>",
    unsafe_allow_html=True
)


selected_movie = st.selectbox("Type or select a movie from the dropdown", movies['title'].values)

if st.button('Recommend'):
    with st.spinner('Finding best movies for you...'):
        names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.caption(names[0])

    with col2:
        st.image(posters[1])
        st.caption(names[1])

    with col3:
        st.image(posters[2])
        st.caption(names[2])

    with col4:
        st.image(posters[3])
        st.caption(names[3])

    with col5:
        st.image(posters[4])
        st.caption(names[4])
