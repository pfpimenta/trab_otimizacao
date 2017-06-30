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
    item = { 'v': 0, 'w': 0, 's': 0, 'e': 0}
    #v: value, w: weight, s: start time, e: end time
    itemList = []
    for line in inp:
        lineWords = line.split(" ")
        item['v'] = int(lineWords[0])
        item['w'] = int(lineWords[1])
        item['s'] = int(lineWords[2])
        item['e'] = int(lineWords[3])
        itemList.append(item.copy())

    return itemList

def choseWithProb( oneProb ):
    #  zeroProb = 1 - oneProb
    #  result = np.random.choice([0,1], 1, p= [zeroProb, oneProb ])[0]
    rand =  random.random()
    if rand <= oneProb:
        return 1
    else:
        return 0

def getRange ():
    min_s = 9999999999999999
    max_s = -100000
    for item in itemList:
        if item['s'] < min_s:
            min_s = item['s']
        if item['e'] > max_s:
            max_s = item['e']
    return min_s, max_s

def generateInitialPopulation():
    new_population = []
    for i in range(populationSize):
        #generates a random solution
        solution = [choseWithProb(PROB_INITIAL_SOLUTION) for j in range(numItems)]
        #prob = (2/math.sqrt(numItems)) / (1 + 2/math.sqrt(numItems))
        # nao aceita repetidos:
        while (solution in new_population):
            solution = [choseWithProb(PROB_INITIAL_SOLUTION) for j in range(numItems)]
        new_population.append(solution)

    return new_population

def isSolutionValid(sol):
    #returns True if the solution doesn't exceed the cap for any second, False otherwise
    secs = [0 for i in range(min_s, max_s + 1)]
    for i in range(numItems):
        if sol[i] == 1:
            for j in range(itemList[i]['s'], itemList[i]['e'] ):  #  TODO why no  +1 here??? shit goes crazy
                secs[j] += itemList[i]['w']

    for i in secs :
        if i > capacity:
            return False
    return True

def deWeight(weights, sol, second):
    for j in range(numItems):
        if sol[j] == 1 and second in range(itemList[j]['s'], itemList[j]['e']+1):
            sol[j] = 0
            for time in range(itemList[j]['s'], itemList[j]['e']+1):
                weights[time] -= itemList[j]['w']
            return weights, sol

    print ("deWeight falhou")
    #print "weights: " + str(weights) + " sol:"+str(sol)
    exit(1)

def adjustSolution2(sol):
    # weights = [0 for i in range(min_s, max_s + 1)]
    weights = {i:0 for i in range(min_s, max_s + 1)}
    for i in range(numItems):
        if sol[i] == 1:
            for j in range(itemList[i]['s'], itemList[i]['e'] +1 ):
                weights[j] += itemList[i]['w']


    for second in range(min_s, max_s + 1):
        while weights[second] > capacity:
            #print "debug weights[i]: " + str(weights[second]) + " capacity:"+str(capacity)+" second: "+str(second)
            weights, sol = deWeight(weights, sol, second)
    return sol

def adjustSolution(sol):
    i = random.choice(range(numItems))
    while(sol[i] != 1):
        if (i < numItems-1):
            i += 1
        else:
            i = 0
    sol[i] = 0
    return sol

def getSolutionValue(sol):
    #get total backpack value for a solution
    solutionValue = 0
    for i in range(numItems):
        if sol[i]:
            solutionValue += itemList[i]['v']
    return solutionValue

def evaluatePopulation():
    for i in range(populationSize):
        #  while not isSolutionValid(population[i]): #solucao invalida, acima da capacidade
        population[i] = adjustSolution2(population[i])
        populationValues[i] = int(getSolutionValue(population[i]))
        """if not isSolutionValid(population[i]):
            populationValues[i] = 1
        else:
            populationValues[i] = int(getSolutionValue(population[i]))"""

def crossover(parent1, parent2):
    newSolution = [0 for i in range(numItems)]
    #  point = random.choice(range(numItems))
    point = numItems/2
    for i in range(point):
        newSolution[i] = parent1[i]
    for i in range(point, numItems):
        newSolution[i] = parent2[i]
    return newSolution

def groupRoulette():
    rand = random.random()
    groupSizes = getGroupSizes()
    if (rand - GROUP_1_PROB <= 0): #group 1
        index = random.randint(0,groupSizes[0]-1)
    elif (rand - (GROUP_1_PROB + GROUP_2_PROB) <= 0): #group 2
        index = random.randint(groupSizes[0], groupSizes[0]+groupSizes[1]-1)
    elif (rand - (GROUP_1_PROB + GROUP_2_PROB + GROUP_3_PROB) <= 0): #group 3
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
    newSolution = crossover(population[index1], population[index2])
    return newSolution

def mutation(solution):
    for i in range(int(numItems*TAXA_MUTACAO)):
        randomIndex = random.randint(0,numItems-1)
        solution[randomIndex] = (1 - solution[randomIndex])
    return solution

def getGroupSizes():
    # devolve o tamanho dos grupos de uma populacao
    populationLeft = populationSize
    groupSizes = [0 for i in range(3)]
    groupSizes[2] = int(populationSize/GROUP_3_SIZE) #10%
    populationLeft -= groupSizes[2]
    proportionLeft = GROUP_1_SIZE/(100 - GROUP_3_SIZE) #20%
    groupSizes[0] = int(proportionLeft*populationLeft)
    groupSizes[1] = populationLeft - groupSizes[0]
    if sum(groupSizes) != populationSize:
        print ("ERRO que nao deveria acontecer: getGroupSizes()")
    #print ("debug group sizes: " +str(groupSizes)) #debug
    return groupSizes

def generateNewPopulation():
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
            newSolution = mutation(newSolution)
        # nao aceita repetidos:
        while (newSolution in newPopulation):
            newSolution = list(generateNewSolutionGroup(sortedPopulation, sortedPopulationValues, itemList, numItems))
            if(choseWithProb(PROB_MUTACAO)):
                newSolution = mutation(newSolution)
        newPopulation.append(list(newSolution))
    for i in range(groupSizes[2]):
        #generates a random solution
        newSolution = [choseWithProb(PROB_INITIAL_SOLUTION) for j in range(numItems)]
        # nao aceita repetidos:
        while (newSolution in newPopulation):
            newSolution = [choseWithProb(PROB_INITIAL_SOLUTION) for j in range(numItems)]
        newPopulation.append(list(newSolution))
    return newPopulation



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
    print ("genaGroup.py")
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
    print "'python genetic.py inputFile seed populationSize'\n\n"
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
    #print populationValues

    endLoopCondition()
    if endLoop:
        break;

    generateNewPopulation()

    #print "3"

endTime = time.time()

totalTime = endTime - startTime

finalPrint()
