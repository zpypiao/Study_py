#this defeat from module import *
__all__ = ['istr'] #this decide the function can be use in other file when import

def istr(str):
	if type(str) == <class 'str'>:
		return True
	else:
		return False

def this(a*):
	return True
	
print('This is a test code',istr('acv')) #this will be excuted when import

if __name__ == '__mian__':
	print('This is a test code',istr('acv')) #when this is a file instead of a module,it will be excuted

'''
put a __init__.py file in the path of your module, it have no necessary to write anything,but it can be used by python2
'''
