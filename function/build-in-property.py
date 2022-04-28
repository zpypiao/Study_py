__init__ # start
__new__ # creat
__class__ # class name
__str__ # print
__repr__
__del__ # delete
__dict__
__doc__ # help
__getattribute__
__bases__ # all the base class

class School(object):
	def __init__(self, subject1):
		self.subject1 = subject1
		self.subject2 = 'cpp'
		
	def __getattribute__(self, obj):
		if obj == 'subject1':
			# diy the rule
			print('log subject1')
			return 'redirect python'
		else: #without this, all others will be disable
			# the original rule
			return object.__getattribute__(self,obj)

s = School('python')
print(s.subject1)
print(s.subject2)

>> redirect python
>> cpp

'''Buid in function'''
range(start, stop [,step])
map(function, sequence[, sequence, ...])
filter(function or None, sequence) # None with no filt
map(function, sequence[, initial])

from functools import reduce
reduce(lambda x, y:x+y, [1, 2, 3, 4])
>> 10
