#!/usr/bin/env python

#Created by Randall Vowles, API token= belongs to me
#Twitter account also belongs to me

import random
import time
import sys
import tweepy
import requests
import simplejson
CONSUMER_KEY = 
CONSUMER_SECRET = 
ACCESS_TOKEN = 
ACCESS_TOKEN_SECRET = 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(AUTH)
APITOKEN = '&token=********************&status=active&' + \
            'units=english&obtimezone=local&qc=all&vars=air_temp&recent=60'
BASEURL = 'http://api.mesowest.net/v2/stations/'
# blacklist=[134, 203, 192, 92, 106, 48, 77, 126, 211, 197, 146, 196,
# 131, 23, 72, 208, 169, 80, 65]
GOOD_NETWORKS = [1, 2, 3, 4, 5, 8, 11, 13, 15, 16, 17, 22, 25, 26, 29, 36, 39,
                 41, 45, 49, 54, 55, 56, 57, 59, 60, 62, 63, 66, 70, 82, 83,
                 84, 85, 88, 89, 90, 91, 93, 97, 98, 99, 100, 101, 102, 103,
                 104, 105, 107, 109, 110, 118, 119, 123, 125, 132, 136, 137,
                 143, 150, 151, 153, 158, 160, 162, 169, 170, 182, 183, 187,
                 188, 191, 194, 195, 199, 200, 201, 206, 207, 208, 209, 212,
                 213, 139]
NETWORK_ID = random.choice(GOOD_NETWORKS)
SQ = requests.get(BASEURL+'metadata?'+APITOKEN+'&network='+str(NETWORK_ID))
SQ1 = simplejson.loads(SQ.content)
RANDOM_STATION = random.choice(SQ1['STATION'])
STID = RANDOM_STATION['STID']
# print(STID)
WQ = requests.get(BASEURL + 'timeseries?' + APITOKEN + '&stid=' + STID)
WQ1 = simplejson.loads(WQ.content)
while WQ1['SUMMARY']['NUMBER_OF_OBJECTS'] == 0:
    RANDOM_STATION = random.choice(SQ1['STATION'])
    STID = RANDOM_STATION['STID']
    # print(STID)
    WQ = requests.get(BASEURL+'timeseries?'+APITOKEN+'&stid='+STID)
    WQ1 = simplejson.loads(WQ.content)
    try:
        WQTEMP = WQ1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
    except (KeyError, IndexError, TypeError) or \
            WQ1['QC_SUMMARY']['TOTAL_OBSERVATIONS_FLAGGED'] > 0:
        RANDOM_STATION = random.choice(SQ1['STATION'])
        STID = RANDOM_STATION['STID']
        # print(STID)
        WQ = requests.get(BASEURL+'timeseries?'+APITOKEN+'&stid='+STID)
        WQ1 = simplejson.loads(WQ.content)
        # WQTEMP = WQ1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
        try:
            WQTEMP = WQ1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
        except (KeyError, IndexError, TypeError) or \
                WQ1['QC_SUMMARY']['TOTAL_OBSERVATIONS_FLAGGED'] > 0:
            RANDOM_STATION = random.choice(SQ1['STATION'])
            STID = RANDOM_STATION['STID']
            # print(STID)
            WQ = requests.get(BASEURL+'timeseries?'+APITOKEN+'&stid='+STID)
            WQ1 = simplejson.loads(WQ.content)
            # WQTEMP = WQ1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
            try:
                WQTEMP = WQ1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
            except (KeyError, IndexError, TypeError) or \
                    WQ1['QC_SUMMARY']['TOTAL_OBSERVATIONS_FLAGGED'] > 0:
                RANDOM_STATION = random.choice(SQ1['STATION'])
                STID = RANDOM_STATION['STID']
                # print(STID)
                WQ = requests.get(BASEURL+'timeseries?'+APITOKEN+'&stid='+STID)
                WQ1 = simplejson.loads(WQ.content)
                WQ = WQ1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
WQTEMP1 = str(WQTEMP)+u'\N{DEGREE SIGN}'+'F'
WQ1SN = WQ1['STATION'][0]['NAME']
WQ1ST = WQ1['STATION'][0]['STATE']
WQRESULT = 'The current weather at ' + WQ1SN + ', '+WQ1ST+' is ' + WQTEMP1
# print(WQRESULT)
api.update_status(WQRESULT)
# print('Just tweeted: "' + WQRESULT + '"')
time.sleep(300)
# prints all tweets from twitter account
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#    print (tweet.text)
# sends new tweet for chosen station's temperature, prints tweet to screen
ALL_STATES = ['al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga',
              'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md',
              'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj',
              'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc',
              'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy', 'dc']
RANDOM_STATE = random.choice(ALL_STATES)
R = requests.get(BASEURL + 'timeseries?&state=' + RANDOM_STATE + APITOKEN)
R1 = simplejson.loads(R.content)
R2 = []
for i in range(len(R1['STATION'])):
    if int(R1['STATION'][i]['MNET_ID']) in GOOD_NETWORKS:
        R2.append(R1['STATION'][i])
MAX_T = []
for j in range(len(R2)):
    if R2[j]['QC_FLAGGED'] is False:
        MAX_T.append(R2[j]['OBSERVATIONS']['air_temp_set_1'][0])
    MT = max(MAX_T)
    MI = (MAX_T).index(MT)
M_NAME = R2[MI]['NAME']
M_STID = R2[MI]['STID']
M_ST = R2[MI]['STATE']
MTRESULT = 'The current high temperature in the state of '+M_ST+', is ' + \
            str(MT) + u'\N{DEGREE SIGN}' + 'F at ' + M_NAME
# print(MTRESULT)
api.update_status(MTRESULT)
# print('Just tweeted: "' + mtresult + '"')
time.sleep(300)
RANDOM_STATE2 = random.choice(ALL_STATES)
S = requests.get(BASEURL + 'timeseries?&state=' + RANDOM_STATE2 + APITOKEN)
S1 = simplejson.loads(S.content)
S2 = []
for i in range(len(S1['STATION'])):
    if int(S1['STATION'][i]['MNET_ID']) in GOOD_NETWORKS:
        S2.append(S1['STATION'][i])
MIN_T = []
for j in range(len(S2)):
    if S2[j]['QC_FLAGGED'] is False:
        MIN_T.append(S2[j]['OBSERVATIONS']['air_temp_set_1'][0])
    MT2 = min(MIN_T)
    MI2 = (MIN_T).index(MT2)
M2_NAME = S2[MI2]['NAME']
M2_STID = S2[MI2]['STID']
M2_ST = S2[MI2]['STATE']
MT2RESULT = 'The current low temperature in the state of ' + M2_ST + ', is ' +\
             str(MT2)+u'\N{DEGREE SIGN}'+'F at '+M2_NAME
# print(MT2RESULT)
api.update_status(MT2RESULT)
# print('Just tweeted: "' + mt2result + '"')
sys.exit()
