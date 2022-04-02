try:
	print(a)
	i = 1/0 #code in this line have not be active
#except NameError:
except (FileNotFoundError,ZeroOivisionError) as ex:
	print('You have a NameError')
	print(ex) #ex: the error has been captured
	
a='123'
f = open('text.txt')
try:	
	f.write('hello\n')
	f.write('%s'%a)
except Exception as ex:#Exception is all error's father
	print(ex)
f.close
