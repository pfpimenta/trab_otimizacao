# this script receives a temporal knapsack instance such as U2
# and generates a new (.sol ??? ou txt mesmo???) file containing a solution for the instance
# usage example:
# python genetic.py tkp_instances/U2 123seedLok4

import sys
import random
import numpy as np

#metaparametros do aloritmo genetico
POPULATION_SIZE = 100
NUM_GERACOES = 50 # nao sei se isso pode #TODO
PROB_MUTACAO = 0.25 # probabilidade de uma nova solucao sofrer mutacao
TAXA_MUTACAO = 0.5 # porcentagem de genes q sao alterados por uma mutacao


def getItemList( inp ):
    #receives the input instance without the first 2 lines
    #retorns a list of all the items
    item = { 'value': 0, 'weight': 0, 'startTime': 0, 'endTime': 0}
    itemList = []
    for line in inp:
        lineWords = line.split(" ")
        item['value'] = int(lineWords[0])
        item['weight'] = int(lineWords[1])
        item['startTime'] = int(lineWords[2])
        item['endTime'] = int(lineWords[3])
        itemList.append(item.copy())

    return itemList

def generateInitialPopulation(numItems, seed):
    # generates initial population based on the seed
    #TODO
    #refazer: ta totalmente aleatorio por enquanto, nao precisa ser
    random.seed(a=hash(seed))

    #solution[i] == 1 se o itemList[i] ta na mochila
    solution = [ 0 for i in range(numItems)]
    population = []
    for i in range(POPULATION_SIZE):
        solution = [random.randint(0, 1) for j in range(numItems)]
        population.append(list(solution))

    return population

def getPopulationProbabilities(populationValues):
    # generates probabilites (summing 1) for picking each solution
    # based on the solution values
    populationProbabilities = [0 for i in range(POPULATION_SIZE)]

    sumExps = 0
    for i in range(POPULATION_SIZE):
        sumExps += np.exp(populationValues[i])

    for i in range(POPULATION_SIZE):
        populationProbabilities[i] = np.exp(populationValues[i])/ sumExps

    return populationProbabilities

def generateNewSolution(population, populationValues, itemList, numItems):
    populationProbabilities = getPopulationProbabilities(populationValues)
    index1, index2 = np.random.choice(POPULATION_SIZE, 2, p=populationProbabilities)
    #print "index1: " + str(index1) + "  index2: " + str(index2) #debug
    newSolution = [0 for i in range(numItems)]
    for i in range(numItems):
        if (i > (numItems/2)):
            newSolution[i] = population[index1][i]
        else:
            newSolution[i] = population[index2][i]

    return newSolution

def getBestSolution(population, populationValues):
    bestSolution = list(population[0])
    bestSolutionValue = -1
    for i in range(POPULATION_SIZE):
        if(populationValues[i] >= bestSolutionValue):
            bestSolutionValue = populationValues[i]
            bestSolution = list(population[i])
    return bestSolution, bestSolutionValue

def mutation(solution, numItems):
    for i in range(int(numItems*TAXA_MUTACAO)):
        randomIndex = random.randint(0,numItems-1)
        solution[randomIndex] = (1 - solution[randomIndex])
    return solution

def generateNewPopulation(population, populationValues, itemList, numItems):
    #TODO
    #sort population by solution values
    #newPopulation = sorted(population, key= lambda solution: getSolutionValue(solution, itemList))
    newPopulation = []
    bestSolution, bestSolutionValue = getBestSolution(population, populationValues)
    newPopulation.append(bestSolution)
    for i in range(POPULATION_SIZE-1):
        newSolution = list(generateNewSolution(population, populationValues, itemList, numItems))
        if(random.random() < PROB_MUTACAO):
            newSolution = mutation(newSolution, numItems)
        newPopulation.append(list(newSolution))
    return newPopulation

def getSolutionTotalWeight(solution, itemList, numItems):
    #get total backpack weight for a solution
    totalWeight = 0
    for i in range(numItems):
        if solution[i]:
            totalWeight += itemList[i]['weight']
    return totalWeight

def getSolutionValue(solution, itemList, numItems):
    #get total backpack value for a solution
    solutionValue = 0
    for i in range(numItems):
        if solution[i]:
            solutionValue += itemList[i]['value']
    return solutionValue


def evaluatePopulation(population, itemList, capacity, numItems):
    populationValues = [0 for i in range(POPULATION_SIZE)]
    for i in range(POPULATION_SIZE):
        totalWeight = getSolutionTotalWeight(population[i], itemList, numItems)
        if (totalWeight > capacity): #solucao invalida, acima da capacidade
            populationValues[i] = -1
        else:
            populationValues[i] = getSolutionValue(population[i], itemList, numItems)
    return populationValues

def printPopulationAndValues(population, populationValues):
    print "...printing population and its values...\n"
    for i in range(POPULATION_SIZE):
        print "solucao: " + str(population[i]) +" valor: " +str(populationValues[i])



############
### main ###
############
if (len(sys.argv) < 3 or len(sys.argv) > 3):
    print "\nERRO: numero invalido de argumentos\n"
    print "'python genetic.py inputFile seed'\n\n"
    sys.exit(1)

seed = sys.argv[2]

inp = open(sys.argv[1], 'rU').read().splitlines()

numItems = int(inp[0])
capacity = int(inp[1])

inp.remove(inp[0])   #  delete those 2 lines we've already used so we're left with the items themselves only
inp.remove(inp[0])

itemList = getItemList(inp)
#print itemList #debug

solution =[ 0 for i in range(numItems+1)] #initialization

population = generateInitialPopulation(numItems,seed)
populationValues = [ 0 for i in range(POPULATION_SIZE)]

for i in range(NUM_GERACOES):
    #avalia a populacao de solucoes
    populationValues = evaluatePopulation(population, itemList, capacity, numItems)

    if False: #i == 0 or True: #debug
        print "\n\n-> geracao " + str(i)
        printPopulationAndValues(population, populationValues)

    #gera nova populacao de solucoes
    population = generateNewPopulation(population, populationValues, itemList, numItems)


populationValues = evaluatePopulation(population, itemList, capacity, numItems)

print "\n\n --- solucao final ---\n"
printPopulationAndValues(population, populationValues)
print "\ --- melhor solucao encontrada ---"
bestSolution, bestSolutionValue = getBestSolution(population, populationValues)
print str(bestSolution) + "\nvalor: " + str(bestSolutionValue)
