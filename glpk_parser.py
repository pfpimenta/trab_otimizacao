import sys
#  this script receives a temporal knapsack instance such as U2 and generates a new file modeling that same instance as a GLPK data file
#  NEED TO REMOVE THE 'INSTANCE FEATURES' SECTION FROM IXXX AND UXXX FILES

inp = open(sys.argv[1], 'rU').read().splitlines()  	#  read the input file in  a list of its lines

out = open(sys.argv[1] + '_GLPK.dat', 'w')

n = str('param n := ' + inp[0] +';\n')  #  write the number of items (first line of input file) to the output file
out.write(n)
out.write('\n\n')

cap = str('param c := ' + inp[1] +';\n')   #  write the capacity (second line of input file) to the output file
out.write(cap)
out.write('\n\n')


inp.remove(inp[0])   #  delete those 2 lines we've already used so we're left with the items themselves only
inp.remove(inp[0])

inp = ['\t\tItem' + str(i) + ' ' + l + '\n' for i, l in enumerate(inp)]   #  format each line so they're as "ItemX value weight start final" and in the right formar for the output file


out.write('param: ITEMS: l d s t := \n')  #  then we write those lines to output file
out.writelines(inp)
out.write('\t; \n\nend;\n')


out.close
