import multiprocessing
import os
import time
from itertools import repeat

import AuthenticationManager


# This block of code enables us to call the script from command line.
def execute(keyword,process_number,x_guest_token, authorization):
    try:
        command = "python ScrapingEngine.py --keyword '%s' --process_number '%s'  --x_guest_token '%s' --authorization '%s' "%(keyword, process_number, x_guest_token, authorization)
        print(command)
        os.system(command)
    except Exception as ex:
        pass



if __name__ == '__main__':
    start=time.time()
    
    with open('list.txt', 'r') as f:
        keyword_list = f.read().split(',')
    
    with open('language_list.txt', 'r') as f:
        language_list = f.read().split(',')
    
    num_of_process = len(language_list)
    
    num_of_process_list = []
    for index in range(0,num_of_process):
        num_of_process_list.append(index)
    x=0
    for keyword in (keyword_list):
        # Creating the tuple of all the processes
        x_guest_token = None
        authorization = None
        while True:
            x_guest_token, authorization  = AuthenticationManager.get_brwoser(keyword,int(num_of_process_list[x]))
            if x_guest_token != None and authorization != None:
                break
        x=x+1
        process_pool = multiprocessing.Pool(processes = num_of_process)
        process_pool.starmap(execute, zip(repeat(keyword), num_of_process_list, repeat(x_guest_token) ,  repeat(authorization) ))

print("-------%s seconds -----"%(time.time()-start))
