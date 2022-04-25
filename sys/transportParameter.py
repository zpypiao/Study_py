#this will be excute when program has excuted
name = input('Please enter the name:')

import sys

#sys.argv is a function to get the input when progarm has been start in cmd
print(sys.argv)

#list generator
a = [i for i in range(10)]

#this is a cycle in cycle
b = [i for i in range(1,3) for j in range(0,2)]

#cycle with condition
c = [i for i in range(100) if i%2 == 0]

#set
d = {1, 2, 3, 4}
d.add(5)

#this is an empty set
e = set()
