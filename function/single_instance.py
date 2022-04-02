#single instance one
class User(object):
	
	def __init__(self,name):
		self.name = name
	
	#fake single instance
	__instance = None
	@classmethod
	def get_instance(cls,name):
		if not cls.__instance:
			cls.__instance = User(name)
		return cls.__instance

u1 = User('lh')
u2 = get_instance('ay')
#id(object) return the physist address of object
print('the address of u1'%id(u1))

#single instance two
class User(object):
	
	def __init__(self,name):
		self.name = name
	
	#recommand
	__instance = None
	def __new__(cls,name):
		if not cls.__instance:
			cls.__instance = object.__new__(cls)
		return cls.__instance
	
#bug
u3 = object.__new__(User)
