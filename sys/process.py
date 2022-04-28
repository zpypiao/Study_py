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
