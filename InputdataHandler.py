import multiprocessing
import os
import time
from itertools import repeat

import AuthenticationManager


# This block of code enables us to call the script from command line.
def execute(query,process_number,x_guest_token):
    try:
        command = "python ScrapingEngine.py --query '%s' --process_number '%s'  --x_guest_token '%s' "%(query, process_number, x_guest_token)
        print(command)
        os.system(command)
    except Exception as ex:
        pass



if __name__ == '__main__':
    start=time.time()
    
    with open('list.txt', 'r') as f:
        query_list = f.read().split(',')
    
    with open('language_list.txt', 'r') as f:
        language_list = f.read().split(',')
    
    num_of_process = len(language_list)
    
    num_of_process_list = []
    for index in range(0,num_of_process):
        num_of_process_list.append(index)
    x=0
    for query in (query_list):
        # Creating the tuple of all the processes
        x_guest_token = None
        while True:
            x_guest_token  = AuthenticationManager.get_brwoser(query)
            if x_guest_token != None:
                break
        x=x+1
        process_pool = multiprocessing.Pool(processes = num_of_process)
        process_pool.starmap(execute, zip(repeat(query), num_of_process_list, repeat(x_guest_token) ))

print("-------%s seconds -----"%(time.time()-start))
