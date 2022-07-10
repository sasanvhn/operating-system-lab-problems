import multiprocessing 

lst = [1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,0, -1, 22, 1000]

def calculate_sum(out_list, q):
    my_sum = sum(out_list)
    q.put(my_sum)

if __name__ == "__main__":

    processes = []

    q = multiprocessing.Queue()

    # slicing the list into 3 lists and make a process for each
    process_1 = multiprocessing.Process(target=calculate_sum, args= (lst[0 : (len(lst)//3)], q,))
    process_2 = multiprocessing.Process(target=calculate_sum, args= (lst[len(lst)//3 : (len(lst) - len(lst)//3)], q,))
    process_3 = multiprocessing.Process(target=calculate_sum, args= ((lst[len(lst)-(len(lst)//3) : len(lst)], q,)))

    processes.append(process_1)
    processes.append(process_2)
    processes.append(process_3)

    for process in processes:
        process.start()

    total = q.get() + q.get() + q.get()

    for process in processes:
        process.join()

    print(total)
    print(sum(lst))