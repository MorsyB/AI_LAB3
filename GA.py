from random import randint, random

popsize = 2048
size = 10
elite_rate = 0.1
mutation = random() * 0.25
maxIter = 150


def init_sol(problem):  # TSP: nearest neighbor heuristic
    size = problem.size
    array = []
    city = randint(1, size)
    array.append(city)
    dictionary = {city: True}
    index = size
    index -= 1
    while index > 0:
        distanceArray = problem.distanceMatrix[city]
        minCity = 1
        minDistance = float('inf')
        for i in range(1, len(distanceArray)):
            distance = distanceArray[i]
            if 0 < distance < minDistance and not dictionary.get(i, False):
                minDistance = distance
                minCity = i
        array.append(minCity)
        dictionary[minCity] = True
        city = minCity
        index -= 1
    return array


class GAstruct:
    def __init__(self, string, fitness):
        self.str = string
        self.fitness = fitness


class GA:
    def __init__(self, CVRP):
        self.population = []
        self.buffer = []
        self.CVRP = CVRP
        self.init_population()

    def init_population(self):
        for i in range(popsize):
            randStr1 = init_sol(self.CVRP)
            randStr2 = init_sol(self.CVRP)

            member1 = GAstruct(randStr1, 0)
            member2 = GAstruct(randStr2, 0)
            self.population.append(member1)
            self.buffer.append(member2)

    def sort_by_fitness(self):
        self.population.sort(key=self.fitness_sort)

    def fitness_sort(self, x):
        return x.fitness

    def calc_fitness(self):
        for i in range(popsize):
            fitness, path = self.CVRP.calcPathCost(self.population[i].str)
            fitness2, path2 = self.CVRP.calcPathCost(self.buffer[i].str)
            arr = self.population[i].str
            arr2 = self.buffer[i].str

            for j in range(len(arr)):
                if j + 1 not in arr:
                    fitness += 100
            for j in range(len(arr)):
                if j + 1 not in arr2:
                    fitness2 += 100
            self.population[i].fitness = fitness
            self.buffer[i].fitness = fitness2

    def swap(self):
        temp = self.population
        self.population = self.buffer
        self.buffer = temp

    def mate(self):
        esize = popsize * elite_rate
        size = self.CVRP.size
        for i in range(int(esize), popsize):
            i1 = randint(0, popsize / 2)
            i2 = randint(0, popsize / 2)
            spos = randint(0, size - 1)
            self.buffer[i].str = self.population[i1].str[0:spos] + self.population[i2].str[spos:]
            if random() < mutation:
                self.mutate(i)
        self.swap()

    def mutate(self, i):
        i1 = randint(0, self.CVRP.size - 1)
        i2 = randint(0, self.CVRP.size - 1)
        tmp = self.buffer[i].str[i1]
        self.buffer[i].str[i1] = self.buffer[i].str[i2]
        self.buffer[i].str[i2] = tmp

    def print_best(self):
        print("Best: ", self.population[0].str, " (", self.population[0].fitness, ")")

    def run(self):
        for i in range(maxIter):
            print()
            print()
            print(self.population[0].fitness)
            self.calc_fitness()
            print(self.population[0].fitness)
            self.sort_by_fitness()
            print(self.population[0].fitness)
            self.mate()
            print(self.population[0].fitness)
            self.CVRP.best = self.population[0].str
            self.CVRP.bestFitness = self.population[0].fitness
            self.print_best()
            print()
            print()