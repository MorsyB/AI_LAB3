import time
from random import randint
import math
import Graph


def initGreedySol(size, problem):   # TSP: nearest neighbor heuristic
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

def tabuSearch(problem, args):
    startTime = time.time()
    points = []
    best = initGreedySol(problem.size, problem)
    bestFitness, mypath = problem.calcPathCost(best)
    bestCandidate = best
    globalBest = best
    globalFitness = bestFitness
    tabuDict = {str(best): True}
    tabu = [best]
    local_counter = 0
    for _ in range(args.maxIter):
        iterTime = time.time()
        neighborhood = getNeighborhood(bestCandidate, args.numNeighbors)    # get neighborhood of current solution
        minimum, _ = problem.calcPathCost(neighborhood[0])
        bestCandidate = neighborhood[0]
        for neighbor in neighborhood:   # get the best neighbor and save it
            cost, _ = problem.calcPathCost(neighbor)
            if cost < minimum and not tabuDict.get(str(neighbor), False):
                minimum = cost
                bestCandidate = neighbor
        if minimum < bestFitness:   # update best (take a step towards the better neighbor)
            bestFitness = minimum
            best = bestCandidate
            local_counter = 0
        elif minimum == bestFitness:    # to detect local optimum
            local_counter += 1
        if bestFitness < globalFitness: # update the best solution found untill now
            globalBest = best
            globalFitness = bestFitness
        tabu.append(bestCandidate)
        tabuDict[str(bestCandidate)] = True
        if len(tabu) > args.maxTabu:
            tabuDict[str(tabu[0])] = False
            tabu.pop(0)
        if local_counter == args.localOptStop:  # if fallen into local optimum, reset and continue with the algorithm
            if bestFitness < globalFitness:
                globalBest = best
                globalFitness = bestFitness
            bestCandidate = initGreedySol(problem.size, problem)
            best = bestCandidate
            bestFitness, _ = problem.calcPathCost(best)
            local_counter = 0
            tabuDict = {str(bestCandidate): True}
        points.append(globalFitness)
        print('Generation time: ', time.time() - iterTime)
        print('sol = ', best)
        print('cost = ', bestFitness)
        print()
    print('Time elapsed: ', time.time() - startTime)
    problem.best = globalBest   # save the solution and its fitness
    Graph.draw(points)
    problem.bestFitness = globalFitness


def init_ackeley():
    myarr = []
    for j in range(10):
        mynum = randint(-32768, 32768)
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

def tabuSearchAckley(args):
    startTime = time.time()
    points = []
    best = init_ackeley()
    bestFitness=calc_Ackley_value(best)
    bestCandidate = best
    globalBest = best
    globalFitness = bestFitness
    tabuDict = {str(best): True}
    tabu = [best]
    local_counter = 0
    for _ in range(args.maxIter):
        iterTime = time.time()
        neighborhood = getNeighborhood(bestCandidate, args.numNeighbors)  # get neighborhood of current solution
        minimum= calc_Ackley_value(neighborhood[0])
        bestCandidate = neighborhood[0]
        for neighbor in neighborhood:  # get the best neighbor and save it
            cost  = calc_Ackley_value(neighbor)
            if cost < minimum and not tabuDict.get(str(neighbor), False):
                minimum = cost
                bestCandidate = neighbor
        if minimum < bestFitness:  # update best (take a step towards the better neighbor)
            bestFitness = minimum
            best = bestCandidate
            local_counter = 0
        elif minimum == bestFitness:  # to detect local optimum
            local_counter += 1
        if bestFitness < globalFitness:  # update the best solution found untill now
            globalBest = best
            globalFitness = bestFitness
        tabu.append(bestCandidate)
        tabuDict[str(bestCandidate)] = True
        if len(tabu) > args.maxTabu:
            tabuDict[str(tabu[0])] = False
            tabu.pop(0)
        if local_counter == args.localOptStop:  # if fallen into local optimum, reset and continue with the algorithm
            if bestFitness < globalFitness:
                globalBest = best
                globalFitness = bestFitness
            bestCandidate = init_ackeley()
            best = bestCandidate
            bestFitness=calc_Ackley_value(best)
            local_counter = 0
            tabuDict = {str(bestCandidate): True}
        points.append(globalFitness)
        print('Generation time: ', time.time() - iterTime)
        print('sol = ', best)
        print('cost = ', bestFitness)
        print()
    print('Time elapsed: ', time.time() - startTime)
    print("final sol",globalBest)  # save the solution and its fitness
    print("final fit",globalFitness)