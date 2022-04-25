import CVRP
import City
import TabuSearch
from TabuSearch import*
from math import sqrt

class args:
    maxIter=1500
    numNeighbors=2048
    maxTabu=20
    localOptStop=25


def getInput():
    file = open('test1' + '.txt', 'r')  # input string
    for _ in range(3):
        file.readline()

    dimensionLine = file.readline()
    arr = [num for num in dimensionLine.split(' ')]
    dimension = int(arr[2])

    file.readline()

    capacityLine = file.readline()
    arr = [num for num in capacityLine.split(' ')]
    capacity = int(arr[2])

    file.readline()

    cityLine = file.readline()
    arr = [num for num in cityLine.split(' ')]
    depot = City.City(int(arr[0]), int(arr[1]), int(arr[2]))

    cities = []
    for _ in range(dimension - 1):
        cityLine = file.readline()
        arr = [num for num in cityLine.split(' ')]
        city = City.City(int(arr[0]) - 1, int(arr[1]), int(arr[2]))
        cities.append(city)

    file.readline()
    file.readline()

    for i in range(dimension - 1):
        demandLine = file.readline()
        arr = [num for num in demandLine.split(' ')]
        cities[i].setDemand(int(arr[1]))

    cities.insert(0, depot)

    distanceMat = calcDistanceMatrix(cities)
    cities.pop(0)

    problem = CVRP.CVRP(distanceMat, depot, cities, capacity, len(cities))

    return problem


def calcDistanceMatrix(cities):
    array = []
    numOfCities = len(cities)
    for i in range(numOfCities):
        arr = []
        for j in range(numOfCities):
            arr.append(distance(cities[i], cities[j]))
        array.append(arr)
    return array


def distance(city1, city2):
    x = city1.x - city2.x
    dx = x * x

    y = city1.y - city2.y
    dy = y * y

    return sqrt(dx + dy)

if __name__ == '__main__':
    myargs= args()

    problem= getInput()
    TabuSearch.tabuSearch(problem,myargs)
    problem.printSolution()
