# input a function and output a new one
def embellish(funct):
	def output():
		# additonal function1
		print(1)
		# additonal function2
		print(2)
		# additonal function3
		print(funct.__name__)
		funct()
	
	return output

@embellish
def function():
	print(3)
	
function()
>> 1
>> 2
>> function
>> 3
