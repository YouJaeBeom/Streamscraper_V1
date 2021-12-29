import multiprocessing
import os
import time
from itertools import repeat



# This block of code enables us to call the script from command line.
def execute(process,x_guest_token,authorization):
    try:
        command = "scrapy crawl_many -q '%s' -x '%s' -a '%s' -p %s -m %s"%("bts",str(x_guest_token),str(authorization),str(process),str(1))
        print(command)
        os.system(command)
    except Exception as ex:
        print(command)
        print(ex)



if __name__ == '__main__':
    start=time.time()

    # Creating the tuple of all the processes
    all_processes = []
    for ps in range(0,33):
        all_processes.append(ps)

    x_guest_token, authorization = get_brwoser()

    process_pool = multiprocessing.Pool(processes = 32)
    process_pool.starmap(execute, zip(all_processes,repeat(x_guest_token),repeat(authorization)))

print("-------%s seconds -----"%(time.time()-start))
