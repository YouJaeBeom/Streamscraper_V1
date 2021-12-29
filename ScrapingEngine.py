class Scraping_Engine:
    def __init__(self,query,lan):
        self.query = query
        self.lan = lan 
        self.base_url = "https://twitter.com/search?q="

    def set_search_url(self):
        if self.min_replies is not None:
            self.query = self.query + "min_replies:"+self.min_replies + " "
        elif self.min_likes is not None:
            self.query = self.query + "min_likes:"+self.min_likes + " "
        elif self.min_retweets is not None:
            self.query = self.query + "min_retweets:"+self.min_retweets + " "
        elif self.place is not None:
            self.query = self.query + "near:"+self.place + " "
        elif self.within is not None:
            self.query = self.query + "within:"+self.within + " "

        self.url = self.base_url + (self.query) +" min_replies:0 min_faves:0 min_retweets:0&src=typed_query&f=live"

        return self.url

    def start_scraping(self):
        ## get URL
        self.url = self.set_search_url()
        
        while (True):
            ## scroll range setting
            #self.cursor = None
            
            ## setting header
            self.headers = {
                    'Accept': '*/*',
                    'Accept-Language': str(self.accept_language),
                    'x-guest-token': str(self.x_guest_token),  # cookies setting
                    'x-twitter-client-language': str(self.x_twitter_client_language) ,
                    'x-twitter-active-user': 'yes',
                    'authorization': str(self.authorization),  ## authorization setting
                    'referer': self.url,  ## base url setting
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
                    ('q', self.query+" -is:retweet"),
                    ('tweet_search_mode', 'live'),
                    ('count', '200'),
                    ('query_source', 'typed_query'),
                    ('pc', '1'),
                    ('spelling_corrections', '1'),
                    ('ext', 'mediaStats,highlightedLabel'),
                    ('cursor', self.cursor ), ## next cursor range
            )
            
            try:
                ## call API with header, parameters
                self.response = requests.get('https://twitter.com/i/api/2/search/adaptive.json', headers=self.headers,
                                             params=self.params)
                #print(self.response.request.headers)
                self.response_json = json.dumps(self.response.json(), indent=4, sort_keys=True, ensure_ascii=False)
                
                #print("self.response_json",self.response_json)
                self.res_json = self.response.json()
                
                ## get tweets information
                self.tweets = res_json['globalObjects']['tweets']
            except Exception as ex:
                ## If API is restricted, request to change Cookie and Authorization again
                print("If API is restricted, request to change Cookie and Authorization again")
                self.get_brwoser()
                continue

            if str(self.response.status_code) != "200":
                ## If API is restricted, request to change Cookie and Authorization again
                print("If API is restricted, request to change Cookie and Authorization again")
                self.get_brwoser()
                continue

            else :
                try :
                    ## get current cur range
                    self.cursor = str(self.res_json['timeline']['instructions'][len(self.res_json['timeline']['instructions'])-1]['replaceEntry']['entry']['content']['operation']['cursor']['value'] )
                except :
                    ## get current cur range
                    self.cursor = str(self.res_json['timeline']['instructions'][0]['addEntries']['entries'][len(self.res_json['timeline']['instructions'][0]['addEntries']['entries'])-1]['content']['operation']['cursor']['value'])


            ## End of collection period for streaming tweet data
            self.now_time = (datetime.now()+ timedelta(days=-1)).strftime('%Y-%m-%d')

            if (self.streaming_end_datetime == self.now_time):
                #print(self.streaming_end_datetime,self.now_time)
                now = datetime.now()
                total_time = now - self.start_time
                result_print = "streaming process|curent_time={0:<10}|process_num={1:<10}|name={2:<10}|total_tweet={3:<10}|streaming quit !!!!!!!!!".format(
                    now.strftime("%Y-%m-%d %H:%M:%S"), self.process_num, self.query, str(self.tweetcount))
                print(result_print)
                logger.critical(result_print)
                break

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

                ## Deepscraper item setting
                tweet = Tweet()

                tweet['tweet_information'] = item


                yield tweet

        self.totalcount = self.totalcount + self.tweetcount

        if len(self.id_strList) < 30:
            print("TO SHROT")
            self.cursor = None

        if self.dup_count >= 2:
            print("REFRESH PAGES",self.totalcount)
            self.cursor = None
        elif self.dup_count < 2:
            print("NEXTPAGE",self.totalcount)


        ## Memory leak protect
        if len(self.id_strList) > 100000:
            del self.id_strList[:50000]

        now = datetime.now()
        result_print = "|curent_time={0:<10}|process_num={1:<10}|name={2:<20}|tweet_count={3:<10}|lan={4:<10},{5:<10}".format(
        now.strftime("%Y-%m-%d %H:%M:%S"), self.process_num, self.query, self.totalcount,str(self.accept_language),str(self.cursor))
        print(result_print)
        logger.critical(result_print)
