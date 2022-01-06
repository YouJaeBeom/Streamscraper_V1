import multiprocessing
import os
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from seletools.actions import drag_and_drop
from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.firefox.options import Options
from itertools import repeat

def get_brwoser():
    """
    Get Cookie, Authorization through Firefox browser
    """
    print("Get Cookie, Authorization through Firefox browser")
    ## drowser setting
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(firefox_profile=get_profile(), options=options)

    ## brwoser execute
    url = "https://twitter.com/search?q=bts&src=typed_query&f=live"
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    ## get Cookie, Authorization
    for request in driver.requests:
        ## get token, authorization values
        Cookie = str(request.headers['Cookie']).replace(" ","").split(";")
        try:
            x_guest_token = [x_guest_token for x_guest_token in Cookie if "gt=" in x_guest_token][0]
            x_guest_token =  x_guest_token.replace("gt=","")
            authorization = request.headers['authorization']
        except :
            continue
        if x_guest_token != None and authorization != None:
            break


    ## browser close
    driver.close()
    driver.quit()

    return x_guest_token, authorization


def get_profile():
    """
    Firefox browser settings
    """
    print("Firefox browser settings")
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.privatebrowsing.autostart", True)


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
