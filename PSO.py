from random import randint, random
import time

import numpy

MIN_ASCII = 32
MAX_ASCII = 122
popsize=2048
elite_rate = 0.1
mutation = random() * 0.25
maxIter = 500


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

class GAStruct:
    def __init__(self, string, fitness):
        self.str = string
        self.fitness = fitness
        self.selfBest = []
        self.velocity = []
        self.personalbestfittnes=-1
        self.score = 0
        self.age = 0

    def get_str(self):
        return self.str

    def get_fitness(self):
        return self.fitness

    def set_str(self, string):
        self.str = string

    def set_fitness(self, fitness):
        self.fitness = fitness

    def __gt__(self, other):
        return self.getFitness() >= other.getFitness()

    def __lt__(self, other):
        return self.getFitness() < other.getFitness()

class PSO:

    def __init__(self, CVRP):
        self.population = []
        self.buffer = []
        self.init_population()
        self.CVRP = CVRP
        self.W=1
        self.C1=1
        self.C2=3


    def init_population(self):
        for i in range(popsize):
            randStr1 = init_sol(self.CVRP)
            randStr2 = init_sol(self.CVRP)
            member1 = GAStruct(randStr1, 0)
            member2 = GAStruct(randStr2, 0)
            self.population.append(member1)
            self.buffer.append(member2)




    def calc_fitness(self):
        for i in range(popsize):
            fitness, path = self.CVRP.calcPathCost(self.population[i].str)
            fitness2, path2 = self.CVRP.calcPathCost(self.buffer[i].str)
            arr = self.population[i].str
            arr2 = self.buffer[i].str

            for j in range(len(arr)):
                if j + 1 not in arr:
                    fitness += 1000
            for j in range(len(arr)):
                if j + 1 not in arr2:
                    fitness2 += 1000
            self.population[i].fitness = fitness
            self.buffer[i].fitness = fitness2

    def fitness_sort(self, x):
        return x.get_fitness()

    def sort_by_fitness(self):
        self.population.sort(key=self.fitness_sort)

    def update_parameters(self, t, N):   # update the PSO parameters

        self.W = 0.5
        self.C1 = -3 * (t / N) + 3.5
        self.C2 = 3 * (t / N) + 0.5

    def print_best(self,global_best,fit):
        print("Best: ",global_best, " (", fit, ")")


    def run(self):
        self.calc_fitness()
        self.sort_by_fitness()
        myfitness=self.population[0].fitness
        global_best=self.population[0].str
        start = time.time()
        for index in range(int(self.GA_MAXITER)):

            self.update_parameters(index, self.GA_MAXITER)
            self.calc_fitness()
            self.sort_by_fitness()
            self.print_best(global_best,myfitness)
            if self.population[0].fitness<myfitness:
               global_best=self.population[0].str
               myfitness=self.population[0].fitness
            if myfitness==0:
                print("Best: ",global_best,"(",myfitness,")")
                end = time.time()
                print("Time elapsed :", end - start)
                break
            for j in range(self.GA_POPSIZE):
                #in this loop we walk over all the parcials
                #we have POPSIZE parcials in our implementation
                string1= ""
                string2= ""
                rand1 = random()
                rand2 = random()
                for k in range(len(self.GA_TARGET)):
                    #here we calculate the new string for each parcial
                    #and update the velocity and position of it
                    #using the formulas we saw in the lecture
                    num1 = rand1 * self.C1 * (ord(self.population[j].selfBest[k]) - ord(self.population[j].str[k]))
                    num2 = rand2 * self.C2 * (ord(global_best[k]) - ord(self.population[j].str[k]))
                    num3= self.W *(ord(self.population[j].velocity[k]))
                    num4=num1+num2+num3
                    string1+= chr(int(num4)%95+32)
                    num5=ord(string1[k])+ord(self.population[j].str[k])
                    string2+=chr(int(num5%95+32))

                self.population[j].velocity=string1
                self.population[j].str=string2

            if myfitness == 0:

                break
