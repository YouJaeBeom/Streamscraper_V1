import requests
import json
from selenium.webdriver.firefox.options import Options
from seleniumwire import webdriver  # Import from seleniumwire
import time
import sys
import locale

print(sys.getfilesystemencoding())
print(locale.getpreferredencoding())

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


x_guest_token, authorization = get_brwoser()

cookies = {
    '_ga': 'GA1.2.309298685.1621573027',
    'mbox': 'PC#d9b42ea86b3f4561b9a3be0590223119.32_0#1701605186|session#6d943409d4494f1d9dd61be40077ba54#1638362245',
    'des_opt_in': 'Y',
    'guest_id_marketing': 'v1%3A162157302558987660',
    'guest_id_ads': 'v1%3A162157302558987660',
    'g_state': '{"i_l":0}',
    'kdt': '6D0x98oNJXzoWvmpDambOjWmHcgM0L3miIv0qrnw',
    '_ga_34PHSZMC42': 'GS1.1.1638360388.1.0.1638360395.0',
    '_gcl_au': '1.1.606822019.1638360390',
    'dnt': '1',
    'personalization_id': 'v1_TDhNn6tGwjVgYTEAuzCrSQ==',
    'guest_id': 'v1%3A164119422707154236',
    'ct0': '586f9ad33da376326e3614d91b0e1056acb03e4504b384b573e1f09a8738a9a5b50f23cf3b7689a20af6d3b7343ddde09f6d1fb7b86781561a3a197ad8084c0cc79bf2409084d9b25a49e46ea71063bb',
    '_gid': 'GA1.2.1863410217.1641444071',
    'gt': '1478949743648997378',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Accept': '*/*',
    'Accept-Language': 'en',
    #'Accept-Encoding': 'gzip, deflate, br',
    'x-guest-token': x_guest_token,
    'x-twitter-client-language': 'en',
    'x-twitter-active-user': 'yes',
    'x-csrf-token': 'c931c4b02e64508ab1dd9b61c19c4614',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'authorization': authorization,
    'Referer': 'https://twitter.com/search?q=bts&src=typed_query&f=live',
    'Connection': 'keep-alive',
    'TE': 'trailers',
}

params = (
    ('include_profile_interstitial_type', '1'),
    ('include_blocking', '1'),
    ('include_blocked_by', '1'),
    ('include_followed_by', '1'),
    ('include_want_retweets', '1'),
    ('include_mute_edge', '1'),
    ('include_can_dm', '1'),
    ('include_can_media_tag', '1'),
    ('include_ext_has_nft_avatar', '1'),
    ('skip_status', '1'),
    ('cards_platform', 'Web-12'),
    ('include_cards', '1'),
    ('include_ext_alt_text', 'true'),
    ('include_quote_count', 'true'),
    ('include_reply_count', '1'),
    ('tweet_mode', 'extended'),
    ('include_entities', 'true'),
    ('include_user_entities', 'true'),
    ('include_ext_media_color', 'true'),
    ('include_ext_media_availability', 'true'),
    ('include_ext_sensitive_media_warning', 'true'),
    ('send_error_codes', 'true'),
    ('simple_quoted_tweet', 'true'),
    ('q', 'bts'),
    ('tweet_search_mode', 'live'),
    ('count', '40'),
    ('query_source', 'typed_query'),
    #('cursor', 'refresh:thGAVUV0VFVBaIgLKVnLqkhikWgMDTib27pIYpEnEV3IV6FYCJehgEVVNFUjUBFQAVAAA='),
    ('pc', '1'),
    ('spelling_corrections', '1'),
    ('ext', 'mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,superFollowMetadata'),
)

response = requests.get('https://twitter.com/i/api/2/search/adaptive.json', headers=headers, params=params, cookies=cookies)

print("response",response.text)

#response_json = json.dumps(response.json(), indent=4, sort_keys=True, ensure_ascii=False)

#print("self.response_json",response_json)
