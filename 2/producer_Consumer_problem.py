
from multiprocessing import Semaphore
import threading
import time
import random

buffer_size = 5
full_semaphore = Semaphore(0)
empty_semaphore = Semaphore(buffer_size)
mutex_semaphore = Semaphore(1)

def producer(items):
    i = 0
    while True:
        task = random.randint(0, 10) # producing items

        empty_semaphore.acquire()
        mutex_semaphore.acquire()

        items.append(task) # adding the produced item to buffer
        i = i + 1

        mutex_semaphore.release()
        full_semaphore.release()

        if i == buffer_size:
            break


def consumer(items):
    while True:
        if items: # if there is work to do

            full_semaphore.acquire()
            mutex_semaphore.acquire()

            items.pop(0)

            mutex_semaphore.release()
            empty_semaphore.release()

            if len(items) == 0: # consume
                break




    
items = []
producer = threading.Thread(target = producer, args=(items,))
consumer = threading.Thread(target = consumer, args=(items,))

producer.start()
consumer.start()
