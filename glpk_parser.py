import sys
#  this program receives a temporal knapsack instance such as U2 and generates a new file modeling that same instance as a GLPK data file
#  NEED TO REMOVE THE 'INSTANCE FEATURES' SECTION FROM IXXX AND UXXX FILES

inp = open(sys.argv[1], 'rU').read().splitlines()  	#  read the input file in  a list of its lines

out = open(sys.argv[1] + '_GLPK.dat', 'w')

n = str('param n := ' + inp[0] +'\n')  #  write the number of items (first line of input file) to the output file
out.write(n)
out.write('\n\n')

cap = str('param c := ' + inp[1] +'\n')   #  write the capacity (second line of input file) to the output file
out.write(cap)
out.write('\n\n')


inp.remove(inp[0])   #  delete those 2 lines we've already used so we're left with the items themselves only
inp.remove(inp[0])

inp = [l.split() for l in inp]   #  split each line so we have a list of items with their respectives properties in a list ([value, weight, start, final]) 


value = [l[0] +' ' for l in inp]  #  create a list for each of the properties. e.g, value list will contain the value for each of the n items in sequence

weight = [l[1] +' ' for l in inp] 

start = [l[2] +' ' for l in inp]

end = [l[3] +' ' for l in inp]


out.write('set l := ')  #  then we write those lists to our output file
out.writelines(value)
out.write('\n\n')

out.write('set d := ')
out.writelines(weight)
out.write('\n\n')

out.write('set s := ')
out.writelines(start)
out.write('\n\n')

out.write('set t := ')
out.writelines(end)
out.write('\n\n')

out.close
