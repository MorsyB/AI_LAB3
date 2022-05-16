from random import random
import math


elite_rate = 0.1
mutation = random() * 0.25
maxIter = 2500

class Ackleystruct:
    def __init__(self,myarr):
      self.fitness=-1
      self.array=myarr

class Ackley:

    def __init__(self,popsize):
        self.population = []
        self.buffer=[]
        self.popsize=popsize
        self.init_population()

    def init_population(self):
        for i in range(self.popsize):
            myarr=[]
            for j in range(10):
                myrandomint=random.uniform(-32768, 32768)
                myarr.append(myrandomint)
            member=Ackleystruct(myarr)
            self.population.append(member)
            self.buffer.append(member)

    def calc_fitness(self):
        for i in range(self.popsize):
            self.population[i].fitness=self.calc_Ackley_value(self.population[i].array)

    def calc_Ackley_value(self,array):

        number1=-20*math.exp(-0.2*math.sqrt(1/10*self.segma(array)))
        number2=-math.exp(1/10*self.segma2(array))+20+math.exp(1)
        return number1+number2


    def segma(self,array):
        sum=0
        for i in range(10):
            sum+=(array[i]*array[i])
        return sum
    def segma2(self,array):
        sum=0
        for i in range(10):
            sum+= math.cos(array[i]*math.pi)
        return sum

    def sort_by_fitness(self):
        self.population.sort(key=self.fitness_sort)

    def fitness_sort(self, x):
        return x.fitness

    def mate(self):
        esize = self.popsize * elite_rate
        for i in range(int(esize), self.popsize):
            i1 = random.randint(0, self.popsize / 2)
            i2 = random.randint(0, self.popsize / 2)
            spos = random.randint(0, 10 - 1)
            self.buffer[i].str = self.population[i1].str[0:spos] + self.population[i2].str[spos:]
            if random() < mutation:
                self.mutate(i)
        self.swap()

    def swap(self):
        temp = self.population
        self.population = self.buffer
        self.buffer = temp

    def mutate(self, i):
        i1 = random.randint(0, self.CVRP.size - 1)
        i2 = random.randint(0, self.CVRP.size - 1)
        tmp = self.buffer[i].str[i1]
        self.buffer[i].str[i1] = self.buffer[i].str[i2]
        self.buffer[i].str[i2] = tmp

    def print_best(self):
        print("array = ", self.population[0].array)
        print('fitness = ', self.population[0].fitness)
        print()

    def run(self):
        for i in range(maxIter):
            self.calc_fitness()
            self.sort_by_fitness()
            self.print_best()
            self.mate()
