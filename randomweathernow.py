#!/uufs/chpc.utah.edu/common/home/u0540701/MyVenv/bin/python

# Created by Randall Vowles, API token and twitter account belong to me
import configparser
import random
import time
import sys
import tweepy
import requests
import numpy
config = configparser.ConfigParser()
config.read(r'./rwnconfig.txt') #/uufs/chpc.utah.edu/common/home/u0540701/randomweathernow
CONSUMER_KEY = config.get('rwn', 'CONSUMER_KEY')
CONSUMER_SECRET = config.get('rwn', 'CONSUMER_SECRET')
ACCESS_TOKEN = config.get('rwn', 'ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = config.get('rwn', 'ACCESS_TOKEN_SECRET')
token = config.get('rwn', 'API_TOKEN')
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
parameters = '&token='+token+'&status=active&' + \
            'units=english&obtimezone=local&vars=air_temp&recent=60&qc=on'
baseURL = 'http://api.mesowest.net/v2/stations/'
# blacklist=[134, 203, 192, 92, 106, 48, 77, 126, 211, 197, 146, 196,
# 131, 23, 72, 208, 169, 80, 65]
good_networks = [1, 2, 3, 4, 5, 8, 11, 13, 15, 16, 17, 22, 25, 26, 29, 36, 39,
                 41, 45, 49, 54, 55, 56, 57, 59, 60, 62, 63, 66, 70, 82, 83,
                 84, 85, 88, 89, 90, 91, 93, 97, 98, 99, 100, 101, 102, 103,
                 104, 105, 107, 109, 110, 118, 119, 125, 132, 136, 137,
                 139, 143, 150, 151, 153, 158, 160, 162, 170, 182, 183, 187,
                 188, 191, 194, 195, 199, 201, 206, 207, 209, 212, 213]
network_id = random.choice(good_networks)
sq = requests.get(baseURL+'metadata?'+parameters+'&network='+str(network_id))
sq1 = sq.json()
random_station = random.choice(sq1['STATION'])
stid = random_station['STID']
# print(stid)
wq = requests.get(baseURL + 'timeseries?' + parameters + '&stid=' + stid)
wq1 = wq.json()
#while wq1['SUMMARY']['NUMBER_OF_OBJECTS'] == 0 or (KeyError, IndexError, TypeError) or \
#            wq1['STATION'][0]['QC']['air_temp_set_1'][-1] == 'true':
#    random_station = random.choice(sq1['STATION'])
#    stid = random_station['STID']
#    # print(stid)
#    wq = requests.get(baseURL+'timeseries?'+parameters+'&stid='+stid)
#    wq1 = simplejson.loads(wq.content)
try:
   wqtem = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][-1]
except (KeyError, IndexError, TypeError) or wqtemp < -50 or wqtemp > 150 or \
       wq1['STATION'][0]['QC']['air_temp_set_1'][-1] == true or \
       wq1['SUMMARY']['NUMBER_OF_OBJECTS'] == 0:
       random_station = random.choice(sq1['STATION'])
       stid = random_station['STID']
       # print(STID)
       wq = requests.get(baseURL+'timeseries?'+parameters+'&stid='+stid)
       wq1 = wq.json()
       # wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
#        try:
#            wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][-1]
#        except (KeyError, IndexError, TypeError) or wqtemp < -50 or wqtemp > 150 \
#                 or wq1['STATION'][0]['QC']['air_temp_set_1'][-1] == true:
#            random_station = random.choice(sq1['STATION'])
#            stid = random_station['STID']
#            # print(STID)
#            wq = requests.get(baseURL+'timeseries?'+parameters+'&stid='+stid)
#            wq1 = simplejson.loads(wq.content)
#            # wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
#            try:
#                wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][-1]
#            except (KeyError, IndexError, TypeError) or \
#                    wq1['STATION'][0]['QC']['air_temp_set_1'][-1] == true or \
#                    wqtemp < -50 or wqtemp > 150:
#                random_station = random.choice(sq1['STATION'])
#                stid = random_station['STID']
#                # print(STID)
#                wq = requests.get(baseURL + 'timeseries?' +
#                                  parameters + '&stid=' + stid)
#                wq1 = simplejson.loads(wq.content)
#                wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][-1]
wqtemp = round(wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][-1], 1)
wqtemp1 = str(wqtemp)+u'\N{DEGREE SIGN}'+'F'
wq1sn = wq1['STATION'][0]['NAME']
wq1st = wq1['STATION'][0]['STATE']
mesolink1 = ' http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=' \
            + stid
wqresult = 'The current weather at ' + wq1sn + ', '+wq1st+' is ' + wqtemp1 \
          + mesolink1
print(wqresult)
api.update_status(wqresult)
# time.sleep(240)
all_states = ['al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga',
              'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md',
              'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj',
              'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc',
              'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy']
random_state = random.choice(all_states)
r = requests.get(baseURL + 'timeseries?&state=' + random_state + parameters + '&network=1,2')
r1 = r.json()
r2 = []
#for i in range(len(r1['STATION'])):
#    if int(r1['STATION'][i]['MNET_ID']) in good_networks:
#        r2.append(r1['STATION'][i])
max_t = []
for j in range(len(r1['STATION'])):
    if r1['STATION'][j]['QC_FLAGGED'] is False and r1['STATION'][j]['OBSERVATIONS']['air_temp_set_1'][-1] is not None:
        max_t.append(r1['STATION'][j]['OBSERVATIONS']['air_temp_set_1'][-1])
        mt = (max(max_t))
        mi = (max_t).index(mt)
mt_t = round(mt, 1)
m_name = r1['STATION'][mi]['NAME']
m_stid = r1['STATION'][mi]['STID']
m_st = r1['STATION'][mi]['STATE']
mesolink2 = ' http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=' \
             + m_stid
mtresult = 'The current high temperature in the state of '+m_st+', is ' + \
            str(mt_t) + u'\N{DEGREE SIGN}' + 'F ' + mesolink2
print(mtresult)
api.update_status(mtresult)
# time.sleep(240)
random_state2 = random.choice(all_states)
s = requests.get(baseURL + 'timeseries?&state=' + random_state2 + parameters)
s1 = s.json()
s2 = []
for i in range(len(s1['STATION'])):
   if int(s1['STATION'][i]['MNET_ID']) in good_networks:
       s2.append(s1['STATION'][i])
min_t = []
for j in range(len(s2)):
   if s2[j]['QC_FLAGGED'] is False and s2[j]['OBSERVATIONS']['air_temp_set_1'][-1] is not None:
       min_t.append(s2[j]['OBSERVATIONS']['air_temp_set_1'][-1])
   mt2 = min(min_t)
   mi2 = (min_t).index(mt2)
mt2_t = round(mt2, 1)
m2_name = s2[mi2]['NAME']
m2_stid = s2[mi2]['STID']
m2_st = s2[mi2]['STATE']
mesolink3 = ' http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=' \
            + m2_stid
mt2result = 'The current low temperature in the state of ' + m2_st + ', is ' +\
            str(mt2_t)+u'\N{DEGREE SIGN}'+'F ' + mesolink3
print(mt2result)
api.update_status(mt2result)
#time.sleep(240)
random_state3 = random.choice(all_states)
wind = requests.get(baseURL + 'timeseries?&state=' + random_state2 + '&token='+token+'&status=active&' +
                   'units=english&obtimezone=local&qc=on&vars=wind_gust&recent=60')
wind1 = wind.json()
wind2 = []
for i in range(len(wind1['STATION'])):
   if int(wind1['STATION'][i]['MNET_ID']) in good_networks:
       wind2.append(wind1['STATION'][i])
max_w = []
for j in range(len(wind2)):
   if wind2[j]['QC_FLAGGED'] is False and wind2[j]['OBSERVATIONS']['wind_gust_set_1'][0] is not None:
       max_w.append(wind2[j]['OBSERVATIONS']['wind_gust_set_1'][0])
   mw = max(max_w)
   mwi = (max_w).index(mw)
mw_w = round(mw, 1)
mw_name = wind2[mwi]['NAME']
mw_stid = wind2[mwi]['STID']
mw_st = wind2[mwi]['STATE']
mesolink4 = ' http://mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi?stn=' \
            + mw_stid
mwresult = 'The current strongest wind gust in the state of ' + mw_st + ', is ' +\
            str(mw_w)+' mph' + mesolink4
print(mwresult)
#api.update_status(mwresult)
##sys.exit()
