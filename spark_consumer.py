from kafka import KafkaConsumer
import json
import datetime
import sys
import pandas as pd
import os
import ast
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


x = 0
timestamp=[]
numberOftweet=[]
server_list = ['117.17.189.205:9092','117.17.189.205:9093','117.17.189.205:9094']
id_list=[]

#topic="bts"

topic="result_minsun"
total_id_list=[]
total_text_list=[]
consumer = KafkaConsumer(topic,bootstrap_servers = server_list, auto_offset_reset = 'latest')
try:
    print("Start",topic)
    for message in consumer:
        timestamp.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        tweet=str(message.value)
        tweet= json.loads(ast.literal_eval(json.dumps(tweet)))
        tweet_id = tweet['id_str']
        tweet_text = tweet['full_text'].encode('utf8')
        created_at=tweet['created_at']


        x=x+1
        numberOftweet.append(x)
        total_id_list.append(tweet_id)
        total_text_list.append(tweet_text)

        print("%s ===== %s ============ %s // %s"%(datetime.datetime.now(),  (x), created_at, tweet_id))



except Exception as e:
    print(e)
finally:
    result=pd.DataFrame(zip(timestamp,numberOftweet,total_text_list,total_id_list),columns=['timestamp','numberOftweet','total_text_list','total_id_list'])
    print("result",result)
    file_name = "Streamscraper_"+"minsun"+".csv"
    result.to_csv(file_name)
    sys.exit()
