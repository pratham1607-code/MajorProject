import streamlit as st
import json  # to import the model
from KNN import KNearestNeighbours
from operator import itemgetter  # only function is to fetch data


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Load data and movies list from corresponding JSON files
# opened in read append mode coding is utf-8 and object is f
# through f it will load in data
with open(r'data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open(r'titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)


def knn(test_point, k):
    # Create dummy target variable for the KNN Classifier
    # because there is many categorical data or string type of data
    # and the computer easily process the numbers data and it finds difficult with the string data
    target = [0 for item in movie_titles]
    # Instantiate object for the Classifier
    model = KNearestNeighbours(data, target, test_point, k=k)
    # Run the algorithm
    model.fit()
    # Distances to most distant movie
    max_dist = sorted(model.distances, key=itemgetter(0))[-1]
    # Print list of recommendations < Change value of k for a different number >
    table = list()
    for i in model.indices:
        # Returns back movie title and imdb link
        table.append([movie_titles[i][0], movie_titles[i][2]])
    return table


if __name__ == '__main__':
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']

    movies = [title[0] for title in movie_titles]
    st.image(
        "media/image.png"
    )

    st.title('MOVIE  RECOMMENDATION  WEBSITE')
    st.title('~ netflix and chill')
    st.title('This is a simple movie recommender application. You can get the recommendation through input ⤵')
    st.title('🔰 Title.')
    st.title('🔰 Genres.')
    apps = ['--Select Type Of Recommendation--',
            'Enter Title.', 'Enter Genres.']
    app_options = st.selectbox('Select Option:', apps)

    if app_options == 'Enter Title.':
        movie_select = st.selectbox(
            'Select Title:', ['--Select the movie you have watched--'] + movies)
        if movie_select == '--Select the movie you have watched--':
            st.write('')
        else:
            n = st.slider('Number of recommendation: ',
                          min_value=5, max_value=30, step=1)
            genres = data[movies.index(movie_select)]
            test_point = genres
            table = knn(test_point, n)
            for movie, link in table:
                # Displays movie title with link to imdb
                st.subheader(f"[{movie}]({link})")
    elif app_options == apps[2]:
        options = st.multiselect('Select Genres:', genres)
        if options:
            imdb_score = 8  
            n = st.slider('Number of recommendation: ',
                          min_value=5, max_value=30, step=1)
            test_point = [1 if genre in options else 0 for genre in genres]
            test_point.append(imdb_score)
            table = knn(test_point, n)
            for movie, link in table:
                # Displays movie title with link to imdb website
                st.subheader(f"[{movie}]({link})")

    else:
        st.write('')
