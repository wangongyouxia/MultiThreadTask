import MultiThreadTask
import os
import time

def add(x,y):
	print('I will sleep 3s...')
	time.sleep(3)
	print('%s add %s is: %s, and pid is %s'%(x,y,x+y,os.getpid()))
	return x+y

def callback_add(result):
	print('I am callback, the result of add is [%d]'%result)

def display_info(info):
	print('I will print info in 3s...')
	time.sleep(3)
	print('info is: %s'%info)
	return

def print_i_want_to_sleep():
	time.sleep(3)
	print('I want to sleep!!!!!!')

def print_i_need_money():
	time.sleep(3)
	print('I need money!!!!!!')


if __name__ == '__main__':

	# A case with parameters and callback. WARN: callback function must accept ONE parameter!
	params_list = [(1,2),(2,3),(3,4),(4,5),(5,6),(7,8)]
	task = MultiThreadTask.MultiThreadTask(func=add,thread_num=3,params_list=params_list,callback=callback_add)
	task.start()

	# A case with parameters. WARN: Every element in paramerter list must be iterable. You can use list or tuple. A WRONG case is [1,2], since 1 and 2 is not iterable.
	params_list = [(1,),(2,),(3,),(4,)]
	task = MultiThreadTask.MultiThreadTask(func=display_info,thread_num=3,params_list=params_list)
	task.start()

	# A case without parameter, task_num means how many times do you want to run).
	task = MultiThreadTask.MultiThreadTask(func=print_i_want_to_sleep, thread_num=4, no_params=True,task_num=6)
	task.start()

	# A case without parameters, work endlessly(task_number = -1 means endless work).
	task = MultiThreadTask.MultiThreadTask(func=print_i_need_money, thread_num=4, no_params=True,task_num=-1)
	task.start()
