class Person:
	
	#restart the object
	def __init__(self),name,age):
		self.name = name
		self.age = age
	
	#translate the object to this str when print object
	def __str__(self):
		return 'Hello World'

class User:
	
	def __init__(self,name,pw):
		self.name = name
		if len(pw) >= 6:
			self.__password = pw  #hiding info
		else:
			print('the pw is invalid')
	
	def get_pd(self):
		return self.__password
	
	def __hello(self): #this function can not be use out of the group
		print('Hello World')
