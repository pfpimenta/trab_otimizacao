# this script receives a temporal knapsack instance such as U2
# and generates a new (.sol ??? ou txt mesmo???) file containing a solution for the instance
# usage example:
# python genetic.py tkp_instances/U2

import sys
import random

#metaparametros do aloritmo genetico
POPULATION_SIZE = 20
NUM_GERACOES = 25 # nao sei se isso pode #TODO

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
    solution = [ 0 for i in range(numItems)]
    population = []
    for i in range(POPULATION_SIZE):
        solution = [random.randint(0, 1) for j in range(numItems)]
        population.append(list(solution))

    return population


def generateNewPopulation(population, populationValues):
    #TODO
    pass

def evaluatePopulation(population):
    #TODO
    populationValues = [0 for i in range(POPULATION_SIZE)]
    return populationValues


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

for i in range(POPULATION_SIZE):
    #avalia a populacao de solucoes
    populationValues = evaluatePopulation(population)
    #gera nova populacao de solucoes
    generateNewPopulation(population, populationValues)


populationValues = evaluatePopulation(population)

print "\n---\nPOPULATION:\n" + str(population)
print "\n---\nPOPULATION VALUES:\n" + str(populationValues)
