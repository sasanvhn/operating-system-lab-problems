import threading
import time
sem = threading.Semaphore()

"""
threading.Condition:
acquire()
release()
wait()
wait_for()
notify()
notify_all()
"""

def fun1():
    while True:
        sem.acquire() # When a Thread executes acquire() method then the value of 1 variable will be printed 
        #print(1)
        sem.release() # whenever a Thread executes release() method the thread is done
        time.sleep(0.25)

def fun2():
    while True:
        sem.acquire()
        #print(2)
        sem.release()
        time.sleep(0.25) # we use sleep here so we can also see fun2 and print(2)

t = threading.Thread(target = fun1)
t.start()
t2 = threading.Thread(target = fun2)
t2.start()