# this script receives a temporal knapsack instance such as U2
# and generates a new (.sol ??? ou txt mesmo???) file containing a solution for the instance
# usage example:
# python genetic.py tkp_instances/U2 123seedLok4

import sys
import random
import numpy as np
import math

#metaparametros do aloritmo genetico
POPULATION_SIZE = 100
NUM_GERACOES = 100 # nao sei se isso pode #TODO
PROB_MUTACAO = 0.25 # probabilidade de uma nova solucao sofrer mutacao
TAXA_MUTACAO = 0.5 # porcentagem de genes q sao alterados por uma mutacao
PROB_INITIAL_SOLUTION = 0.01 # probabilidade de cada gene ser ==1 em uma solucao inicial
#PROB_INITIAL_SOLUTION podia ser +-  ==10/numItems
STABLE_ITERS_STOP =  10 # numero maximo de iteracoes sem mudar a melhor solucao


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

def choseWithProb( oneProb ):
    zeroProb = 1 - oneProb
    result = np.random.choice([0,1], 1, p= [zeroProb, oneProb ])[0]
    return result

def generateInitialPopulation(numItems, seed):
    # generates initial population based on the seed
    #TODO
    #refazer: ta totalmente aleatorio por enquanto, nao precisa ser

    #solution[i] == 1 se o itemList[i] ta na mochila
    solution = [ 0 for i in range(numItems)]
    population = []
    for i in range(POPULATION_SIZE):
        #generates a random solution
        solution = [choseWithProb(PROB_INITIAL_SOLUTION) for j in range(numItems)]
        #prob = (2/math.sqrt(numItems)) / (1 + 2/math.sqrt(numItems))
        #solution = [choseWithProb(prob) for j in range(numItems)] # versao alternativa
        population.append(list(solution))

    return population

def getPopulationProbabilities(populationValues): #original version
    # generates probabilites (summing 1) for picking each solution
    # based on the solution values
    populationProbabilities = [0 for i in range(POPULATION_SIZE)]

    sumExps = 0
    for i in range(POPULATION_SIZE):
        sumExps += np.exp(populationValues[i])

    for i in range(POPULATION_SIZE):
        populationProbabilities[i] = np.exp(populationValues[i])/ sumExps

    return populationProbabilities

def getSquaredPopulationProbabilities(populationValues): #alternative version
    # generates probabilites (summing 1) for picking each solution
    # based on the solution values SQUARED
    populationProbabilities = [0 for i in range(POPULATION_SIZE)]

    sumExps = 0
    for i in range(POPULATION_SIZE):
        valueSquared = (populationValues[i])*(populationValues[i])/100
        sumExps += np.exp(valueSquared)

    for i in range(POPULATION_SIZE):
        valueSquared = (populationValues[i])*(populationValues[i])/100
        populationProbabilities[i] = np.exp(valueSquared)/ sumExps

    return populationProbabilities

def generateNewSolution(population, populationValues, itemList, numItems):
    populationProbabilities = getPopulationProbabilities(populationValues)
    #populationProbabilities = getSquaredPopulationProbabilities(populationValues) #alternative version
    index1, index2 = np.random.choice(POPULATION_SIZE, 2, p=populationProbabilities)
    #print "index1: " + str(index1) + "  index2: " + str(index2) #debug
    newSolution = [0 for i in range(numItems)]
    for i in range(numItems):
        if choseWithProb(0.5):
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
        if(choseWithProb(PROB_MUTACAO)):
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
            populationValues[i] = int(getSolutionValue(population[i], itemList, numItems))
    return populationValues

def printPopulationAndValues(population, populationValues):
    print "...printing population and its values...\n"
    for i in range(POPULATION_SIZE):
        print "solucao: " + str(population[i]) +" valor: " +str(populationValues[i])

def printPopulationValues( populationValues):
    print "...printing population values...\n"
    print str(populationValues)

def endLoopCondition(populationValues, stableSolutionCounter, currentBestSolutionValue):
    # returns stableSolutionCounter, currentBestSolutionValue, and the endLoop
    bestSolution, bestSolutionValue = getBestSolution(population, populationValues)
    if (currentBestSolutionValue == bestSolutionValue):
        stableSolutionCounter += 1
    elif(currentBestSolutionValue > bestSolutionValue):
        print "\n-\n-\nERRO: algo ta errado, a melhor solucao piorou\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-"
        print "current: " +str(currentBestSolutionValue) + "\nnova: " +str(bestSolutionValue) +"\n"
    else: # currentBestSolution < bestSolution
        currentBestSolutionValue = bestSolutionValue
        stableSolutionCounter = 0
    #print  "debug " +str(stableSolutionCounter) + ", " +str(currentBestSolution) #debug
    if (stableSolutionCounter >= STABLE_ITERS_STOP):
        return stableSolutionCounter, currentBestSolutionValue, 1
    else:
        return stableSolutionCounter, currentBestSolutionValue, 0



############
### main ###
############
if (len(sys.argv) < 3 or len(sys.argv) > 3):
    print "\nERRO: numero invalido de argumentos\n"
    print "'python genetic.py inputFile seed'\n\n"
    sys.exit(1)

seed = sys.argv[2]
random.seed(a=hash(seed))
np.random.seed(hash(seed))

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
stableSolutionCounter = 0 # number of iterations in which the currentBestSolution didnt change
currentBestSolutionValue = -1

for i in range(NUM_GERACOES):
    #avalia a populacao de solucoes
    populationValues = evaluatePopulation(population, itemList, capacity, numItems)

    stableSolutionCounter, currentBestSolutionValue, endLoop =  endLoopCondition(populationValues, stableSolutionCounter, currentBestSolutionValue)
    if (endLoop):
        print "\nendLoopCondition atingida: " +str(STABLE_ITERS_STOP) +" iteracoes sem mudancas na melhor solucao"
        print "(geracao " +str(i) +")"
        break;

    if i==0 or i == int(NUM_GERACOES*2/3): #debug
        print "\n\n-> geracao " + str(i)
        #printPopulationAndValues(population, populationValues)
        printPopulationValues( populationValues)

    #gera nova populacao de solucoes
    population = generateNewPopulation(population, populationValues, itemList, numItems)


populationValues = evaluatePopulation(population, itemList, capacity, numItems)

print "\n\n --- populacao final ---\n"
#printPopulationAndValues(population, populationValues)
printPopulationValues( populationValues)
print "\n --- melhor solucao encontrada ---"
bestSolution, bestSolutionValue = getBestSolution(population, populationValues)
print str(bestSolution) + "\nvalor: " + str(bestSolutionValue)
