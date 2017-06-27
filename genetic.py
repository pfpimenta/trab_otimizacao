# this script receives a temporal knapsack instance such as U2
# and generates a new (.sol ??? ou txt mesmo???) file containing a solution for the instance
# usage example:
# python genetic.py tkp_instances/U2 123seedLok4

import sys
import random
import numpy as np
import math
import time

#metaparametros do aloritmo genetico
POPULATION_SIZE = 100
NUM_GERACOES = 100 # nao sei se isso pode #TODO
PROB_MUTACAO = 0.25 # probabilidade de uma nova solucao sofrer mutacao
TAXA_MUTACAO = 0.3 # porcentagem de genes q sao alterados por uma mutacao
PROB_INITIAL_SOLUTION = 0.01 # probabilidade de cada gene ser ==1 em uma solucao inicial
#PROB_INITIAL_SOLUTION podia ser +-  ==10/numItems
STABLE_ITERS_STOP =  10 # numero maximo de iteracoes sem mudar a melhor solucao
# group sizes in %
GROUP_1_SIZE = 20.0
GROUP_2_SIZE = 70.0
GROUP_3_SIZE = 10.0
# group chances in group roulette in probabilities
GROUP_1_PROB = 0.5
GROUP_2_PROB = 0.35
GROUP_3_PROB = 0.15



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

def getRange ():
    min_s = 9999999999999999
    max_s = -100000
    for item in itemList:
        if item['startTime'] < min_s:
            min_s = item['startTime']
        if item['endTime'] > max_s:
            max_s = item['endTime']
    return min_s, max_s

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
        sumExps += np.exp(populationValues[i]/100) # to avoid overflow

    for i in range(POPULATION_SIZE):
        populationProbabilities[i] = np.exp(populationValues[i]/100)/ sumExps

    return populationProbabilities

def getSquaredPopulationProbabilities(populationValues): #alternative version
    # generates probabilites (summing 1) for picking each solution
    # based on the solution values SQUARED
    populationProbabilities = [0 for i in range(POPULATION_SIZE)]

    sumExps = 0
    for i in range(POPULATION_SIZE):
        valueSquared = (populationValues[i]/100)*(populationValues[i]/100)/100
        sumExps += np.exp(valueSquared)

    for i in range(POPULATION_SIZE):
        valueSquared = (populationValues[i]/100)*(populationValues[i]/100)/100
        populationProbabilities[i] = np.exp(valueSquared)/ sumExps

    return populationProbabilities

def crossover(parent1, parent2, numItems):
    newSolution = [0 for i in range(numItems)]
    for i in range(numItems):
        if choseWithProb(0.5):
            newSolution[i] = parent1[i]
        else:
            newSolution[i] = parent1[i]
    return newSolution

def generateNewSolutionRoulette(population, populationValues, itemList, numItems, populationProbabilities):
    index1, index2 = np.random.choice(POPULATION_SIZE, 2, p=populationProbabilities, replace= True)
    #print "index1: " + str(index1) + "  index2: " + str(index2) #debug
    newSolution = crossover(population[index1], population[index2], numItems)
    return newSolution

def fastRoulette():
    #escolhe um indice aleatorio do array (mais chance pros primeiros itens)
    if (POPULATION_SIZE < 50):
        prob = 0.2 # 20%
    else:
        prob = 10/POPULATION_SIZE

    for i in range(POPULATION_SIZE):
        if (choseWithProb(prob)):
            return i
    #se nao escolher nenhum no for, escolhe entre os 20% primeiros
    return random.randint(0,int(POPULATION_SIZE/(2.0*GROUP_1_SIZE)))

def groupRoulette():
    group = np.random.choice([1,2,3], 1, p= [GROUP_1_PROB, GROUP_2_PROB, GROUP_3_PROB])[0]
    groupSizes = getGroupSizes()
    if (group == 1):
        index = random.randint(0,groupSizes[0]-1)
    elif (group == 2):
        index = random.randint(groupSizes[0], groupSizes[0]+groupSizes[1]-1)
    elif (group == 3):
        index = random.randint(groupSizes[0] + groupSizes[1], groupSizes[0] + groupSizes[1] + groupSizes[2]-1)
    else:
        print ("ERRO que nao deveria acontecer: groupRoulette")
        sys.exit(1)
    return index

def generateNewSolutionGroup(population, populationValues, itemList, numItems):
    newSolution = [0 for i in range(numItems)]
    index1 = groupRoulette()
    index2 = groupRoulette()
    #print ("debug indexes: " + str(index1) +", "+str(index2)) #debug
    newSolution = crossover(population[index1], population[index2], numItems)
    return newSolution

def getBestSolution(population, populationValues):
    bestSolution = list(population[0])
    bestSolutionValue = -1
    for i in range(POPULATION_SIZE):
        if(populationValues[i] >= bestSolutionValue):
            bestSolutionValue = populationValues[i]
            bestSolution = list(population[i])
    return bestSolution, bestSolutionValue

def getBestAndSecondSolution(population, populationValues):
    bestSolution = list(population[0])
    secondBestSolution = list(population[0])
    bestSolutionValue = populationValues[0]
    secondBestSolutionValue = populationValues[0]
    for i in range(POPULATION_SIZE):
        if(populationValues[i] > bestSolutionValue):
            secondBestSolutionValue = bestSolutionValue
            secondBestSolution = list(bestSolution)
            bestSolutionValue = populationValues[i]
            bestSolution = list(population[i])
        elif(populationValues[i] < bestSolutionValue and populationValues[i] > secondBestSolutionValue):
            secondBestSolutionValue = populationValues[i]
            secondBestSolution = list(population[i])
    return bestSolution, bestSolutionValue, secondBestSolution, secondBestSolutionValue

def mutation(solution, numItems):
    for i in range(int(numItems*TAXA_MUTACAO)):
        randomIndex = random.randint(0,numItems-1)
        solution[randomIndex] = (1 - solution[randomIndex])
    return solution

def generateNewPopulationRoulette(population, populationValues, itemList, numItems):
    #roulette version
    #sort population by solution values
    #newPopulation = sorted(population, key= lambda solution: getSolutionValue(solution, itemList))
    newPopulation = []
    bestSolution, bestSolutionValue, secondBestSolution, secondBestSolutionValue = getBestAndSecondSolution(population, populationValues)
    newPopulation.append(bestSolution)
    newPopulation.append(secondBestSolution)
    populationProbabilities = getPopulationProbabilities(populationValues)
    #populationProbabilities = getSquaredPopulationProbabilities(populationValues) #alternative version
    for i in range(POPULATION_SIZE-2): # ja botamos os 2 melhores
        newSolution = list(generateNewSolutionRoulette(population, populationValues, itemList, numItems, populationProbabilities))
        if(choseWithProb(PROB_MUTACAO)):
            newSolution = mutation(newSolution, numItems)
        # nao aceita repetidos:
        while (newSolution in newPopulation):
            newSolution = list(generateNewSolutionRoulette(population, populationValues, itemList, numItems, populationProbabilities))
            if(choseWithProb(PROB_MUTACAO)):
                newSolution = mutation(newSolution, numItems)

        newPopulation.append(list(newSolution))
    return newPopulation


def getGroupSizes():
    # devolve o tamanho dos grupos de uma populacao
    populationLeft = POPULATION_SIZE
    groupSizes = [0 for i in range(3)]
    groupSizes[2] = int(POPULATION_SIZE/GROUP_3_SIZE) #10%
    populationLeft -= groupSizes[2]
    proportionLeft = GROUP_1_SIZE/(100 - GROUP_3_SIZE) #20%
    groupSizes[0] = int(proportionLeft*populationLeft)
    groupSizes[1] = populationLeft - groupSizes[0]
    if sum(groupSizes) != POPULATION_SIZE:
        print ("ERRO que nao deveria acontecer: getGroupSizes()")
    #print ("debug group sizes: " +str(groupSizes)) #debug
    return groupSizes

def generateNewPopulationGroups(population, populationValues, itemList, numItems):
    #groups version
    #sort population by solution values
    populationAndValues = sorted(zip(population, populationValues), key= lambda pair: pair[1], reverse=True)
    sortedPopulation = [ x[0] for x in populationAndValues]
    sortedPopulationValues = [ x[1] for x in populationAndValues]

    groupSizes = getGroupSizes()

    newPopulation = []

    for i in range(groupSizes[0]):
        newPopulation.append(list(sortedPopulation[i]))
    for i in range(groupSizes[1]):
        newSolution = list(generateNewSolutionGroup(sortedPopulation, sortedPopulationValues, itemList, numItems))
        if(choseWithProb(PROB_MUTACAO)):
            newSolution = mutation(newSolution, numItems)
        # nao aceita repetidos:
        while (newSolution in newPopulation):
            newSolution = list(generateNewSolutionGroup(sortedPopulation, sortedPopulationValues, itemList, numItems))
            if(choseWithProb(PROB_MUTACAO)):
                newSolution = mutation(newSolution, numItems)
        newPopulation.append(list(newSolution))
    for i in range(groupSizes[2]):
        #generates a random solution
        newSolution = [choseWithProb(PROB_INITIAL_SOLUTION) for j in range(numItems)]
        # nao aceita repetidos:
        while (newSolution in newPopulation):
            newSolution = [choseWithProb(PROB_INITIAL_SOLUTION) for j in range(numItems)]
        newPopulation.append(list(newSolution))
    return newPopulation

def isSolutionValid(solution, itemList, numItems):
    #returns True if the solution doesn't exceed the cap for any second, False otherwise
    for t in range(min_s, max_s + 1 ): # segundo de termino
        totalWeight = 0
        for i in range(numItems):
            if (solution[i]==1) and (t in range(itemList[i]['startTime'], itemList[i]['endTime'] + 1)):
                totalWeight += itemList[i]['weight']
        if totalWeight > capacity:
            return False
    return True

def getSolutionValue(solution, itemList, numItems):
    #get total backpack value for a solution
    solutionValue = 0
    for i in range(numItems):
        if solution[i]:
            solutionValue += itemList[i]['value']
    return solutionValue


def adjustSolution(solution):
    i = random.choice(range(numItems))
    while(solution[i] != 1):
        if (i < numItems-1):
            i += 1
        else:
            i = 0
    solution[i] = 0
    return solution

def evaluatePopulationRemoveInvalid(population, itemList, capacity, numItems):
    populationValues = [0 for i in range(POPULATION_SIZE)]
    for i in range(POPULATION_SIZE):
        while (not isSolutionValid(population[i], itemList, numItems)): #solucao invalida, acima da capacidade
            population[i] = adjustSolution(population[i])
        populationValues[i] = int(getSolutionValue(population[i], itemList, numItems))
    return populationValues


def evaluatePopulation(population, itemList, capacity, numItems):
    populationValues = [0 for i in range(POPULATION_SIZE)]
    for i in range(POPULATION_SIZE):
        if (not isSolutionValid(population[i], itemList, numItems)): #solucao invalida, acima da capacidade
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

def endLoopCondition(population, populationValues, stableSolutionCounter, currentBestSolutionValue):
    # returns stableSolutionCounter, currentBestSolutionValue, and the endLoop
    bestSolution, bestSolutionValue = getBestSolution(population, populationValues)
    if (currentBestSolutionValue == bestSolutionValue):
        stableSolutionCounter += 1
        print("\n --- bestSolution nao muda a " + str(stableSolutionCounter) + " geracoes ---")
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
seedValue =  abs(hash(seed))%((2**32) - 1)
#print ("seedValue " + str(seedValue))
random.seed(a=seedValue)
np.random.seed(seedValue)

inp = open(sys.argv[1], 'rU').read().splitlines()

numItems = int(inp[0])
capacity = int(inp[1])

inp.remove(inp[0])   #  delete those 2 lines we've already used so we're left with the items themselves only
inp.remove(inp[0])

itemList = getItemList(inp)
#print itemList #debug

min_s, max_s = getRange()

solution =[ 0 for i in range(numItems+1)] #initialization

startTime = time.time() # medir o tempo de execucao a partir daqui?

population = generateInitialPopulation(numItems,seed)
populationValues = [ 0 for i in range(POPULATION_SIZE)]
stableSolutionCounter = 0 # number of iterations in which the currentBestSolution didnt change
currentBestSolutionValue = -1

for i in range(NUM_GERACOES):
    #avalia a populacao de solucoes
    populationValues = evaluatePopulation(population, itemList, capacity, numItems)

    stableSolutionCounter, currentBestSolutionValue, endLoop =  endLoopCondition(population, populationValues, stableSolutionCounter, currentBestSolutionValue)
    if (endLoop):
        print "\nendLoopCondition atingida: " +str(STABLE_ITERS_STOP) +" iteracoes sem mudancas na melhor solucao"
        print "(geracao " +str(i) +")"
        break;

    if True or i==0 or i == int(NUM_GERACOES*2/3): #debug
        print "\n\n-> geracao " + str(i)
        #printPopulationAndValues(population, populationValues)
        printPopulationValues( populationValues)

    #gera nova populacao de solucoes
    #population = generateNewPopulationGroups(population, populationValues, itemList, numItems)
    population = generateNewPopulationRoulette(population, populationValues, itemList, numItems)


populationValues = evaluatePopulation(population, itemList, capacity, numItems)
bestSolution, bestSolutionValue = getBestSolution(population, populationValues)
endTime = time.time()

totalTime = endTime - startTime

print "\n\n --- populacao final ---\n"
#printPopulationAndValues(population, populationValues)
printPopulationValues( populationValues)
print "\n --- melhor solucao encontrada ---"
print str(bestSolution) + "\nvalor: " + str(bestSolutionValue)
print ("tempo de execucao: " +str(totalTime) +" segundos")
