import random
from collections import Counter
import re
import pickle

def readFile(fileName):
  matrix = pickle.load( open( "pickledMatrix.pkl", "rb" ) )
  return matrix
  # print(favorite_color)
  # lines = open(fileName, "r").readlines()
  # inputData = []
  # for line in lines:
  #   pattern = r'\[.*?\]'
  #   re.sub(pattern, '', line)
  #   temp = line.split(",")
  #   print(temp)
  #   newTemp = []
  #   for item in temp:
  #     newTemp.append(int(item))
  #   inputData.append(newTemp)
  # return inputData


def createRandomPopulation(numberOfCities, populationSize):
  newPopulation = []
  while len(newPopulation) < populationSize:
    valueList = list(range(0, numberOfCities))
    random.shuffle(valueList)
    newPopulation.append(valueList)
  return newPopulation


def costFunction(member, costMatrix):
  costSum = 0
  for i in range(1, len(member)):
    costSum += costMatrix[member[i-1]][member[i]]
  costSum += costMatrix[member[0]][member[len(member)-1]]
  return costSum


def checkConvergence(population, convergenceRate):
  listToString = []
  for member in population:
    listToString.append(''.join(str(member)))
  c = Counter(listToString)
  rate = c.most_common(1)[0][1] / float(len(population))
  return rate >= convergenceRate

def checkConvergenceGetResult(population, convergenceRate):
  listToString = []
  for member in population:
    listToString.append(''.join(str(member)))
  c = Counter(listToString)
  return c.most_common(1)


def assessPopulationFitness(population, costMatrix):
  return [[costFunction(member, costMatrix), member] for member in population]


def fittestPopulation(population, costMatrix):
  fittestPopulation = []
  populationResults = assessPopulationFitness(population, costMatrix)
  for i in range(len(population)):
    randIndex1 = random.randint(0,len(population)-1)
    randIndex2 = random.randint(0,len(population)-1)
    if populationResults[randIndex1][0] < populationResults[randIndex2][0]:
      fittestPopulation.append(populationResults[randIndex1][1]) 
    else: 
      fittestPopulation.append(populationResults[randIndex2][1]) 
  return fittestPopulation


def mutatePopulation(population, mutationRate):
  mutatedPopulation = []
  for i in range(len(population)):
    if random.random() <= mutationRate:
      member = population[i]
      randMutationIndex1 = random.randint(0, len(member)-1)
      randMutationIndex2 = random.randint(0, len(member)-1)
      temp = member[randMutationIndex1]
      member[randMutationIndex1] = member[randMutationIndex2]
      member[randMutationIndex2] = temp
      mutatedPopulation.append(member)
    else:
      mutatedPopulation.append(population[i])
  return mutatedPopulation


def crossoverPopulation(population, crossoverRate):
  newPopulation = []
  for i in range(len(population)):
    if random.random() <= crossoverRate:
      member = population[i]
      mateIndex = random.randint(0, len(population)-1)
      while mateIndex == i:
        mateIndex = random.randint(0, len(population)-1)
      mate = population[mateIndex]
      cut1 = random.randint(0, len(member)-1)
      cut2 = random.randint(0, len(member)-1)
      while (cut2 - cut1) <= 1:
        cut1 = random.randint(0, len(member)-1)
        cut2 = random.randint(0, len(member)-1)
      newMember = []
      for i in range(len(member)):
        newMember.append(-1)
      lookupDict = {}
      for i in range(cut1+1, cut2):
        newMember[i] = mate[i]
        lookupDict[mate[i]] = member[i]
      for i in range(len(member)):
        if i <= cut1 or i >= cut2:
          candidate = member[i]
          while candidate in newMember:
            candidate = lookupDict[candidate]
          newMember[i] = candidate
      newPopulation.append(newMember)
    else:
      newPopulation.append(population[i])
  return newPopulation



def setup(convergenceRate, populationSize, mutationRate, crossoverRate):
  costMatrix = readFile("data.txt")
  numberOfCities = len(costMatrix)
  population = createRandomPopulation(numberOfCities, populationSize)

  iterations = 0
  while checkConvergence(population, convergenceRate) is not True:
    iterations += 1

    bestPopulation = fittestPopulation(population, costMatrix)
    mutatedPopulation = mutatePopulation(bestPopulation, mutationRate)
    bredPopulation = crossoverPopulation(mutatedPopulation, crossoverRate)
    population = bredPopulation
  return iterations, costFunction(population[0], costMatrix), checkConvergenceGetResult(population, convergenceRate)


convergence = 0.95
populationSize = [2000, 5000, 1000]
mutationRates = [0.001]
crossoverRates = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

testList = []
for population in range(populationSize[0], populationSize[1], populationSize[2]):
  for mutation in mutationRates:
    for crossover in crossoverRates:  
      print("Testing:", population, " population size")
      print("Testing:", mutation, " mutation rate")
      print("Testing:", crossover, " crossover rate")
      print("-----")
      iterations, costFunctionResult, convergenceResult = setup(convergence, population, mutation, crossover)
      testList.append([costFunctionResult, iterations, population, mutation, crossover, convergenceResult[0][0]])

testList = sorted(testList, key=lambda x: (x[0], x[1]))
print("\n\n\n------")
print("All Tests:")
for test in testList:
  print(test)



print("\n\n\nBEST - sorted by cost function result then minimum iterations")
print("Cost Function Result:", testList[0][0])
print("Iterations:", testList[0][1])
print("Population:", testList[0][2])
print("Mutation Rate:", testList[0][3])
print("Crossover Rate:", testList[0][4])
print("Convervence Result: ", testList[0][5])

