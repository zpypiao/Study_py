class Animal:
	
	def __init__(self):
		self.name = 'animal'
		self.__str = 'hello world' #the private property can not be inherited
	
	def hello(self):
		print(self.__str)
		
	def eat(self):
		pass
	
	def sleep(self):
		pass
	
class Dog(Animal):
	
	#if son without this, he will inherit his father's
	def __init__(self,name):
		seif.name = name
		
	def shout(self):
		pass
	
class Cat(Animal):
	
	def __init__(self,name):
		seif.name = name
	
	def catch(self):
		pass
	
class Hashq(Dog):
	
	def fight(self):
		pass
