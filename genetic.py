# this script receives a temporal knapsack instance such as U2
# and generates a new (.sol ??? ou txt mesmo???) file containing a solution for the instance
# usage example:
# python genetic.py tkp_instances/U2

import sys



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



### main ###
if (len(sys.argv) < 2 or len(sys.argv) > 2):
    print "\nERRO: numero invalido de argumentos\n\n"
    sys.exit(1)

inp = open(sys.argv[1], 'rU').read().splitlines()

numItens = int(inp[0])
capacity = int(inp[1])

inp.remove(inp[0])   #  delete those 2 lines we've already used so we're left with the items themselves only
inp.remove(inp[0])

itemList = getItemList(inp)
#print itemList #debug
