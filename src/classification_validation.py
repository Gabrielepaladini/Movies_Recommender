import sklearn
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import RepeatedKFold

from recommenderSystem import get_recommendation

def RandomizedSearch(hyperparameters, X_train, y_train):
    knn = KNeighborsClassifier()

    cvFold = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    randomSearch = RandomizedSearchCV(estimator=knn, cv=cvFold, param_distributions=hyperparameters)

    best_model = randomSearch.fit(X_train, y_train)
    return best_model

def ModelEvaluation(y_test, y_pred, pred_prob):
    print("Classification Report: \n", classification_report(y_test, y_pred))

    roc_score = roc_auc_score(y_test, pred_prob, multi_class='ovr')
    print("ROC Score: ", roc_score)

    return roc_score

def HyperparametersSearch(X_train, X_test, y_train, y_test):
    result = {}
    n_neighbors = list(range(1, 30))
    weights = ['uniform', 'distance']
    metric = ['euclidean', 'manhattan', 'hamming']

    hyperparameters = dict(metric=metric, weights=weights, n_neighbors=n_neighbors)

    i = 0
    while i < 15:
        best_model = RandomizedSearch(hyperparameters, X_train, y_train)
        bestweights = best_model.best_estimator_.get_params()['weights']
        bestMetric = best_model.best_estimator_.get_params()['metric']
        bestNeighbours = best_model.best_estimator_.get_params()['n_neighbors']

        knn = KNeighborsClassifier(n_neighbors=bestNeighbours, weights=bestweights, algorithm='auto', metric=bestMetric, metric_params=None, n_jobs=None)
        knn.fit(X_train, y_train)

        pred_prob = knn.predict_proba(X_test)

        #valutiamo il nostro modello
        roc_score = roc_auc_score(y_test, pred_prob, multi_class='ovr')

        result[i] = {'n_neighbors': bestNeighbours, 'metric': bestMetric, 'weights': bestweights, 'roc_score': roc_score}
        i += 1

    result = dict(sorted(result.items(), key=lambda x: x[1]['roc_score'], reverse=True))

    first_e1 = list(result.keys())[0]
    result = list(result[first_e1].values())
    return result

def SearchingBestModelStats(X_train, X_test, y_train, y_test):
    print("\n\nComposizione iniziale del modello con iper-parametri di base...")
    knn = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto', p=2, metric='minkowski', metric_params=None, n_jobs=None)
    knn.fit(X_train, y_train)

    print("\nPredizioni dei primi 5 elementi: ", knn.predict(X_test)[0:5], 'Valori effettivi: ', y_test[0:5])

    y_pred = knn.predict(X_test)
    pred_prob = knn.predict_proba(X_test)

    print("\nValutazione del modello...\n")
    ModelEvaluation(y_test, y_pred, pred_prob)

    print("\nProviamo a migliorare il nostro modello determinando gli iper-parametri ottimali con 'Grid Search':\n")

    result = {}
    result = HyperparametersSearch(X_train, X_test, y_train, y_test)

    print("\nGRID SEARCH:\n")

    bestweights = result[2]
    print("Best Weights: ", bestweights)

    bestmetric = result[1]
    print("Best Metric: ", bestmetric)

    bestNeighbours = result[0]
    print("Best n_eighbours: ", bestNeighbours)

    #ricomposizione del modello utilizzando i nuovi iper-parametri
    print("\nRicomponiamo il modello utilizzando i nuovi iper-parametri: ")
    knn = KNeighborsClassifier(n_neighbors=bestNeighbours, weights=bestweights, algorithm='auto', metric=bestmetric, metric_params=None, n_jobs=None)
    knn.fit(X_train, y_train)

    print("\nPredizione dei primi 5 elementi: ", knn.predict(X_test)[0:5], "Valori effettivi: ", y_test[0:5])
    y_pred = knn.predict(X_test)
    pred_prob = knn.predict_proba(X_test)

    #valutiamo il nostro modello
    ModelEvaluation(y_test, y_pred, pred_prob)

    print("\nOra possiamo procede alla fase di recommandation...")

    return knn

def main_recommender():
    movie_data = pd.read_csv('../dataset/pre-processato/pre_processed_dataset.csv')

    #creiamo la categoria star
    movie_data['star'] = ((movie_data['imdb_score'] + movie_data['tmdb_score']) / 2)

    #assegnamo i dati alla sezione corretta
    movie_data.loc[(movie_data['star'] >= 7.5), ['star']] = 5
    movie_data.loc[(movie_data['star'] < 7.5) & (movie_data['star'] >= 5), 'star'] = 4
    movie_data.loc[(movie_data['star'] < 5) & (movie_data['star'] >= 3), 'star'] = 3
    movie_data.loc[(movie_data['star'] < 3) & (movie_data['star'] >= 1.5), 'star'] = 2
    movie_data.loc[(movie_data['star'] < 1.5)] = 1

    knn_data = movie_data[['id', 'runtime', 'star', 'imdb_score', 'tmdb_score']].copy()

    x = knn_data.drop(columns=['star'])
    y = knn_data['star'].values

    movie_index = get_recommendation()

    recommend_data = movie_data[['title', 'release_year', 'genre', 'streaming_service', 'star']].iloc[movie_index]
    predict_data = movie_data[['id', 'runtime', 'imdb_score', 'tmdb_score']].iloc[movie_index]

    #dividiamo il dataset in due parti, 80% destinato al training e 20% destinato al testing
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1, stratify=y)

    #traformiamo i dati per renderli adeguati
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    predict_data = scaler.transform(predict_data)

    knn = SearchingBestModelStats(X_train, X_test, y_train, y_test)

    #alleniamo il modello sulla parte di training
    knn.fit(X_train, y_train)

    #facciamo predizioni sui nuovi dati
    star_prediction = knn.predict(predict_data)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    recommend_data['star_prediction'] = star_prediction

    print("\nEcco una lista di 5 film più simili a quello indicato, con una predizione sulla categoria star:\n", recommend_data, "\n")



