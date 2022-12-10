import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import pickle
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder


FILE_PATH = 'D:/Coding/Python/game-recommendation-system/finaldata.csv'

def label_encode(df, old_cols, new_cols):

    le = LabelEncoder()
    cols = zip(old_cols, new_cols)
    for i, j in cols:
        df[j] = le.fit_transform(df[i])
    df.drop(old_cols, axis=1, inplace=True)

    return df

def extract_release_year(df, date, releaseYear):

    df[releaseYear] = pd.DatetimeIndex(df[date]).year
    df[releaseYear] = df[releaseYear].astype(np.int64)
    df.drop(date, axis=1, inplace=True)

    return df

def clustering_features(df, cols_to_remove):

    X = df.drop(cols_to_remove, axis=1)
    return X



dataframe = pd.read_csv(FILE_PATH)
game_titles = dataframe['name'].tolist()
X = dataframe.pipe(label_encode, old_cols=['publisher','genre'], new_cols=['publisher_enc', 'genre_enc']).pipe(
                   extract_release_year, date='release_date', releaseYear='year').pipe(
                   clustering_features, ['name', 'img_url'])

model = NearestNeighbors(n_neighbors=11, algorithm='brute')

model.fit(X)

# WARNING!: Only uncomment if you wish to rewrite the pickle files

# pickle.dump(model, open('pickle/model.pkl', 'wb'))
# pickle.dump(dataframe, open('pickle/dataframe.pkl', 'wb'))
# pickle.dump(game_titles, open('pickle/gamelist.pkl', 'wb'))
# pickle.dump(X, open('pickle/features.pkl', 'wb'))



