import threading

def worker(func,task_num,params_list=None,callback = None):
	print('param about to run is %s'%params_list)
	task = threading.Thread(target=task_loop,args=[func,task_num,params_list,callback])
	task.start()
	task.join()

def task_loop(func,task_num,params_list=None,callback=None):
	if type(params_list) == list:
		for i in range(task_num):
			ret = func(*(params_list[i]))
			if callback:
				callback(*ret)
	else:
		for i in range(task_num):
			ret = func()
			if callback:
				callback(*ret)
