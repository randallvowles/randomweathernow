#!/usr/bin/env python

# Created by Randall Vowles, API token and twitter account belong to me
import configparser
import random
import time
import sys
import tweepy
import requests
import simplejson
config = configparser.ConfigParser()
config.read(r'rwnconfig.txt')
CONSUMER_KEY = config.get('randomweatherbot', 'CONSUMER_KEY')
CONSUMER_SECRET = config.get('randomweatherbot', 'CONSUMER_SECRET')
ACCESS_TOKEN = config.get('randomweatherbot', 'ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config.get('randomweatherbot', 'ACCESS_TOKEN_SECRET')
token = config.get('randomweatherbot', 'token')
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(AUTH)
parameters = '&token='+token+'&status=active&' + \
            'units=english&obtimezone=local&qc=all&vars=air_temp&recent=60'
baseURL = 'http://api.mesowest.net/v2/stations/'
# blacklist=[134, 203, 192, 92, 106, 48, 77, 126, 211, 197, 146, 196,
# 131, 23, 72, 208, 169, 80, 65]
good_networks = [1, 2, 3, 4, 5, 8, 11, 13, 15, 16, 17, 22, 25, 26, 29, 36, 39,
                 41, 45, 49, 54, 55, 56, 57, 59, 60, 62, 63, 66, 70, 82, 83,
                 84, 85, 88, 89, 90, 91, 93, 97, 98, 99, 100, 101, 102, 103,
                 104, 105, 107, 109, 110, 118, 119, 123, 125, 132, 136, 137,
                 139, 143, 150, 151, 153, 158, 160, 162, 170, 182, 183, 187,
                 188, 191, 194, 195, 199, 201, 206, 207, 208, 209, 212, 213]
network_id = random.choice(good_networks)
sq = requests.get(baseURL+'metadata?'+parameters+'&network='+str(network_id))
sq1 = simplejson.loads(sq.content)
random_station = random.choice(sq1['STATION'])
stid = random_station['STID']
# print(stid)
wq = requests.get(baseURL + 'timeseries?' + parameters + '&stid=' + stid)
wq1 = simplejson.loads(wq.content)
while wq1['SUMMARY']['NUMBER_OF_OBJECTS'] == 0:
    random_station = random.choice(sq1['STATION'])
    stid = random_station['STID']
    # print(stid)
    wq = requests.get(baseURL+'timeseries?'+parameters+'&stid='+stid)
    wq1 = simplejson.loads(wq.content)
    try:
        wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
    except (KeyError, IndexError, TypeError) or \
            wq1['QC_SUMMARY']['TOTAL_OBSERVATIONS_FLAGGED'] > 0 or \
            wqtemp < -50 or wqtemp > 150:
        random_station = random.choice(sq1['STATION'])
        stid = random_station['STID']
        # print(STID)
        wq = requests.get(baseURL+'timeseries?'+parameters+'&stid='+stid)
        wq1 = simplejson.loads(wq.content)
        # wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
        try:
            wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
        except (KeyError, IndexError, TypeError) or \
                wq1['QC_SUMMARY']['TOTAL_OBSERVATIONS_FLAGGED'] > 0 or \
                wqtemp < -50 or wqtemp > 150:
            random_station = random.choice(sq1['STATION'])
            stid = random_station['STID']
            # print(STID)
            wq = requests.get(baseURL+'timeseries?'+parameters+'&stid='+stid)
            wq1 = simplejson.loads(wq.content)
            # wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
            try:
                wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
            except (KeyError, IndexError, TypeError) or \
                    wq1['QC_SUMMARY']['TOTAL_OBSERVATIONS_FLAGGED'] > 0 or \
                    wqtemp < -50 or wqtemp > 150:
                random_station = random.choice(sq1['STATION'])
                stid = random_station['STID']
                # print(STID)
                wq = requests.get(baseURL+'timeseries?'+parameters+'&stid='+stid)
                wq1 = simplejson.loads(wq.content)
                wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
else:
    wqtemp = round(wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0], 1)
    wqtemp1 = str(wqtemp)+u'\N{DEGREE SIGN}'+'F'
wq1sn = wq1['STATION'][0]['NAME']
wq1st = wq1['STATION'][0]['STATE']
wqresult = 'The current weather at ' + wq1sn + ', '+wq1st+' is ' + wqtemp1
print(wqresult)
#api.update_status(wqresult)
#time.sleep(300)
all_states = ['al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga',
              'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md',
              'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj',
              'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc',
              'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy', 'dc']
random_state = random.choice(all_states)
r = requests.get(baseURL + 'timeseries?&state=' + random_state + parameters)
r1 = simplejson.loads(r.content)
r2 = []
for i in range(len(r1['STATION'])):
    if int(r1['STATION'][i]['MNET_ID']) in good_networks:
        r2.append(r1['STATION'][i])
max_t = []
for j in range(len(r2)):
    if r2[j]['QC_FLAGGED'] is False:
        max_t.append(r2[j]['OBSERVATIONS']['air_temp_set_1'][0])
    mt = max(max_t)
    mi = (max_t).index(mt)
mt_t = round(mt, 1)
m_name = r2[mi]['NAME']
m_stid = r2[mi]['STID']
m_st = r2[mi]['STATE']
mtresult = 'The current high temperature in the state of '+m_st+', is ' + \
            str(mt_t) + u'\N{DEGREE SIGN}' + 'F at ' + m_name
print(mtresult)
#api.update_status(mtresult)
#time.sleep(300)
random_state2 = random.choice(all_states)
s = requests.get(baseURL + 'timeseries?&state=' + random_state2 + parameters)
s1 = simplejson.loads(s.content)
s2 = []
for i in range(len(s1['STATION'])):
    if int(s1['STATION'][i]['MNET_ID']) in good_networks:
        s2.append(s1['STATION'][i])
min_t = []
for j in range(len(s2)):
    if s2[j]['QC_FLAGGED'] is False:
        min_t.append(s2[j]['OBSERVATIONS']['air_temp_set_1'][0])
    mt2 = min(min_t)
    mi2 = (min_t).index(mt2)
mt2_t = round(mt2, 1)
m2_name = s2[mi2]['NAME']
m2_stid = s2[mi2]['STID']
m2_st = s2[mi2]['STATE']
mt2result = 'The current low temperature in the state of ' + m2_st + ', is ' +\
             str(mt2_t)+u'\N{DEGREE SIGN}'+'F at '+m2_name
print(mt2result)
#api.update_status(mt2result)
#sys.exit()
