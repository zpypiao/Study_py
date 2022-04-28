import functools
dir(functools)

def showarg(*args, **kwargs):
	print(args)
	print(kwargs)
	
# partial function
p1 = functools.partial(showarg, 1, 2, 3)
p1()
>> (1, 2, 3)
>> {}
p1(4, 5, 6)
>> (1, 2, 3, 4, 5, 6)

# wraps
def note(func):
	"not function"
	@functools.wraps(func) # eliminate the bad influence of the decorator
	def wrapper():
		print('note something')
		return func()
	return wrapper

@note
def test():
	"test function"
	print('I am test.')
	
test()
print(test.__doc__)

>> note something
>> test function
