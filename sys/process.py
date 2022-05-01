# linux_process
import os
import time

pid = os.fork() # return 0 in branch and return branch id in total process

if pid<0:
	print('fork failed to be called')
elif pid == 0:
	time.sleep(2) # sleep two seconds
	print('this is branch process:%s, the total process id: %s'%(os.getpid(), os.getppid()))
else:
	print('this is total process:%s, my branch id: %s'%(os.getpid(), pid))
print('all can print')

# Process
# base on windows

from multiprocessing import Process
import os

def run_proc(name):
	print('branch process is runing, name: %s, pid:%s'%(name, os.getpid()))
	
if __name__ == '__main__':
	print('total process, pid:%s'%os.getpid())
	
	p = Process(target=run_proc, args=('test'))
	
	print('the branch will be started')
	
	p.start()
	p.join() # total process wait for branch process
	
	print('branch process has ended')
	
Process([group [, target [, name [, args [, kwargs]]]]])

is_alive() # judge process status
join([timeout]) # wait or wait ? time
start()
terminate() # shutdown the process


'''2022/5/1'''
from multiprocessing import Process
import time

def fun(name, num, **kwargs):
	time.sleep(2)
	print('Branch: name:%s, num:%s'%(name, num))
	for k, v in kwargs.otems():
		  print('%s:%s'%(k, s))
		  
print('Father')
p = Process(target=fun, name='piao', args=('test', 10), kwargs={'a':10, 'b': 20})
p.start()
p.join()
print('branch name:%s, id:%d'%(p.name, p.pid))
p.terminate()
print('branch process is ended')

'''ingerit Process'''
class Process_Class(Process):
	
	def __init__(self, interval):
		super.__init__()
		self.interval = interval
		
	def run(self):
		print('little baby has been started')
		t.start = time.time()
		time.sleep(self.interval)
		t.stop = time.time()
		print(t.stop - t.start)
		
'''Procesing Pool'''
from multiprocessing import Process, Pool
import os, time, random

def worker(msg):
	t.start = time.time()
	print('%s is starting, id:%d'%(msg, os.getpid()))
	time.sleep(random.random()*2)
	t.stop = time.time()
	print('%s is ended, id:%d'%(msg, os.getpid()))
pool = Pool(3)
for i in range(10):
	
	'''excute the target, this is not a co-step process'''
	pool.applay_async(worker, (i,))
	
	# this is a co-step process
	pool.apply(worker, (i,))
print('---start---')
pool.close() # close the process pool
pool.join() # this must put back of the close()
print('---end---')
