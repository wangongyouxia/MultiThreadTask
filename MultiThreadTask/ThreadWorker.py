import platform
if platform.python_version().startswith('4'):
	import _threading as threading
else:
	import threading
import logging

class FalseQueue():
	def get_nowait(self):
		return []
	def empty(self):
		return False

def worker(func,thread_num,no_params=False,params_queue=None,callback = None,endless = False):
	logging.debug('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!about to create thread')
	thread_list = []
	for i in range(thread_num):
		if endless:
			fq = FalseQueue()
			thread_list.append(threading.Thread(target=task_loop,args=[func,no_params,fq,callback]))
		else:
			thread_list.append(threading.Thread(target=task_loop,args=[func,no_params,params_queue,callback]))
	for t in thread_list:
		t.start()
	for t in thread_list:
		t.join()

def task_loop(func,no_params,params_queue=None,callback=None):
	if not no_params:
		while not params_queue.empty():
			try:
				params = params_queue.get_nowait()
			except:
				continue
			ret = func(*(params))
			if callback:
				callback(ret)
	else:
		while not params_queue.empty():
			try:
				params = params_queue.get_nowait()
			except:
				continue
			ret = func()
			if callback:
				callback(ret)
