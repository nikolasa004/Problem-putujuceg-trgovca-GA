import City
import GeneticAlgorithm

#main funkcija koja se izvrsava kada se pokrene skripta
if __name__ == "__main__":
    cities=City.read_cities()
    result=GeneticAlgorithm.genetic_algorithm(population_size=1000, generations=20, mutation_rate=0.55, cities=cities, procent_of_protection=0.1, procent_of_keep=0.1)

    print("Najbolja jedinka:")
    print("Udaljenost:", result.distance)
    print("Putanja:", [city.name for city in result.genes])