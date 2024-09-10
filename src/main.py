import QueryKB
import mainOntology
import classification_validation

class Main:

    def run(self):
        while True:
            print("\nSeleziona un'operazione:\n1) Recommender System\n2) Interagisci con la KB\n3) Interagisci con l'ontologia\n4) Esci\n")
            choice = input("Inserisci un valore: ")

            if choice == '1':
                print("Recommender System")
                classification_validation.main_recommender()

            elif choice == '2':
                print('Caricamento della KB... Attendi...')
                QueryKB.main()

            elif choice == '3':
                mainOntology.main_ontology()

            elif choice == '4':
                print('Uscita in corso...')
                break

            else:
                print('Valore non valido! Digita 1, 2, 3 o 4.')


if __name__ == "__main__":
    Main().run()