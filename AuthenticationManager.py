from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from seletools.actions import drag_and_drop
from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.firefox.options import Options
from itertools import repeat
import time

#class AuthenticationManager:

def get_profile():
    """
    Firefox browser settings
    """
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.privatebrowsing.autostart", True)

def get_brwoser(keyword,process_number):
    """
    Get Cookie, Authorization through Firefox browser
    """
    
    ## drowser setting
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(firefox_profile=get_profile(), options=options)

    ## brwoser execute
    url = "https://twitter.com/search?q="+keyword+"&src=typed_query&f=live"
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    ## get Cookie, Authorization
    for request in driver.requests:
        ## get token, authorization values
        Cookie = str(request.headers['Cookie']).replace(" ","").split(";")
        Headers = request.headers
        try:
            x_guest_token = [x_guest_token for x_guest_token in Cookie if "gt=" in x_guest_token][0]
            x_guest_token =  str(x_guest_token.replace("gt=",""))
            authorization = str(Headers['authorization'])    
            if x_guest_token != None and authorization != None :
                ## browser close
                driver.close()
                driver.quit()
                return x_guest_token, authorization
        except :
            pass
    
    driver.close()
    driver.quit()
    return None, None
