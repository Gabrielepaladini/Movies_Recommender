from owlready2 import *


def main_ontology():
    print("\nBENVENUTO NELL'ONTOLOGIA")

    while (True):
        print("\nSeleziona un'operazione:\n1) Visualizzazione Classi\n2) Visualizzazione proprietà d'oggetto\n3)"
              " Visualizzazione proprietà dei dati\n4) Esegui query\n5) Esci dall'Ontologia\n")
        menu_answer = input("Inserisci un valore: ")

        ontology_path = 'Ontologia.owx'
        ontology = get_ontology(ontology_path).load()

        if menu_answer == '1':
            print("CLASSI PRESENTI NELL'ONTOLOGIA: ")
            classes = ontology.classes()

            for item in classes:
                print(f"- {item}")

            while (True):
                print("\nVorresti esplorare meglio una delle seguenti classi?\n\n1) Film\n2) Release_year\n"
                      "3) Streaming_service\n4) Genre\n5) Customer\n6) Film_production_studios\n7) No\n")
                class_answer = input("Inserisci un valore: ")

                if class_answer == '1':
                    print("\nLISTA FILM PRESENTI: ")
                    film = ontology.search(is_a=ontology.Film)
                    for item in film:
                        print(f"- {item}")
                elif class_answer == '2':
                    print("\nLISTA ANNI DI RILASCIO PRESENTI: ")
                    year = ontology.search(is_a=ontology.Release_year)
                    for item in year:
                        print(f"- {item}")
                elif class_answer == '3':
                    print("\nLISTA DEI SERVIZI DI STREAMING PRESENTI: ")
                    streaming_service = ontology.search(is_a=ontology.Streaming_Service)
                    for item in streaming_service:
                        print(f"- {item}")
                elif class_answer == '4':
                    print("\nLISTA DEI GENERI PRESENTI: ")
                    genre = ontology.search(is_a=ontology.Genre)
                    for item in genre:
                        print(f"- {item}")
                elif class_answer == '5':
                    print("\nLISTA DEI CLIENTI PRESENTI: ")
                    customer = ontology.search(is_a=ontology.Customer)
                    for item in customer:
                        print(f"- {item}")
                elif class_answer == '6':
                    print("\nLISTA DEGLI STUDI DI PRODUZIONE PRESENTI: ")
                    film_production_studio = ontology.search(is_a=ontology.Film_production_studios)
                    for item in film_production_studio:
                        print(f"- {item}")
                elif class_answer == '7':
                    break

                else:
                    print("Valore non valido! Inseriscine uno tra quelli presenti.")

                answer = input("\nVuoi esaminare un'altra classe? (y/n): ")
                if answer == 'n' or answer == 'N':
                    break

        elif menu_answer == '2':
            print("\nPROPRIETÁ D'OGGETTO PRESENTI NELL'ONTOLOGIA: ")
            object_properties = ontology.object_properties()
            for item in object_properties:
                print(f"- {item}")
        elif menu_answer == '3':
            print("\nPROPRIETÁ DEI DATI PRESENTI NELL'ONTOLOGIA: ")
            data_properties = ontology.data_properties()
            for item in data_properties:
                print(f"- {item}")
        elif menu_answer == '4':
            while True:
                print("\n1) Lista film presenti su 'Amazon'\n"
                      "2) Lista film di genere 'scifi'\n"
                      "3) Studi di produzione del film 'Deep Water'\n"
                      "4) Torna indietro\n")

                query_choice = input("Inserisci un valore: ")
                if query_choice == '1':
                    print("FILM PRESENTI SU AMAZON: ")
                    amazon_films = ontology.search(is_a=ontology.Film,
                                                   is_distribuited_by=ontology.search(is_a=ontology.Amazon))

                    for item in amazon_films:
                        print(f"- {item}")
                elif query_choice == '2':
                    print("FILM DI GENERE SCI-FI: ")
                    scifi_films = ontology.search(is_a=ontology.Film, has_genre=ontology.search(is_a=ontology.scifi))

                    for item in scifi_films:
                        print(f"- {item}")
                elif query_choice == '3':
                    deep_water = ontology.search_one(is_a=ontology.Film, is_distribuited_by=ontology.Hulu)

                    production_studios = ontology.search(realize=deep_water)

                    if production_studios:
                        print("STUDI DI PRODUZIONE DEL FILM 'DEEP WATER': ")
                        for studio in production_studios:
                            print(f"- {studio}")
                    else:
                        print("Nessuno studio di produzione trovato per il film 'Deep Water'")
                elif query_choice == '4':
                    break



        elif menu_answer == '5':
            break


if __name__ == "__main__":
    main_ontology()