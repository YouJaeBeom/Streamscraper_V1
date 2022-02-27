import multiprocessing
import os
import time
from itertools import repeat

import AuthenticationManager


# This block of code enables us to call the script from command line.
def execute(keyword,process_number,x_guest_token, authorization, x_csrf_token):
    try:
        command = "python ScrapingEngine.py --keyword '%s' --process_number '%s'  --x_guest_token '%s' --authorization '%s' --x_csrf_token '%s' "%(keyword, process_number, x_guest_token, authorization, x_csrf_token)
        print(command)
        os.system(command)
    except Exception as ex:
        print(ex)



if __name__ == '__main__':
    start=time.time()
    
    with open('list.txt', 'r') as f:
        keyword_list = f.read().split(',')
    
    with open('language_list.txt', 'r') as f:
        language_list = f.read().split(',')
    
    print(len(keyword_list))
    print(len(language_list))
    num_of_process = len(language_list)
    
    num_of_process_list = []
    for index in range(0,num_of_process+1):
        num_of_process_list.append(index)
    
    for keyword in (keyword_list):
        # Creating the tuple of all the processes
        x_guest_token, authorization, x_csrf_token = AuthenticationManager.get_brwoser(keyword)

        process_pool = multiprocessing.Pool(processes = num_of_process)
        process_pool.starmap(execute, zip(repeat(keyword), num_of_process_list, repeat(x_guest_token) ,  repeat(authorization), repeat(x_csrf_token) ))

print("-------%s seconds -----"%(time.time()-start))
