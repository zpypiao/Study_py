from queue import Queue
FIFO = 'first input first output'
LIFO = 'last input first output'
PriorityQueue = 'output by priority'

queue = Queue()
queue.put('first production')
queue.qsize()
queue.get()
