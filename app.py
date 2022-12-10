import pickle
import streamlit as st

st.header("Video Game Recommendation System")

model = pickle.load(open('pickle/model.pkl','rb'))
dataframe = pickle.load(open('pickle/dataframe.pkl','rb'))
features = pickle.load(open('pickle/features.pkl','rb'))
gamelist = pickle.load(open('pickle/gamelist.pkl','rb'))

def recommend(game_title):

    game_id = dataframe.index[dataframe['name']==game_title]
    distance, indices = model.kneighbors(features.iloc[game_id,:])

    for i in indices:
        game_list = dataframe['name'][i].tolist()
        url_list = dataframe['img_url'][i].tolist()
    
    return game_list, url_list

selected_game = st.selectbox(
    "Choose A Game",
    gamelist,
    index=14583
)

if st.button('Recommend'):
    names, urls = recommend(selected_game)
    for i in range(2):
        cols = st.columns(5)
        
        for j,col in enumerate(cols):
            if i == 1:
                j += 5
            with col:
                st.text(names[j+1])
                st.image(urls[j+1])



