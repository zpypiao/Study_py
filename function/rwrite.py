class A(object):
	
	def test(self):
		pass

class B(A):
	
	#when son have a same-name method with,it has been called rewritted
	#it will be used former than father
	def test(self):
		pass
