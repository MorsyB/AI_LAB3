from random import randint

popsize = 2048


def init_sol(size, problem):  # TSP: nearest neighbor heuristic
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

    def init_population(self):
        for i in range(popsize):
            randStr1 = init_sol(self.args.SIZE, self.CVRP)
            randStr2 = init_sol(self.args.SIZE, self.CVRP)

            member1 = GAstruct(randStr1, 0)
            member2 = GAstruct(randStr2, 0)
            self.population.append(member1)
            self.nextPopulation.append(member2)

    def calc_fitness(self):
        for i in range(popsize):
            fitness, path = self.CVRP.calcPathCost(self.population[i].str)
            self.population[i].fitness = fitness
