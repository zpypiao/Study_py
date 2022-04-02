class Person(object):
	
	def __init__(self,name):
		self.name = name
    
	def work(self):
		axe = Factory_stone.creat_axe()
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
	
	def creat_axe(self):
		pass
	
class Factory_stone(Factory):
	
	def creat_axe(self):
		return StoneAxe('huagangyan')
	
class Factory_steel(Factory):
	
	def creat_axe(self):
		return SteelAxe('taihejin')
	
p = Person('laohuang')
p.work()
