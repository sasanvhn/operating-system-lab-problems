import threading
import os

lst = [1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,0, -1, 22, 1000]

global sum1
sum1 = 0

def calculate_sum(the_list, i, j, q):
    global sum1
    sum_of_list = 0

    for z in range(i, min(j,len(lst))):
        sum_of_list += the_list[z]

    if (j + len(lst)%os.cpu_count() == len(lst)): # for when the list size is odd and we wanna sum the last element
        for s in range(j, len(lst)):
            sum_of_list += the_list[s]

    #print ("sum: ", sum_of_list)
    sum1 += sum_of_list
    


threads = []

for cores in range(os.cpu_count()):
    core_count = os.cpu_count()

    sublist_size = len(lst) // os.cpu_count()
    start_index = cores*sublist_size

    x = threading.Thread(target=calculate_sum, args=(lst, start_index, (start_index + sublist_size),))
    threads.append(x)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(sum1)
print(sum(lst))