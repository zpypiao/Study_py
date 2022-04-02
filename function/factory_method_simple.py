class Person(object):
	
	def __init__(self,name):
		self.name = name
	
	'''
	def work(self):
		print('%s is starting work...'%self.name)
		
		#use stoneaxe
		axe = StoneAxe('huagangyan')
		#use steelaxe
		axe = SteelAxe('taihegang')
		axe.cut_tree()'''
	
	'''
	def work(self,axe):
		axe.cut_tree()'''
	
	def work(self,axe_type):
		axe = Factory.creat_axe(axe_type)
		axe.cut_tree
		
class Axe(object):
	
	def __init(self,name):
		self.name = name
		
	def cut_tree(self):
		print('%s is cutting the tree.'%self.name)
		
class StoneAxe(Axe):
	
	def cut_tree(self):
		print('%s is cutting the tree by stone.'%self.name)
		
class SteelAxe(Axe):
	
	def cut_tree(self):
		print('%s is cutting the tree by steel.'%self.name)
		
class Factory(object):
	
	@staticmethod
	def creat_axe(type):
		if type == 'stone':
			return StoneAxe('huagangyang')
		elif type == 'steel':
			return SteelAxe('taihejin')
		else:
			return False

p = Person('prime')
p.work('stone')
