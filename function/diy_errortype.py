class Passworgcheck(object):
	
	def __init__(self,pw,min_length):
		self.pw = pw
		self.min_length = min_length
		
	def __str__(self):
		return 'Invaild password,the minnest length is %s'%self.min_length
	
def reg(username,password):
	if len(password)<6:
		raise Passwordcheck(password,6) #get the designed error
	else:
		print('username:%s,password:%s'%(username,password))
	
try:
	reg('zs','123')
except Passwordcheck as ex:
	print('first:'+ex)
except Exception as ex:
	print('second:'+ex)
