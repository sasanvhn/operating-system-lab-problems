import threading
import time

class ReaderWriter():
    def __init__(self):
        
        self.reader = threading.Semaphore()                                  
        self.writer = threading.Semaphore()  
        self.readCount = 0   # readCount presemts number of current readers

    def reader(self):

        while True:

            self.reader.acquire()

            self.readCount += 1       # increase count for reader by 1

            if self.readCount == 1:
                self.writer.acquire()

            self.reader.release()

            self.reader.acquire()
            self.readCount -= 1   # reading is done

            if self.readCount == 0:
                self.writer.release() 

            self.reader.release()

            time.sleep(2)          

    def writer(self):

        while True:

            self.writer.acquire()

             # writing the data

            self.writer.release()      #sinal on write semaphore

            time.sleep(2)    


readerWriter = ReaderWriter()

threads = []

threads.append(threading.Thread(target = readerWriter.reader))
threads.append(threading.Thread(target = readerWriter.writer))
threads.append(threading.Thread(target = readerWriter.reader))
threads.append(threading.Thread(target = readerWriter.reader))
threads.append(threading.Thread(target = readerWriter.writer))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join