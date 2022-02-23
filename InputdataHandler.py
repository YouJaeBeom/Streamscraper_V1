import multiprocessing
import os
import time
from itertools import repeat

import AuthenticationManager


# This block of code enables us to call the script from command line.
def execute(keyword,index_num,x_guest_token, authorization, x_csrf_token):
    try:
        command = "python ScrapingEngine.py --keyword '%s' --index_num '%s'  --x_guest_token '%s' --authorization '%s' --x_csrf_token '%s' "%(keyword, index_num, x_guest_token, authorization, x_csrf_token)
        print(command)
        os.system(command)
    except Exception as ex:
        print(ex)



if __name__ == '__main__':
    start=time.time()
    numOflan = 1
    with open('list.txt', 'r') as f:
        keyword_list = f.read().split(',')

    for keyword in (keyword_list):
        # Creating the tuple of all the processes
        index_num = []
        for index in range(0,numOflan+1):
            index_num.append(index)

        x_guest_token, authorization, x_csrf_token = AuthenticationManager.get_brwoser(keyword)

        process_pool = multiprocessing.Pool(processes = numOflan)
        process_pool.starmap(execute, zip(repeat(keyword), index_num, repeat(x_guest_token) ,  repeat(authorization), repeat(x_csrf_token) ))

print("-------%s seconds -----"%(time.time()-start))
