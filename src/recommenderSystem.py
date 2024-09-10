import numpy as np
import pandas as pd
import sklearn

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.stats import pearsonr

def get_info():
    print("Inseisci i dati con la lettera maiuscola iniziale\n")

    title = input("Inserisci il titolo: \n")
    genre = input("Inserisci il genere: \n")
    year = input("Inserisci l'anno di uscita: \n")

    #creiamo un dataframe temporaneo che contiene i dati inseriti dall'utente
    user_data = pd.DataFrame({'title': title, 'genre': genre, 'year': year}, index=[0])
    return user_data

def construct_recommendation(filename, user_data):
    movie_data = pd.read_csv(filename)
    movie_data = movie_data[['title', 'description', 'release_year', 'runtime', 'production_countries', 'imdb_score', 'tmdb_score', 'genre', 'streaming_service', 'actors']].copy()

    #controllo se l'elemento indicato dall'utente è presente o meno nel dataset.
    #se non è presente lo aggiungo e memorizzo il suo indice.

    control = 0

    for title in movie_data['title']:
        if user_data['title'][0] != title:
            index = 0
            control = 1
        else:
            index = movie_data.index[movie_data['title'] == title].values[0]
            control = 0
            break

    if control == 1:
        movie_data = pd.concat([user_data, movie_data], ignore_index=True)

    movie_data['all_content'] = (
        movie_data['title'].astype(str) + ';' +
        movie_data['release_year'].astype(str) + ';' +
        movie_data['runtime'].astype(str) + ';' +
        movie_data['production_countries'].astype(str) + ';' +
        movie_data['genre'].astype(str)
    )

    #vettorizzazione
    tfidf_matrix = vectorize_data(movie_data)
    tfidf_matrix_array = tfidf_matrix.toarray()

    print("\nInizio ricerca dei film...")

    indices = pd.Series(movie_data['title'].index)
    id = indices[index]

    correlation = []

    for i in range(len(tfidf_matrix_array)):
        correlation.append(pearsonr(tfidf_matrix_array[id], tfidf_matrix_array[i]))
    correlation = list(enumerate(correlation))
    sorted_corr = sorted(correlation, reverse=True, key=lambda x: x[1])[1:6]
    movie_index = [i[0] for i in sorted_corr]

    print(f"Movie_Index trovato: {movie_index}")

    print("\n[5 film più simili a quello inserito sono stati trovati!]")
    print("\nPassaggio all'analisi del modello...")

    return movie_index

def vectorize_data(movie_data):
    vectorizer = TfidfVectorizer(analyzer='word')
    tfidf_matrix = vectorizer.fit_transform(movie_data['all_content'])
    return tfidf_matrix

def get_recommendation():
    print("\nBENVENUTO NEL RECOMMENDER SYSTEM\n")
    print("Digita le caratteristiche del film su cui vuoi che si avii la raccomandazione")

    user_data = get_info()

    while(True):
        print("\nQuesti sono i dati del film che hai inserito: \n")
        print(user_data.head())

        answer = input("\nÈ corretto? (y/n): ")
        if answer == 'n' or answer == 'N':
            user_data = get_info()
            movie_index = construct_recommendation('../dataset/pre-processato/pre_processed_dataset.csv', user_data)
        else:
            movie_index = construct_recommendation('../dataset/pre-processato/pre_processed_dataset.csv', user_data)
            print("\nEcco Movie_Index: \n", movie_index)

        return movie_index