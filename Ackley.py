from random import random
from random import randint

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
                mynum=randint(-32768, 32768)
                myarr.append(mynum)

            myarr[randint(0,9)] = 0
            myarr[randint(0, 9)] = 0
            myarr[randint(0, 9)] = 0
            member=Ackleystruct(myarr)
            self.population.append(member)
            self.buffer.append(member)

    def calc_fitness(self):
        for i in range(self.popsize):
            self.population[i].fitness=self.calc_Ackley_value(self.population[i].array)
            self.buffer[i].fitness = self.calc_Ackley_value(self.buffer[i].array)


    def calc_Ackley_value(self,array):

        number1=-20*math.exp(-0.2*math.sqrt((1/10)*self.segma(array)))
        number2=-math.exp((1/10)*self.segma2(array))+20+math.exp(1)
        #print(math.exp(1))
        #print(number1,number2)
        return number1+number2



    def segma(self,array):
        sum=0
        for i in range(10):
            sum+=(array[i]*array[i])
            #print(sum)
        return sum
    def segma2(self,array):
        sum=0
        for i in range(10):
            sum+= math.cos(array[i]*math.pi*2)
        return sum

    def sort_by_fitness(self):
        self.population.sort(key=self.fitness_sort)

    def fitness_sort(self, x):
        return x.fitness

    def mate(self):
        esize = self.popsize * elite_rate
        for i in range(0, self.popsize):
            i1 = randint(0, self.popsize / 2)
            i2 = randint(0, self.popsize / 2)
            spos = randint(0, 9 - 1)
            self.buffer[i].array = self.population[i1].array[0:spos] + self.population[i2].array[spos:]
            if random() < mutation:
                self.mutate(i)
        self.swap()

    def swap(self):
        temp = self.population
        self.population = self.buffer
        self.buffer = temp

    def mutate(self, i):
        i1 = randint(0, 9 )
        i2 = randint(0, 9 )
        tmp = self.buffer[i].array[i1]
        self.buffer[i].array[i1] = self.buffer[i].array[i2]
        self.buffer[i].array[i2] = tmp

    def print_best(self):
        print("array = ", self.population[0].array)
        print('fitness = ', self.population[0].fitness)
        print()

    def run(self):
        myglobalmin=10000
        myglobalminarr=[]
        for i in range(maxIter):
            self.calc_fitness()
            self.sort_by_fitness()
            if self.population[0].fitness<myglobalmin:
                myglobalmin=self.population[0].fitness
                myglobalminarr=self.population[0].array

            if myglobalmin==0:
                break
            self.print_best()
            self.mate()
            #print("global min is :",myglobalmin)

        print("global min is :", myglobalmin)
        print("global min array is :", myglobalminarr)