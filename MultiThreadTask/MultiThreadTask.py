import multiprocessing
import ThreadWorker
import logging
import signal
import sys

class MultiThreadTask():
	have_added_task_num = 0

	def __init__(self,func,thread_num,params_list=[],no_params=False,task_num=False,callback=None):
		self.func = func
		self.params_list = params_list
		self.endless = False
		if no_params:
			if task_num == -1:
				self.endless = True
			self.task_num = task_num
			self.params_list = []
			for i in range(task_num):
				self.params_list.append([])
		else:
			self.task_num = len(params_list)
		self.thread_num = thread_num
		self.callback=callback
		self.no_params = no_params
		self.init()

	def start(self):
		logging.debug('the self.thread_num_list is %s'%self.thread_num_list)
		try:
			for i in range(self.process_num):
				logging.debug('add %s thread into pool'%self.thread_num_list[i])
				results = self.pool.apply_async(ThreadWorker.worker,args=(self.func,self.thread_num_list[i],self.no_params,self.params_queue,self.callback,self.endless))
			results.get(999999999)
		except KeyboardInterrupt:
			print("Caught KeyboardInterrupt, terminate workers and exit")
			self.pool.terminate()
			self.pool.close()
			sys.exit(0)
		else:
			self.pool.close()
		self.pool.join()

	def init_exit(self):
		signal.signal(signal.SIGINT, signal.SIG_IGN)

	def init(self):
		self.process_num = multiprocessing.cpu_count()
		self.pool = multiprocessing.Pool(self.process_num,self.init_exit)
		self.params_queue = multiprocessing.Manager().Queue(self.task_num)
		for content in self.params_list:
			self.params_queue.put(content)
		self.thread_num_list = []
		average = self.thread_num/self.process_num
		for i in range(self.process_num):
			if (self.thread_num%self.process_num) > i:
				self.thread_num_list.append(average+1)
			else:
				self.thread_num_list.append(average)
