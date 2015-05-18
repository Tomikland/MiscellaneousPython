import math

num = int(input("Enter the depth of the tree"))
outFile = open("binaryTree.gv", "w")

#print the start
outFile.write("digraph G\n{\n\tnode [shape = record, height = .1]\n//Nodes\n")

#print the node definitions
row = 2
for n in range(pow(2,num)-1):
    outFile.write('\tnode'+str(n)+'[label = "<f0> |<f1> n | <f2>"];\n')
outFile.write('\n')

#print Row 0 separately because log(0) is undefined.
outFile.write('\t//Row 0\n')
outFile.write('\t"node0":f0 -> "node1":f1;\n')
outFile.write('\t"node0":f2 -> "node2":f1;\n')
outFile.write('\n')

n = 3
row = 1
for i in range(1,(pow(2,num)-1)//2):
    if (math.log(i, 2).is_integer()):
        outFile.write("\t//Row " + str(row) + '\n')
        row+=1
    
    outFile.write('\t"node'+str(i)+'":f0 -> "node'+str(n)+'":f1;\n')
    n+=1
    outFile.write('\t"node'+str(i)+'":f2 -> "node'+str(n)+'":f1;\n')
    n+=1
    outFile.write('\n')
    
#print the end
outFile.write("}")

outFile.close()
