import pandas as pd

def clean_string(s):
    """Pulisce e normalizza una stringa per l'uso in Prolog."""
    return s.replace("'", "").encode('ascii', 'ignore').decode()

class KnowledgeBase:
    def createKnowledgeBase(self):
        # Lettura del dataset
        df = pd.read_csv('../dataset/pre-processato/pre_processed_dataset.csv')

        # Pulizia dei dati
        columns_to_string = ['title', 'description', 'production_countries', 'streaming_service', 'genre', 'actors']
        df[columns_to_string] = df[columns_to_string].apply(lambda x: x.apply(clean_string))

        # Creazione del file Prolog
        with open('KB.pl', 'w') as f:
            # Direttiva per predicati discontigui
            f.write(":- discontiguous title/2.\n")
            f.write(":- discontiguous description/2.\n")
            f.write(":- discontiguous release_year/2.\n")
            f.write(":- discontiguous runtime/2.\n")
            f.write(":- discontiguous genre/2.\n")
            f.write(":- discontiguous actors/2.\n")
            f.write(":- discontiguous production_countries/2.\n")
            f.write(":- discontiguous streaming_service/2.\n")
            f.write(":- discontiguous monthly_subscription_cost/2.\n")

            # Scrittura dei fatti
            for index, row in df.iterrows():
                f.write(f"title({row['id']}, '{row['title']}').\n")
                f.write(f"description({row['id']}, '{row['description']}').\n")
                f.write(f"release_year({row['id']}, {row['release_year']}).\n")
                f.write(f"runtime({row['id']}, {row['runtime']}).\n")
                f.write(f"genre({row['id']}, '{row['genre']}').\n")
                f.write(f"actors({row['id']}, '{row['actors']}').\n")
                f.write(f"production_countries({row['id']}, '{row['production_countries']}').\n")
                f.write(f"streaming_service({row['id']}, '{row['streaming_service']}').\n")
                f.write(f"monthly_subscription_cost({row['id']}, {row['monthly_subscription_cost']}).\n")

            # Scrittura delle regole
            rules = [
                # Prezzo di sottoscrizione
                "prezzo_economy(ID) :- monthly_subscription_cost(ID, Cost), Cost < 9.99.\n",
                "prezzo_medio(ID) :- monthly_subscription_cost(ID, Cost), Cost = 9.99.\n",
                "prezzo_costoso(ID) :- monthly_subscription_cost(ID, Cost), Cost > 9.99.\n",

                # Anno di uscita
                "film_recente(ID) :- release_year(ID, Uscita), Uscita > 2010.\n",
                "film_tra_2000_2010(ID) :- release_year(ID, Uscita), 2000 =< Uscita, Uscita =< 2010.\n",
                "film_pre_2000(ID) :- release_year(ID, Uscita), Uscita < 2000.\n",

                # Genere principale
                "film_genre(ID, Genre) :- genre(ID, Genre).\n",

                # Durata del film
                "film_breve_durata(ID) :- runtime(ID, Durata), Durata =< 60.\n",
                "film_media_durata(ID) :- runtime(ID, Durata), 60 < Durata, Durata =< 90.\n",
                "film_lunga_durata(ID) :- runtime(ID, Durata), Durata > 90.\n",

                # Utilizzo di film_durata per ottenere la durata in categorie
                "film_durata(ID, breve) :- film_breve_durata(ID).\n",
                "film_durata(ID, media) :- film_media_durata(ID).\n",
                "film_durata(ID, lunga) :- film_lunga_durata(ID).\n",

                # Combinazioni di anno e genere
                "recente_genre(ID, Genre) :- film_recente(ID), film_genre(ID, Genre).\n",
                "tra_2000_2010_genre(ID, Genre) :- film_tra_2000_2010(ID), film_genre(ID, Genre).\n",
                "pre_2000_genre(ID, Genre) :- film_pre_2000(ID), film_genre(ID, Genre).\n",

                # Combinazioni di anno, genere e durata
                "recente_genre_durata(ID, Genre, DurataCat) :- recente_genre(ID, Genre), film_durata(ID, DurataCat).\n",
                "tra_2000_2010_genre_durata(ID, Genre, DurataCat) :- tra_2000_2010_genre(ID, Genre), film_durata(ID, DurataCat).\n",
                "pre_2000_genre_durata(ID, Genre, DurataCat) :- pre_2000_genre(ID, Genre), film_durata(ID, DurataCat).\n",
            ]

            for rule in rules:
                f.write(rule)

            # Combinazioni per ogni genere
            genres = ['western', 'scifi', 'romance', 'drama', 'horror', 'thriller', 'comedy', 'crime', 'documentation',
                      'family', 'action', 'fantasy', 'animation', 'music', 'history', 'war', 'european', 'sport',
                      'reality']

            for genre in genres:
                f.write(f"recente_{genre}_breve(ID) :- recente_genre_durata(ID, '{genre}', breve).\n")
                f.write(f"recente_{genre}_media(ID) :- recente_genre_durata(ID, '{genre}', media).\n")
                f.write(f"recente_{genre}_lunga(ID) :- recente_genre_durata(ID, '{genre}', lunga).\n")
                f.write(f"tra_2000_2010_{genre}_breve(ID) :- tra_2000_2010_genre_durata(ID, '{genre}', breve).\n")
                f.write(f"tra_2000_2010_{genre}_media(ID) :- tra_2000_2010_genre_durata(ID, '{genre}', media).\n")
                f.write(f"tra_2000_2010_{genre}_lunga(ID) :- tra_2000_2010_genre_durata(ID, '{genre}', lunga).\n")
                f.write(f"pre_2000_{genre}_breve(ID) :- pre_2000_genre_durata(ID, '{genre}', breve).\n")
                f.write(f"pre_2000_{genre}_media(ID) :- pre_2000_genre_durata(ID, '{genre}', media).\n")
                f.write(f"pre_2000_{genre}_lunga(ID) :- pre_2000_genre_durata(ID, '{genre}', lunga).\n")

# Creazione della base di conoscenza
kb = KnowledgeBase()
kb.createKnowledgeBase()
