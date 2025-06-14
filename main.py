import City
import GeneticAlgorithm
import multiprocessing as mp

#konstante
CONST_FILE_NAME = "data_tsp.txt"

CONST_POPULATION_SIZE = 250
CONST_GENERATIONS = 1000
CONST_SAME_STOPPAGE = 450
CONST_MUTATION_RATE = 0.55
CONST_PERCENT_OF_PROTECTION = 0.05
CONST_PERCENT_OF_KEEP = 0.1
CONST_MAX_REPEAT = 5
CONST_PERCENT_OF_RESET = 0.95

#main funkcija koja se izvrsava kada se pokrene skripta
if __name__ == "__main__":
    print("Dobrodosli u program za resavanje problema putujuceg trgovca!")

    #koji fajl sa gradovima ce se koristiti
    file_name=""
    while True:
        print("Koji fajl sa gradovima zelite da koristite?")
        print("1. podrazumevani fajl (data_tsp.txt)")
        print("2. drugi fajl (unesite ime fajla sa gradovima)")
        print("3. izlaz iz programa")
        choice = input("Unesite broj opcije: ")
        if choice == "1":
            file_name = CONST_FILE_NAME
            break
        elif choice == "2":
            file_name = input("Unesite ime fajla sa gradovima: ")
            if not file_name.endswith(".txt"):
                file_name += ".txt"
            break
        elif choice == "3":
            print("Izlaz iz programa...")
            exit(0)
        else:
            print("Nepoznata opcija, molimo unesite ponovo.")
        
    print("Ucitavanje gradova iz fajla:", file_name)
    cities=City.read_cities(file_name)
    if cities is None:
        file_name = CONST_FILE_NAME
        cities = City.read_cities(file_name)

    #da li da koristimo vise instanci algoritma
    while True:
        print("Da li zelite da koristite vise instanci algoritma za resavanje problema putujuceg trgovca?")
        print("1. Da")
        print("2. Ne")
        print("3. Izlaz iz programa")
        choice = input("Unesite broj opcije: ")
        if choice == "1":
            multiple_instances = True

            #koliko instanci da koristimo
            print("Koliko instanci zelite da koristite? (preporuceno " + str(mp.cpu_count()-1) + " ili manje)")
            try:
                number_of_instances = int(input("Unesite broj instanci: "))
                if number_of_instances <= 0 or number_of_instances > mp.cpu_count():
                    print("Broj instanci mora biti izmedju 1 i " + str(mp.cpu_count()) + ". Koristicemo podrazumevani broj instanci (" + str(mp.cpu_count()-1) + ").")
                    number_of_instances = mp.cpu_count() - 1
            except ValueError:
                print("Neispravan unos, koristimo podrazumevani broj instanci (" + str(mp.cpu_count()-1) + ").")
                number_of_instances = mp.cpu_count() - 1

            break
        elif choice == "2":
            multiple_instances = False
            break
        elif choice == "3":
            print("Izlaz iz programa...")
            exit(0)
        else:
            print("Nepoznata opcija, molimo unesite ponovo.")

    #parametri algoritma
    while True:
        print("Da li zelite da koristite podrazumevane vrednosti za parametre algoritma?")
        print("1. Da")
        print("2. Ne")
        print("3. Izlaz iz programa")

        choice = input("Unesite broj opcije: ")
        if choice == "1":
            population_size = CONST_POPULATION_SIZE
            generations = CONST_GENERATIONS
            same_stoppage = CONST_SAME_STOPPAGE
            mutation_rate = CONST_MUTATION_RATE
            percent_of_protection = CONST_PERCENT_OF_PROTECTION
            percent_of_keep = CONST_PERCENT_OF_KEEP
            max_repeat = CONST_MAX_REPEAT
            percent_of_reset = CONST_PERCENT_OF_RESET
            break
        elif choice == "2":
            try:
                population_size = int(input("Unesite velicinu populacije (preporuceno 250): "))
                generations = int(input("Unesite broj generacija (preporuceno 1000): "))
                same_stoppage = int(input("Unesite broj generacija posle kojih se algoritam prekida ako se ne menjaju dovoljno (preporuceno 450): "))
                mutation_rate = float(input("Unesite stopu mutacije (preporuceno 0.55): "))
                percent_of_protection = float(input("Unesite procenat najboljih jedinki koje ce biti zasticene od mutacije (preporuceno 0.05): "))
                percent_of_keep = float(input("Unesite procenat najboljih jedinki stare populacije koji ce ostati (preporuceno 0.1): "))
                max_repeat = int(input("Unesite broj ponavljanja najbolje jedinke pre vecinskog resetovanja populacije (preporuceno 5): "))
                percent_of_reset = float(input("Unesite procenat populacije za reset (preporuceno 0.95): "))
            except ValueError:
                print("Neispravan unos, koristimo podrazumevane vrednosti.")
                population_size = CONST_POPULATION_SIZE
                generations = CONST_GENERATIONS
                same_stoppage = CONST_SAME_STOPPAGE
                mutation_rate = CONST_MUTATION_RATE
                percent_of_protection = CONST_PERCENT_OF_PROTECTION
                percent_of_keep = CONST_PERCENT_OF_KEEP
                max_repeat = CONST_MAX_REPEAT
                percent_of_reset = CONST_PERCENT_OF_RESET
            break
        elif choice == "3":
            print("Izlaz iz programa...")
            exit(0)
        else:
            print("Nepoznata opcija, molimo unesite ponovo.")

    result = None
    parallel_results = []
    print("Molim vas, sacekajte dok se algoritam izvrsava...")
    if not multiple_instances:
        result=GeneticAlgorithm.genetic_algorithm(population_size, generations, same_stoppage, mutation_rate, cities, percent_of_protection, percent_of_keep, max_repeat, percent_of_reset)
    else:
        with mp.Pool(processes=number_of_instances) as pool:
            results = [pool.apply_async(GeneticAlgorithm.genetic_algorithm, (population_size, generations, same_stoppage, mutation_rate, cities, percent_of_protection, percent_of_keep, max_repeat, percent_of_reset)) for _ in range(number_of_instances)]
            for async_individual in results:
                parallel_results.append(async_individual.get().distance)
            result = min(results, key=lambda async_individual: async_individual.get().distance).get()

    while True:
        print("Koji tip interfejsa zelite da koristite za prikaz rezultata?")
        print("1. Tekstualni interfejs")
        print("2. Graficki interfejs")
        print("3. Izlaz iz programa")

        choice = input("Unesite broj opcije: ")
        use_gui = False
        if choice == "1":
            if multiple_instances:
                print("Rezultati svih instanci:")
                for i, distance in enumerate(parallel_results):
                    print(f"Instanca {i + 1}: Udaljenost = {distance}")

            print("Najbolja jedinka:")
            print("Udaljenost:", result.distance)
            print("Putanja:", [city.name for city in result.genes])

            print("Zavrseno, hvala na koriscenju programa!")
            exit(0)
            break
        elif choice == "2":
            use_gui = True
            break
        elif choice == "3":
            print("Izlaz iz programa...")
            exit(0)
        else:
            print("Nepoznata opcija, molimo unesite ponovo.")
    
    if use_gui:
        while True:
            print("Unesite tip interakcije sa grafickim interfejsom:")
            print("1. Interaktivno (igra protiv programa)")
            print("2. Samo prikaz rezultata")
            print("3. Izlaz iz programa")

            choice = input("Unesite broj opcije: ")
            if choice == "1":
                #ovde bi trebalo da se pokrene GUI koji omogucava interakciju sa korisnikom
                pass
            elif choice == "2":
                # ovde bi trebalo da se pokrene GUI koji samo prikazuje rezultate
                pass
            elif choice == "3":
                print("Izlaz iz programa...")
                exit(0)
            else:
                print("Nepoznata opcija, molimo unesite ponovo.")