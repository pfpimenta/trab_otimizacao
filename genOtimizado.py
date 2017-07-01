import sys
import random
import math
import time

#metaparametros do aloritmo genetico
#POPULATION_SIZE = 100
NUM_GERACOES = 100 # nao sei se isso pode #TODO
PROB_MUTACAO = 0.25 # probabilidade de uma nova solucao sofrer mutacao
TAXA_MUTACAO = 0.3 # porcentagem de genes q sao alterados por uma mutacao
PROB_INITIAL_SOLUTION = 0.8  #  podia ser +-  ==10/numItems
STABLE_ITERS_STOP =  4 # numero maximo de iteracoes sem mudar a melhor solucao


def getItemList( inp ): # alt version
    #receives the input instance without the first 2 lines
    #retorns a dict with 4 lists: of all the items' values, weights, start times, and end times
    itemList = { 'v': [], 'w': [], 's': [], 'e': []}
    #v: values, w: weights, s: start times, e: end times
    for line in inp:
        lineWords = line.split(" ")
        itemList['v'].append( int(lineWords[0]))
        itemList['w'].append( int(lineWords[1]))
        itemList['s'].append( int(lineWords[2]))
        itemList['e'].append( int(lineWords[3]))
    return itemList

def getItemIndexesPerSecond():
    itemIndexesPerSecond = {second:[] for second in secondsList}
    #for second in secondsList:
    for itemIndex in range(numItems):
        for second in range(itemList['s'][itemIndex],itemList['e'][itemIndex] + 1): #+1 pra incluir o ultimo segundo
            itemIndexesPerSecond[second].append(itemIndex)
    #print ("debug itemIndexesPerSecond: " +str(itemIndexesPerSecond)) #debug
    return itemIndexesPerSecond

def choseWithProb( oneProb ):
    # returns 1 with probability == oneProb
    # returns 0 with probability == (1 - oneProb)
    rand =  random.random()
    if rand <= oneProb:
        return 1
    else:
        return 0

def getRange ():
    min_s = 9999999999999999
    max_s = -100000
    for i in range(numItems):
        if itemList['s'][i] < min_s:
            min_s = itemList['s'][i]
        if itemList['e'][i] > max_s:
            max_s = itemList['e'][i]
    return min_s, max_s


def generateInitialPopulation():
    new_population = []
    for i in range(populationSize):
        #generates a random solution
        solution = [choseWithProb(PROB_INITIAL_SOLUTION) for j in range(numItems)]
        new_population.append(solution)
    return new_population


def deWeight(weights, solution, second):
    for itemIndex in itemIndexesPerSecond[second]:
        if solution[itemIndex] == 1:
            solution[itemIndex] = 0
            for time in range(itemList['s'][itemIndex], itemList['e'][itemIndex]+1):
                weights[time] -= itemList['w'][itemIndex]
            return weights, solution

    print ("deWeight2 falhou")
    #print "weights: " + str(weights) + " solution:"+str(solution) #debug
    exit(1)

def adjustSolution(solution):
    # optimized version
    weights = {second:0 for second in secondsList}

    for second in secondsList:
        for itemIndex in itemIndexesPerSecond[second]:
            if solution[itemIndex] == 1:
                weights[second] += itemList['w'][itemIndex]
        while weights[second] > capacity:
            #print "debug weights[i]: " + str(weights[second]) + " capacity:"+str(capacity)+" second: "+str(second) #debug
            weights, solution = deWeight(weights, solution, second)
    return solution

def getSolutionValue(solution):
    #get total backpack value for a solution
    solutionValue = 0
    for itemIndex in range(numItems):
        if solution[itemIndex]:
            solutionValue += itemList['v'][itemIndex]
    return solutionValue

def evaluatePopulation():
    #ajusta as solucoes invalidas e avalia cada solucao
    for i in range(populationSize):
        population[i] = adjustSolution(population[i]) # ajusta solucoes invalidas, acima da capacidade
        populationValues[i] = int(getSolutionValue(population[i]))

def crossover(parent1, parent2):
    newSolution = [0 for i in range(numItems)]
    #  point = random.choice(range(numItems))
    point = numItems/2
    for i in range(point):
        newSolution[i] = parent1[i]
    for i in range(point, numItems):
        newSolution[i] = parent2[i]
    return newSolution


def generateNewSolution():
    sum_v = 0
    for i in range(populationSize):
        sum_v += populationValues[i]
    point1 = random.randint(0,sum_v - 1)
    point2 = random.randint(0,sum_v - 1)
    parent1 = 0
    parent2 = 0

    for i in range(populationSize):
        if point1 <=0:
            parent1 = i
            break;
        point1 -= populationValues[i]
    for i in range(populationSize):
        if point2 <=0:
            parent2 = i
            break;
        point2 -= populationValues[i]

    newSolutiion = crossover(population[parent1],population[parent2])
    return newSolutiion

def mutation(solution):
    for i in range(int(numItems*TAXA_MUTACAO)):
        randomIndex = random.randint(0,numItems-1)
        solution[randomIndex] = (1 - solution[randomIndex])
    return solution

def generateNewPopulation():
    newPopulation = []
    newPopulation.append(currentBestSolution)
    newPopulation.append(currentSecondSolution)
    newPopulation.append(crossover(currentBestSolution, currentSecondSolution))
    #populationProbabilities = getSquaredPopulationProbabilities(populationValues) #alternative version
    for i in range(populationSize-3): # ja botamos os 2 melhores
        newSolution = generateNewSolution()
        if(choseWithProb(PROB_MUTACAO)): # TODO
            newSolution = mutation(newSolution)
        newPopulation.append(list(newSolution))
    global population
    population = newPopulation


def endLoopCondition():
    # returns stableSolutionCounter, currentBestSolutionValue, and the endLoop
    global currentBestSolutionValue, stableSolutionCounter, endLoop, currentBestSolution, currentSecondSolution, currentSecondSolutionValue
    bestSolution, bestSolutionValue, secondSolution, secondSolutionValue = getBestAndSecondSolution()
    if (currentBestSolutionValue == bestSolutionValue):
        stableSolutionCounter += 1
        # print("\n --- bestSolution nao muda a " + str(stableSolutionCounter) + " geracoes ---")
    elif(currentBestSolutionValue > bestSolutionValue):
        print "\n-\n-\nERRO: algo ta errado, a melhor solucao piorou\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-"
        print "current: " +str(currentBestSolutionValue) + "\nnova: " +str(bestSolutionValue) +"\n"
    else: # currentBestSolution < bestSolution
        currentBestSolutionValue = bestSolutionValue
        stableSolutionCounter = 0
    #print  "debug " +str(stableSolutionCounter) + ", " +str(currentBestSolution) #debug
    if (stableSolutionCounter >= STABLE_ITERS_STOP):
        endLoop = 1
    else:
        endLoop = 0
    currentBestSolutionValue = bestSolutionValue
    currentBestSolution = bestSolution
    currentSecondSolutionValue = secondSolutionValue
    currentSecondSolution = secondSolution


def getBestAndSecondSolution():
    bestSolution = list(population[0])
    secondBestSolution = list(population[0])
    bestSolutionValue = populationValues[0]
    secondBestSolutionValue = populationValues[0]
    for i in range(populationSize):
        if(populationValues[i] > bestSolutionValue):
            secondBestSolutionValue = bestSolutionValue
            secondBestSolution = list(bestSolution)
            bestSolutionValue = populationValues[i]
            bestSolution = list(population[i])
        elif(populationValues[i] < bestSolutionValue and populationValues[i] > secondBestSolutionValue):
            secondBestSolutionValue = populationValues[i]
            secondBestSolution = list(population[i])
    return bestSolution, bestSolutionValue, secondBestSolution, secondBestSolutionValue

def finalPrint():
    # pra printar no arquivo os resultados
    print ("\n --- genOtimizado.py results ---")
    print ("instancia: " +str(sys.argv[1]))
    print ("population size: " +str(populationSize))
    print ("melhor solucao: " +str(currentBestSolution))
    print ( "valor da melhor solucao: "+str(currentBestSolutionValue))
    print ("tempo de execucao: " +str(totalTime))




############
### main ###
############

if (len(sys.argv) < 4 or len(sys.argv) > 4):
    print "\nERRO: numero invalido de argumentos\n"
    print "'python genOtimizado.py inputFile seed populationSize'\n\n"
    sys.exit(1)


seed = sys.argv[2]
seedValue =  abs(hash(seed))%((2**32) - 1)
#print ("seedValue " + str(seedValue))
random.seed(a=seedValue)

populationSize = int(sys.argv[3])

inp = open(sys.argv[1], 'rU').read().splitlines()

numItems = int(inp[0])
capacity = int(inp[1])

inp.remove(inp[0])   #  delete those 2 lines we've already used so we're left with the items themselves only
inp.remove(inp[0])

itemList = getItemList(inp)

min_s, max_s = getRange()
secondsList = range(min_s, max_s + 1)

itemIndexesPerSecond = getItemIndexesPerSecond()


startTime = time.time() # medir o tempo de execucao a partir daqui?

population = generateInitialPopulation()
populationValues = [0 for i in  range(populationSize)]
stableSolutionCounter = 0 # number of iterations in which the currentBestSolution didnt change
currentBestSolutionValue = -1
currentBestSolution = []
currentSecondSolutionValue = -1
currentSecondSolution = []
endLoop = 0
#print "1"

for i in range(NUM_GERACOES):
    #avalia a populacao de solucoes
    #populationValues = evaluatePopulation(population, itemList, capacity, numItems)
    evaluatePopulation()
    #print "2"
    print ("\n --- geracao " + str(i) + ": \n" +str(populationValues))

    endLoopCondition()
    if endLoop:
        break;

    generateNewPopulation()

    #print "3"

endTime = time.time()

totalTime = endTime - startTime

finalPrint()
