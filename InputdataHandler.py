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
def execute(keyword,index_num,authorization,x_guest_token):
    try:
        command = "python ScrapingEngine.py --keyword '%s' --index_num '%s' --authorization '%s' --x_guest_token '%s'"%(keyword,index_num,authorization,x_guest_token)
        print(command)
        os.system(command)
    except Exception as ex:
        print(ex)



if __name__ == '__main__':
    start=time.time()
    numOflan = 2
    with open('list.txt', 'r') as f:
        keyword_list = f.read().split(',')

    for keyword in (keyword_list):
        # Creating the tuple of all the processes
        index_num = []
        for index in range(0,numOflan+1):
            index_num.append(index)

        x_guest_token, authorization = get_brwoser()

        process_pool = multiprocessing.Pool(processes = numOflan)
        process_pool.starmap(execute, zip(repeat(keyword),index_num,repeat(authorization),repeat(x_guest_token)))

print("-------%s seconds -----"%(time.time()-start))
