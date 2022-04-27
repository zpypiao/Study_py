def line(a, b):
	def funct(x):
		return a*x + b
	return funct

line1 = line(1, 2)
line2 = line(2, 1)

y = line1(5)
>> 7
