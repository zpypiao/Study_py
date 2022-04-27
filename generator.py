g = (i for i in range(5))
next(g)
>> 0
next(g)
>> 1
...
next(g)
>> 4
next(g)
exception: error
  
def fib(n):
    i = 0
    a, b = 0, 1
    while i<n:
        temp = yield b
        print(temp)
		a, b = b, a+b
        i += 1
    return 'done'

n = fib(5)
# n has been made as a generator
>> Null
next(n)
>> 1
g.__next__()
>> 1
g.send('hehe')
>> hehe
>> 2

form collections import Iterable
isinstance([], Iterable)
>> True
isinstance(10, Iterable)
>> False
iter([1, 2, 3]) # tranlate a iterable item to a iterator

local varition and global varition(LEGB)
locals -> enclosing function -> globals -> builtins
dir(__builtins__) # check the builtins
