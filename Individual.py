import math

#klasa za jedinku(jedan put oko svih gradova)
class Individual:
    def __init__(self,genes):
        self.genes=genes
        self.distance=self.calculate_full_distance()

    #funkcija koja racuna ukupnu udaljenost oko svih gradova
    def calculate_full_distance(self):
        distance = 0
        for i in range(len(self.genes)-1):
            distance += self.calculate_one_distance(self.genes[i], self.genes[i+1])
        distance += self.calculate_one_distance(self.genes[-1], self.genes[0])
        return distance

    #funkcija koja racuna udaljenost izmedju dva grada
    def calculate_one_distance(self,city1,city2):
        return math.sqrt((city1.x - city2.x) ** 2 + (city1.y - city2.y) ** 2)
    