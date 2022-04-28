import sys
a = 'hello world'
sys.getrefcount(a)
>> 2

import gc

gc.disable()

gc.collect()

gc.get_threshold() # get the frequent of gc
gc.set_threshold() # set the frequent of gc

gc.garbage

gc.get_count()
