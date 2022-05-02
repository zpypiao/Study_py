'''thread is a lightweight process'''
'''thread is a component of process'''
'''thread can use the variton in common'''

#coding=utf-8
import threading
import time

def fun():
	print('This is a thread executing...')
	time.sleep(2)
	
if __name__=='__mian__':
	for i in range(5):
		t = threading.Thread(target=fun)
		t.start()
		
	# get the number of threads
	length = (threading.enumerate())

# the class of thread
class MyThread(threading.Thread):
	def run(self):
		for i in range(3):
			time.sleep(1)
			msg = "I'm" + self.name + +'@' + str(i)
			print(msg)
			
if __name__=='__main__':
	t = MyThread()
	t.start()
	
'''thred cna use the global varition'''
from threading import Thread
import time
g_num = 100
def work1():
	global g_num
	for i in range(3):
		g_num += 1
	print('g_num is %d in worke1'%g_num)
	
def work2():
	global g_num
	print('g_num in work2 is %d'%g_num)

print('the g_num before work is %d'%g_num)
t1 = Thread(target=work1)
t1.start()
time.sleep(1)
t2 = Thread(target=work2)
t2.start()

def work():
	global g_num
	for i in range(10000):
		g_num += 1

for i in range(2):
	t = threading.Thread(target=work)
	t.start
	
>> 5000
'''this is an error result, beacuse the exchange of threads have been interuputed'''
'''so we add a sleep to function'''
