import multiprocessing
import ThreadWorker

class MultiThreadTask():
	have_added_task_num = 0

	def __init__(self,func,params_list,thread_num,no_params=False,endless=False,task_per_thread=1,callback=None):
		self.func = func
		self.params_list = params_list
		self.task_num = len(params_list)
		self.thread_num = thread_num
		self.task_per_thread = task_per_thread
		self.callback=callback
		self.init()

	def add_thread_worker_into_pool(self):
		if self.have_added_task_num < self.task_num:
			if self.task_num-self.have_added_task_num > self.task_per_thread:
				add_num = self.task_per_thread
			else:
				add_num = self.task_num-self.have_added_task_num
			self.have_added_task_num += add_num
			print('add %s into pool'%self.params_list[-1*(add_num):])
			self.pool.apply_async(ThreadWorker.worker,args=(self.func,self.task_per_thread,self.params_list[-1*(add_num):]),callback=self.callback)
			self.params_list = self.params_list[:-1*add_num]
			return self
		else:
			return None

	def start(self):
		ret = self
		while ret:
			ret = self.add_thread_worker_into_pool()

	def init(self):
		if multiprocessing.cpu_count() > self.thread_num:
			self.process_num = self.thread_num
		else:
			self.process_num = multiprocessing.cpu_count()
		self.pool = multiprocessing.Pool(self.process_num)
