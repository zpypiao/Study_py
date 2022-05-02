import threading

# creat a lock
mutex = threading.Lock()
# get the lock
mutex.acquire([blocking])
#release the lock
mutex.release()

def work():
	global g_num
	for i in range(1000):
		# add the lock
		m = mutex.acquire(False)
		if m:
			g_num += 1
			# release the lock
			mutex.release()
			
lock = threading.Lock()
lock.acquire() # freeze the lock
