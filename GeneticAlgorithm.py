import Individual
import random

#klasa za rangiranu jedinku(koristi se za selekciju roditelja)
class RankedIndividual:
    def __init__(self, individual,rank):
        self.individual = individual
        self.rank = rank
        self.rand = 0
        self.value=0

    #funkcija koja racuna vrednost jedinke na osnovu ranga i slucajnog broja
    def calculate_value(self,rand):
        self.rand = rand
        self.value = rand*self.rank

#funkcija koja pravi pocetnu populaciju nasumicno generisanih jedinki
def make_initial_population(population_size,cities):
    population=[]
    for _ in range(population_size):
        random_cities=cities.copy()
        random.shuffle(random_cities)
        individual=Individual.Individual(random_cities)
        population.append(individual)
    return population

#funkcija koja pravi decu od roditelja koristeci crossover
def crossover(parent1, parent2):
    crossover_point= random.randint(1, len(parent1.genes) - 1)

    child1_genes= parent1.genes[:crossover_point]
    for gene in parent2.genes:
        if gene not in child1_genes:
            child1_genes.append(gene)
    child1 = Individual.Individual(child1_genes)

    child2_genes= parent2.genes[:crossover_point]
    for gene in parent1.genes:
        if gene not in child2_genes:
            child2_genes.append(gene)
    child2 = Individual.Individual(child2_genes)

    return child1, child2

#funkcija koja mutira dete tako da zameni dva grada
def mutate_child(child):
    index1 = random.randint(0, len(child.genes) - 1)
    index2 = random.randint(0, len(child.genes) - 1)
    while index1 == index2:
        index2 = random.randint(0, len(child.genes) - 1)

    child.genes[index1], child.genes[index2] = child.genes[index2], child.genes[index1]
    
    child.distance = child.calculate_full_distance()

#glavna funkcija koja implementira genetski algoritam
def genetic_algorithm(population_size, generations,same_stoppage, mutation_rate, cities, percent_of_protection, percent_of_keep,max_repeat, percent_of_reset):
    #pravimo pocetnu populaciju
    population=make_initial_population(population_size,cities)
    
    #prolazimo kroz sve generacije
    repeat_count = 0
    stoppage_count = 0
    last_value=0
    for generation in range(generations):
        # smanjujemo stopu mutacije sa svakom generacijom
        #mutation_rate = mutation_rate * (1 - generation / generations)

        #sortiramo populaciju po kvalitetu (udaljenosti)
        population.sort(key=lambda individual: individual.distance, reverse=True)
        #print(f"Generation {generation + 1}: Best distance = {population[-1].distance}")

        #ako dete upada u bar top procent populacije, ne mutiramo ga
        min_for_protection = population[-int(population_size * percent_of_protection)].distance

        #pravimo rangiranu populaciju
        ranked_population = []
        for i in range(len(population)):
            rank = i + 1
            ranked_population.append(RankedIndividual(population[i], rank))

        #izvršavamo selekciju roditelja i pravimo novu generaciju
        new_generation = []
        for i in range(int(population_size/2)):
            #računamo vrednost za svaku rangiranu jedinku(ubacujemo nasumicnost u rangiranje)
            for ranked_individual in ranked_population:
                ranked_individual.calculate_value(random.random())

            #sortiramo rangiranu populaciju po vrednosti
            ranked_population.sort(key=lambda ranked_individual: ranked_individual.value, reverse=True)

            #biramo roditelje
            parent1 = ranked_population[0].individual
            parent2 = ranked_population[1].individual

            #pravimo decu od roditelja
            child1, child2 = crossover(parent1, parent2)

            #mutiramo decu
            if child1.distance>min_for_protection:
                if random.random() < mutation_rate:
                    mutate_child(child1)
            if child2.distance>min_for_protection:
                if random.random() < mutation_rate:
                    mutate_child(child2)

            #dodajemo decu u novu generaciju
            new_generation.append(child1)
            new_generation.append(child2)

        #biramo koga izbacujemo iz populacije, cuvamo n najboljih jedinki iz stare generacije i popunjavamo sa novom generacijom
        number_of_keep = int(population_size * percent_of_keep)
        new_generation.sort(key=lambda individual: individual.distance)

        new_best=0
        if new_generation[0].distance < population[-1].distance:
            new_best = new_generation[0].distance
        else:
            new_best = population[-1].distance

        population = population[population_size - number_of_keep:] + new_generation[:population_size - number_of_keep]

        #proveravamo da li je algoritam konvergirao
        if new_best == last_value:
            repeat_count += 1
            stoppage_count += 1
        else:
            repeat_count = 0
            stoppage_count = 0
            last_value = new_best

        #ako se algoritam previse ponavlja i sa resetom populacije ne moze da se pomeri, prekidamo ga
        if stoppage_count >= same_stoppage:
            #print(f"Stopping algorithm at generation {generation + 1} due to stagnation.")
            break

        #ako se algoritam ponavlja, resetujemo deo populacije
        if repeat_count >= max_repeat:
            #print(f"Resetting population at generation {generation + 1}")
            new_population = make_initial_population(int(population_size * percent_of_reset), cities)
            population.sort(key=lambda individual: individual.distance)
            population = population[:population_size - int(population_size * percent_of_reset)] + new_population
            repeat_count = 0

    #sortiramo poslednju populaciju po kvalitetu (udaljenosti) i vracamo najbolju jedinku
    population.sort(key=lambda individual: individual.distance)
    return population[0]
