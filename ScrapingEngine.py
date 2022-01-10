import argparse 
import requests
import json
import logging
# 로그 생성
logger = logging.getLogger()

# 로그의 출력 기준 설정
logger.setLevel(logging.CRITICAL)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(message)s')

# log를 파일에 출력
file_handler = logging.FileHandler('log.txt')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

import time
from datetime import datetime
from datetime import timedelta

## set kafka
from kafka import KafkaProducer

## selenium import setting
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options

class ScrapingEngine(object):
    def __init__(self, keyword, index_num, authorization, x_guest_token):
        self.keyword = keyword
        self.index_num = index_num

        ## Setting Language type
        self.language_types =["en","ja","ko","ar","bn","cs","da","de","el","es","fa","fi","fil","he","hi","hu","id","it","msa","nl","no","pl","pt","ro","ru","sv","th","tr","uk","ur","vi","zh-cn","zh-tw"]
        self.accept_language = self.language_types[int(self.index_num)]
        self.x_twitter_client_language = self.language_types[int(self.index_num)]

        ## Setting authorization keysets
        self.authorization = authorization
        self.x_guest_token = x_guest_token 

        ## Setting init  
        self.cursor = None
        self.id_strList =[]
        self.totalcount = 0

        ## Setting base url
        self.base_url = "https://twitter.com/search?q="

        ## Setting kafka
        self.producer = KafkaProducer(acks=0, compression_type='gzip', api_version=(0, 10, 1), bootstrap_servers=['117.17.189.205:9092','117.17.189.205:9093','117.17.189.205:9094'])
    
    def get_profile(self):
        """
        Firefox browser settings
        """
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.privatebrowsing.autostart", True)
        return profile

    def get_brwoser(self):
        """
        Get Cookie, Authorization through Firefox browser
        """
        ## drowser setting
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Firefox(firefox_profile=self.get_profile(), options=self.options)

        ## brwoser execute
        self.driver.get(self.url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        ## get Cookie, Authorization
        for request in self.driver.requests:
            ## get token, authorization values
            Cookie = str(request.headers['Cookie']).replace(" ","").split(";")
            print(self.process_num,"RESET get Cookie, Authorization")
            try:
                self.x_guest_token = [x_guest_token for x_guest_token in Cookie if "gt=" in x_guest_token][0]
                self.x_guest_token =  self.x_guest_token.replace("gt=","")
                self.authorization = request.headers['authorization']
            except :
                continue
            if self.x_guest_token != None and self.authorization != None:
                break

        ## browser close
        self.driver.close()
        self.driver.quit()

    def set_search_url(self):
        self.url = self.base_url + self.keyword +"&src=typed_query&f=live"

        return self.url

    def start_scraping(self):
        ## get URL
        self.url = self.set_search_url()
        
        while (True):
            ## setting header
            self.headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0',
                    'Accept': '*/*',
                    'Accept-Language': self.accept_language,
                    #'Accept-Encoding': 'gzip, deflate, br',
                    'x-guest-token': self.x_guest_token,
                    'x-twitter-client-language': self.x_twitter_client_language,
                    'x-twitter-active-user': 'yes',
                    #'x-csrf-token': 'c931c4b02e64508ab1dd9b61c19c4614',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'authorization': self.authorization,
                    'Referer': self.url,
                    'Connection': 'keep-alive',
                    'TE': 'trailers',
            }
            ## setting parameters
            self.params = (
                    ('include_profile_interstitial_type', '1'),
                    ('include_blocking', '1'),
                    ('include_blocked_by', '1'),
                    ('include_followed_by', '1'),
                    ('include_want_retweets', '1'),
                    ('include_mute_edge', '1'),
                    ('include_can_dm', '1'),
                    ('include_can_media_tag', '1'),
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
                    ('send_error_codes', 'true'),
                    ('simple_quoted_tweet', 'true'),
                    ('q', self.keyword+" -is:retweet"),
                    ('tweet_search_mode', 'live'),
                    ('count', '40'),
                    ('query_source', 'typed_query'),
                    ('pc', '1'),
                    ('spelling_corrections', '1'),
                    ('ext', 'mediaStats,highlightedLabel'),
                    ('cursor', self.cursor ), ## next cursor range
            )
            
            try:
                ## call API with header, parameters
                self.response = requests.get(
                        'https://twitter.com/i/api/2/search/adaptive.json', 
                        headers=self.headers,
                        params=self.params
                        )
                
                self.response_json = self.response.json()
            except Exception as ex:
                ## If API is restricted, request to change Cookie and Authorization again
                print("If API is restricted, request to change Cookie and Authorization again")
                self.get_brwoser()
                continue

            if str(self.response.status_code) != "200":
                ## If API is restricted, request to change Cookie and Authorization again
                print(" Response status code was not 200")
                self.get_brwoser()
                continue

            else :
                self.tweets = self.response_json['globalObjects']['tweets']
                try :
                    ## get current cur range
                    self.cursor = str(self.response_json['timeline']['instructions'][len(self.response_json['timeline']['instructions'])-1]['replaceEntry']['entry']['content']['operation']['cursor']['value'] )
                except :
                    ## get current cur range
                    self.cursor = str(self.response_json['timeline']['instructions'][0]['addEntries']['entries'][len(self.response_json['timeline']['instructions'][0]['addEntries']['entries'])-1]['content']['operation']['cursor']['value'])

            try:
                #print("self.parse_tweets",self.tweets.values())
                self.parse_tweets(self.tweets.values())
            except Exception as es:
                print(es)


    def parse_tweets(self,tweets):
        """
        Parse tweets and store them in item
        Tweet object description : https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
        Entities object description : https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/entities
        Extended entities object description : https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/extended-entities
        Geo object description : https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/geo
        """
        self.tweetcount = 0
        self.dup_count = 0

        ## tweets to tweet
        for tweet in tweets:
            ## overlap tweet
            if tweet['id_str'] in self.id_strList:
                self.dup_count = self.dup_count + 1
                continue
            # No overlap tweet
            else :
                self.id_strList.append(tweet['id_str'])
                self.tweetcount = self.tweetcount + 1
                print(tweet['created_at'], tweet['full_text'])
                try:
                    self.producer.send(self.keyword, json.dumps(tweet).encode('utf-8'))
                    self.producer.flush()
                except Exception as ex:
                    print("ex",ex)

        if len(self.id_strList) < 30:
            self.cursor = None
            
        if self.dup_count == len(tweets):
            pass

        elif self.dup_count != len(tweets):
            self.cursor = None 
        
        self.totalcount = self.totalcount + self.tweetcount

        now = datetime.now()
        result_print = "|index_num={0:<10}|keyword={1:<20}|tweet_count={2:<10}|cursor={3:<10}".format(
                self.index_num, 
                self.keyword, 
                self.totalcount,
                str(self.cursor)
                )
        #print(result_print)
        logger.critical(result_print)


if(__name__ == '__main__') :
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword",help="add keyword")
    parser.add_argument("--index_num", help="add index number max(32)")
    parser.add_argument("--authorization", help="add init authorization")
    parser.add_argument("--x_guest_token", help="add init x_guest_token")
    args = parser.parse_args()
    
    streamscraper = ScrapingEngine(args.keyword, args.index_num, args.authorization, args.x_guest_token)
    streamscraper.start_scraping()

