class Animal:
	
	def __init__(self):
		self.name = 'animal'
		self.__str = 'hello world' #all the private property and functions can not be inherited
	
	def hello(self):
		print(self.__str)
		
	def eat(self):
		pass
	
	def sleep(self):
		pass
	
class Dog(Animal):
	
	#if son without this, he will inherit his father's
	def __init__(self,name):
		#if you want to use the father's __init__ but also retain yourself, use the super
		super().__init__()
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
