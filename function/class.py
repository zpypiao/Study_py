class Person:
	
	#restart the object
	def __init__(self,name,age):
		self.name = name
		self.age = age
	
	#when create an object, it will be used
	#it must return an object, or init will not be used.
	def __new__(cls):
		return object.__new__(cls)
	
	#this function will be displayed when object belong this group be deleted
	#when program is shut down, the object alse will be deleted
	def __del__(self):
		print('The object will be deleted, release the space')
	
	#translate the object to this str when print object
	def __str__(self):
		return 'Hello World'
	
	#class proporty can be used by all the object belong to it
	#public proporty
	name = 'huaman'
	#private(hidding) propority
	__color = 'red'
	__num = 100
	__kile = 50
	
	# get private proporty
	def getnum(self):
		return self.__color
	
	# change private proporty
	def setnum(self, num):
		if num>100:
			self.__num = num
			
	# property function
	num = property(getnum, setnum)
	
	@property
	def kile(self): # getter
		return self.__kile
	
	@num.setter
	# the name of function must be same with private proporty
	def kile(self, x): # setter
		self.__kile = x
			
n = Person(name, age)
n.num
n.num = 20
class User:
	
	def __init__(self,name,pw):
		self.name = name
		if len(pw) >= 6:
			self.__password = pw  #hiding info
		else:
			print('the pw is invalid')
	
	def get_pd(self):
		return self.__password
	
	def __hello(self): #this function can not be use out of the class
		print('Hello World')
	
	@classmethod #classmethod must have this to explain
	def h_method(cls): #cls repredent the current class, can use with no parameter
		print('Hello small human.')
	
	@staticmethod
	def stme(str): #when you use it, you must have a parameter
		print('this ia a static  %s'%str)
	
#the propority and method of class can be used by class and object		
Person.name
User.h_method()
