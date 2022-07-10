import threading
import random
 
def generateRandomSupplierIngredients(): # The supplier randomly generates two ingredient and place them on the table
    ingredient1 = random.randint(1,100)
    ingredient2 = random.randint(1,100)
    ingredient1 %= 3
    ingredient2 %= 3
    if (ingredient1 == ingredient2):
        ingredient2 += 1
        ingredient2 %= 3
    ingredientList = [ingredient1, ingredient2]
    return ingredientList

class smoker:
    def __init__(self, rounds):
        self.condMutex = threading.Condition()

        self.rounds = rounds

        self.ingredients = ['tobacco', 'paper', 'match']
        self.availableItems = [False, False, False] # at first there is no item on the table

        self.smokerThreads = [] # we gonna make a thread for each of the 3 smokers and add them to this list
        self.terminate = False # if a smoker is done smoking, set the terminate boolean to true

        # Each of smokers has only one item with infinite supply
        self.smokerThreads.append(threading.Thread(target=self.smokerNeed, args=(1, 2))) 
        self.smokerThreads.append(threading.Thread(target=self.smokerNeed, args=(0, 2)))
        self.smokerThreads.append(threading.Thread(target=self.smokerNeed, args=(0, 1)))
                                  
        for smokers in self.smokerThreads:
            smokers.start()
        # create vendor thread
        self.vendorThread = threading.Thread(target=self.vendorRoutine)
        self.vendorThread.start()
 
    def vendorRoutine(self):
        for i in range(self.rounds):
            # Generate two random items for supplier
            randomIngredients = generateRandomSupplierIngredients()
            self.condMutex.acquire()

            # make items available on table.
            self.availableItems[randomIngredients[0]] = True
            self.availableItems[randomIngredients[1]] = True
            
            # notify to all smokers that items are made available on table
            self.condMutex.notify_all()
            self.condMutex.release()
 
    def smokerNeed(self, neededItem1, neededItem2): # each smoker needs two remaining ingredients to make a cigars 
        myName = threading.currentThread().getName()
        while (True):
            self.condMutex.acquire()

            # do nothing untill the needed items are on table
            while (False == self.availableItems[neededItem1] or
                   False == self.availableItems[neededItem2]):
                self.condMutex.wait()
            self.condMutex.release()

            # check if the smoker is done
            if (True == self.terminate):
                break

            # remove the supplier generated items from the table
            self.availableItems[neededItem1] = False
            self.availableItems[neededItem2] = False
 
    def waitTillDone(self):
        # wait for vendor thread to end
        self.vendorThread.join()

        # send terminate signal to smoker threads
        self.condMutex.acquire()

        # its done
        self.terminate = True
        self.availableItems = [True, True, True]

        self.condMutex.notify_all()
        self.condMutex.release()
 
if __name__== "__main__":
    obj = smoker(3)
    obj.waitTillDone()