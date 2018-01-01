import MultiThreadTask as mtt
import os

def add(x,y):
	print('%s add %s is: %s, and pid is %s'%(x,y,x+y,os.getpid()))

if __name__ == '__main__':
	params_list = [(1,2),(2,3),(3,4),(4,5),(5,6),(7,8)]
	task = mtt.MultiThreadTask(func=add,params_list=params_list,thread_num=1)
	task.start()
