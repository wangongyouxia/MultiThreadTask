import multiprocessing
import ThreadWorker
import logging
import signal

class MultiThreadTask():
	have_added_task_num = 0

	def __init__(self,func,params_list,thread_num,no_params=False,endless=False,task_per_thread=1,callback=None):
		self.func = func
		self.params_list = params_list
		self.task_num = len(params_list)
		self.thread_num = thread_num
		self.task_per_thread = task_per_thread
		self.callback=callback
		self.no_params = no_params
		self.init()

	def add_thread_worker_into_pool(self):
		if self.have_added_task_num < self.task_num:
			if self.task_num-self.have_added_task_num > self.task_per_thread:
				add_num = self.task_per_thread
			else:
				add_num = self.task_num-self.have_added_task_num
			self.have_added_task_num += add_num
			logging.debug('add %s into pool'%self.params_list[-1*(add_num):])
			self.pool.apply_async(self.worker,args=(self.func,self.no_params,self.params_queue,self.callback))
			#self.pool.apply(ThreadWorker.worker,args=(self.func,self.task_per_thread,self.params_list[-1*(add_num):]))
			self.params_list = self.params_list[:-1*add_num]
			return 
		else:
			return

	def start(self,nouse=None):
		#ret = self
		logging.debug('the self.thread_num_list is %s'%self.thread_num_list)
		for i in range(self.process_num):
			logging.debug('add %s thread into pool'%self.thread_num_list[i])
			self.pool.apply_async(ThreadWorker.worker,args=(self.func,self.thread_num_list[i],self.no_params,self.params_queue,self.callback))
			#self.add_thread_worker_into_pool()
		self.pool.close()
		self.pool.join()

	def exit(self,a=0,b=1):
		self.pool.terminate()

	def init(self):
		signal.signal(signal.SIGINT, self.exit)  
		signal.signal(signal.SIGTERM, self.exit)  
		self.process_num = multiprocessing.cpu_count()
		self.pool = multiprocessing.Pool(self.process_num)
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
