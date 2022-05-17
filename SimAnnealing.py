from random import randint
from numpy import exp
from numpy.random import rand
import time

import math

import Graph


def initGreedySol(size, problem):  # TSP: nearest neighbor heuristic
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


def getNeighborhood(bestCandidate, numNeighbors):
    return [mutate(bestCandidate) for _ in range(numNeighbors)]


def mutate(bestCandidate):
    return simpleInversionMutation(bestCandidate)


def exchangeMutation(sol):
    string = sol[:]
    i1 = randint(0, len(sol) - 1)
    i2 = randint(0, len(sol) - 1)
    string[i1], string[i2] = string[i2], string[i1]
    return string


def simpleInversionMutation(sol):
    string = sol[:]
    i1 = randint(0, len(sol) - 1)
    i2 = randint(0, len(sol) - 1)
    if i1 > i2:
        i1, i2 = i2, i1
    while i1 < i2:
        string[i1], string[i2] = string[i2], string[i1]
        i1 += 1
        i2 -= 1
    return string

def init_ackeley():
    myarr = []
    for j in range(10):
        mynum = randint(-32, 32)
        myarr.append(mynum)

    return myarr

def calc_Ackley_value( array):
    number1 = -20 * math.exp(-0.2 * math.sqrt((1 / 10) * segma(array)))
    number2 = -math.exp((1 / 10) * segma2(array)) + 20 + math.exp(1)
    # print(math.exp(1))
    # print(number1,number2)
    return number1 + number2

def segma( array):
    sum = 0
    for i in range(10):
        sum += (array[i] * array[i])
        # print(sum)
    return sum

def segma2( array):
    sum = 0
    for i in range(10):
        sum += math.cos(array[i] * math.pi * 2)
    return sum


def simulatedAnnealing(problem, args):
    startTime = time.time()
    points = []
    best = initGreedySol(problem.size, problem)
    bestFitness, _ = problem.calcPathCost(best)
    globalBest = best
    globalFitness = bestFitness
    currentBest = best
    currentFitness = bestFitness
    temperature = float(args.temperature)
    local_counter = 0
    LK = 30
    for _ in range(args.maxIter):
        iterTime = time.time()
        neighborhood = getNeighborhood(best, args.numNeighbors)
        for _ in range(LK):  # pick 'LK' neighbors and get the best
            randNeighbor = neighborhood[randint(0, len(neighborhood) - 1)]
            neighborFitness, _ = problem.calcPathCost(randNeighbor)
            diff = neighborFitness - bestFitness
            metropolis = float(exp(float(-1 * diff) / temperature))
            if neighborFitness < currentFitness or rand() < metropolis:
                currentFitness = neighborFitness
                currentBest = randNeighbor
        if currentFitness < bestFitness:  # update best (take a step towards the better neighbor)
            best = currentBest
            bestFitness = currentFitness
            local_counter = 0
        if currentFitness == bestFitness:  # to detect local optimum
            local_counter += 1
        if bestFitness < globalFitness:  # update the best solution found untill now
            globalBest = best
            globalFitness = bestFitness
        if local_counter == args.localOptStop:  # if fallen into local optimum, reset and continue with the algorithm
            if bestFitness < globalFitness:
                globalBest = best
                globalFitness = bestFitness
            best = initGreedySol(problem.size, problem)
            bestFitness, _ = problem.calcPathCost(best)
            currentBest = best
            currentFitness = bestFitness
            local_counter = 0
            temperature = float(args.temperature)
        print('Generation time: ', time.time() - iterTime)
        print('sol = ', best)
        print('cost = ', bestFitness)
        print()
        points.append(bestFitness)
        temperature *= args.alpha
    print('Time elapsed: ', time.time() - startTime)
    problem.best = globalBest  # save the solution and its fitness
    problem.bestFitness = globalFitness
    Graph.draw(points)


def simulatedAnnealingAckley(args):
    startTime = time.time()
    points = []
    best = init_ackeley()
    bestFitness= calc_Ackley_value(best)
    globalBest = best
    globalFitness = bestFitness
    currentBest = best
    currentFitness = bestFitness
    temperature = float(args.temperature)
    local_counter = 0
    LK = 30
    for _ in range(args.maxIter):
        iterTime = time.time()
        neighborhood = getNeighborhood(best, args.numNeighbors)
        for _ in range(LK):  # pick 'LK' neighbors and get the best
            randNeighbor = neighborhood[randint(0, len(neighborhood) - 1)]
            neighborFitness = calc_Ackley_value(randNeighbor)
            diff = neighborFitness - bestFitness
            metropolis = float(exp(float(-1 * diff) / temperature))
            if neighborFitness < currentFitness or rand() < metropolis:
                currentFitness = neighborFitness
                currentBest = randNeighbor
        if currentFitness < bestFitness:  # update best (take a step towards the better neighbor)
            best = currentBest
            bestFitness = currentFitness
            local_counter = 0
        if currentFitness == bestFitness:  # to detect local optimum
            local_counter += 1
        if bestFitness < globalFitness:  # update the best solution found untill now
            globalBest = best
            globalFitness = bestFitness
        if local_counter == args.localOptStop:  # if fallen into local optimum, reset and continue with the algorithm
            if bestFitness < globalFitness:
                globalBest = best
                globalFitness = bestFitness
            best = init_ackeley()
            bestFitness=calc_Ackley_value(best)
            currentBest = best
            currentFitness = bestFitness
            local_counter = 0
            temperature = float(args.temperature)
        print('Generation time: ', time.time() - iterTime)
        print('sol = ', best)
        print('cost = ', bestFitness)
        print()
        points.append(bestFitness)
        temperature *= args.alpha
    print('Time elapsed: ', time.time() - startTime)
    print("final sol", globalBest)  # save the solution and its fitness
    print("final fit", globalFitness)
    Graph.draw(points)
