#the any object's father is <object>
class A(object):
	
	def test(self):
		print('This is type A')
		
class B:
	
	def Test(self):
		print('This is type B')
		
class C(A,B):
#the grade of A is higher than B
	
	def test_c(self):
		print('This is the type C')
		
c = C()
C.__mro__ #print the father inherit grade
c.test() #follow the order number of grade
