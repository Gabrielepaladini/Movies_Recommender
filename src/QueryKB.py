from pyswip import Prolog


def main():
    prolog = Prolog()
    prolog.consult('KB.pl')  # Assicurati che questo carichi correttamente la tua KB
    film_ids = []  # Lista per memorizzare i risultati della ricerca

    while True:
        try:
            choice = int(input("\nScegliere quale funzione eseguire:\n"
                               "1) Trova un film date determinate caratteristiche\n"
                               "2) Sulla base delle preferenze dell'utente, trovare la piattaforma migliore per i film selezionati.\n"
                               "3) Esci\n"
                               "\nInserisci un valore: "))
            if choice == 1:
                film_ids = query_filmstreaming(prolog)
            elif choice == 2:
                if film_ids:
                    find_best_streaming_platform(prolog, film_ids)
                else:
                    print("Esegui prima una ricerca di film (opzione 1).")
            elif choice == 3:
                print("Uscita dal programma.")
                break
            else:
                print("Input non valido. Utilizzare solo 1, 2 o 3.")
        except ValueError:
            print("Input non valido. Inserisci un numero.")


def query_filmstreaming(prolog):
    uscita = None
    genere = None
    durata = None
    film_ids = []  # Lista per salvare gli ID dei film trovati

    # Gestione del periodo
    while uscita is None:
        try:
            uscita_input = int(input("\nInserisci il periodo relativo all'anno di uscita del film\n"
                                     "1) recente\n2) tra 2000 e 2010\n3) pre 2000\n"))
            if uscita_input == 1:
                uscita = "recente"
            elif uscita_input == 2:
                uscita = "tra_2000_2010"
            elif uscita_input == 3:
                uscita = "pre_2000"
            else:
                print("Input non valido. Utilizzare solo 1, 2 o 3.")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

    # Gestione del genere
    while genere is None:
        try:
            genere_input = int(input("Inserisci il genere cui vorresti appartenga il film\n"
                                     "1) western\n2) scifi\n3) romance\n4) drama\n5) horror\n6) thriller\n7) comedy\n"
                                     "8) crime\n9) documentation\n10) family\n11) action\n12) fantasy\n13) animation\n"
                                     "14) music\n15) history\n16) war\n17) european\n18) sport\n19) reality\n"))
            genres = ["western", "scifi", "romance", "drama", "horror", "thriller", "comedy", "crime",
                      "documentation", "family", "action", "fantasy", "animation", "music", "history",
                      "war", "european", "sport", "reality"]
            if 1 <= genere_input <= 19:
                genere = genres[genere_input - 1]
            else:
                print("Input non valido. Utilizzare solo da 1 a 19.")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

    # Gestione della durata
    while durata is None:
        try:
            durata_input = int(input("Inserisci la durata del film\n1) breve\n2) media\n3) lunga\n"))
            if durata_input == 1:
                durata = "breve"
            elif durata_input == 2:
                durata = "media"
            elif durata_input == 3:
                durata = "lunga"
            else:
                print("Input non valido. Utilizzare solo 1, 2 o 3.")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

    # Creazione della query
    query = f"{uscita}_{genere}_{durata}(ID)"  # Crea la query dinamica in base agli input

    # Esecuzione della query e gestione dei risultati
    try:
        results = list(prolog.query(query))  # Esegui la query su Prolog
        if len(results) == 0:
            print("Con questi filtri non vi sono risultati.")
        else:
            ids_set = set()  # Creiamo un set per eliminare duplicati
            print("Gli ID dei film che rispettano i filtri sono:")
            for soln in results:
                if soln["ID"] not in ids_set:  # Controlliamo se l'ID è già stato stampato
                    print(soln["ID"])  # Stampa l'ID del film
                    film_ids.append(soln["ID"])  # Aggiungiamo l'ID alla lista
                    ids_set.add(soln["ID"])  # Aggiungiamo l'ID al set per evitare duplicati
    except Exception as e:
        print(f"Errore durante l'esecuzione della query: {e}")

    return film_ids  # Restituiamo gli ID dei film trovati


def find_best_streaming_platform(prolog, film_ids):
    platform_count = {}
    price_filters = []

    # Selezione del prezzo
    while not price_filters:
        try:
            price_input = int(input("Seleziona il tipo di sottoscrizione:\n"
                                    "1) economica\n2) media\n3) costosa\n"))
            if price_input == 1:
                price_filters = ["prezzo_economy"]  # Solo economico
            elif price_input == 2:
                price_filters = ["prezzo_economy", "prezzo_medio"]  # Economico o medio
            elif price_input == 3:
                price_filters = ["prezzo_economy", "prezzo_medio", "prezzo_costoso"]  # Economico, medio o costoso
            else:
                print("Input non valido. Utilizzare solo 1, 2 o 3.")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

    # Iteriamo su tutti gli ID dei film trovati e cerchiamo su quale piattaforma si trovano
    for film_id in film_ids:
        query = f"streaming_service({film_id}, Piattaforma)"  # Usare il predicato corretto per la piattaforma
        try:
            results = list(prolog.query(query))
            for result in results:
                piattaforma = result["Piattaforma"]

                # Verifichiamo il prezzo della piattaforma con uno dei predicati selezionati
                price_match = False
                for price_filter in price_filters:
                    price_query = f"{price_filter}({film_id})"
                    price_results = list(prolog.query(price_query))
                    if price_results:  # Se il film è disponibile per quel tipo di sottoscrizione
                        price_match = True
                        break

                if price_match:
                    if piattaforma in platform_count:
                        platform_count[piattaforma] += 1
                    else:
                        platform_count[piattaforma] = 1
        except Exception as e:
            print(f"Errore durante l'esecuzione della query per {film_id}: {e}")

    if platform_count:
        # Troviamo la piattaforma con il maggior numero di film
        best_platform = max(platform_count, key=platform_count.get)
        print(f"La migliore piattaforma consigliata è: {best_platform}")
        print(f"Numero di film disponibili su {best_platform}: {platform_count[best_platform]}")
    else:
        print("Non è stato trovato nessun film su alcuna piattaforma con il prezzo selezionato.")


if __name__ == "__main__":
    main()
