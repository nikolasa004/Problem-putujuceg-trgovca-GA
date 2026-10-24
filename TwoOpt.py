import Individual

def two_opt(individual):
    path = individual.genes.copy()
    improved = True
    while improved:
        improved = False
        for i in range(len(path) - 1):
            for j in range(i + 2, len(path)):
                if i == 0 and j == len(path) - 1:
                    continue
                a, b, c, d = path[i], path[i + 1], path[j], path[(j + 1) % len(path)]
                old_distance = individual.calculate_one_distance(a, b) + individual.calculate_one_distance(c, d)
                new_distance = individual.calculate_one_distance(a, c) + individual.calculate_one_distance(b, d)
                if new_distance + 1e-9 < old_distance:
                    path[i + 1:j + 1] = reversed(path[i + 1:j + 1])
                    improved = True
                    break
            if improved:
                break
    return Individual.Individual(path)
