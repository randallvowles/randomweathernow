#!/usr/bin/env python

#Created by Randall Vowles, API token= belongs to me
#Twitter account also belongs to me

import tweepy, requests, simplejson, random, time, sys
 
CONSUMER_KEY = 
CONSUMER_SECRET = 
ACCESS_TOKEN = 
ACCESS_TOKEN_SECRET = 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
APItoken = 
#blacklist = [134, 203, 192, 92, 106, 48, 77, 126, 211, 197, 146, 196, 131, 23, 72, 208, 169, 80, 65]


good_networks = [1, 2, 3, 4, 5, 8, 11, 13, 15, 16, 17, 22, 25, 26, 29, 36, 39, 41, 45, 49, 54, 55, 56,\
                 57, 59, 60, 62, 63, 66, 70, 82, 83, 84, 85, 88, 89, 90, 91, 93, 97, 98, 99, \
                 100, 101, 102, 103, 104, 105, 107, 109, 110, 118, 119, 123, 125, 132, 136, 137, 139, \
                 143, 150, 151, 153, 158, 160, 162, 169, 170, 182, 183, 187, 188, 191, 194, 195, \
                 199, 200, 201, 206, 207, 208, 209, 212, 213]
network_id = random.choice(good_networks)
sq = requests.get('http://api.mesowest.net/v2/stations/metadata?&token='+APItoken+'&status=active&network='+str(network_id))
sq1 = simplejson.loads(sq.content)
random_station = random.choice(sq1['STATION'])
station_id = random_station['STID']
#print(station_id)
wq = requests.get('http://api.mesowest.net/v2/stations/timeseries?&token='+APItoken+'&units=english&obtimezone=local&qc=all&vars=air_temp&recent=60&stid='+station_id)
wq1 = simplejson.loads(wq.content)
while wq1['SUMMARY']['NUMBER_OF_OBJECTS'] == 0 : 
    random_station = random.choice(sq1['STATION'])
    station_id = random_station['STID']
    #print(station_id)
    wq = requests.get('http://api.mesowest.net/v2/stations/timeseries?&token='+APItoken+'&units=english&obtimezone=local&qc=all&recent=60&stid='+station_id)
    wq1 = simplejson.loads(wq.content)
else:
    try :
        wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
    except (KeyError, IndexError, TypeError) or wqtemp < -30 or wqtemp > 130 or wq1['QC_SUMMARY']['TOTAL_OBSERVATIONS_FLAGGED'] > 0 :
        random_station = random.choice(sq1['STATION'])
        station_id = random_station['STID']
        #print(station_id)
        wq = requests.get('http://api.mesowest.net/v2/stations/timeseries?&token='+APItoken+'&units=english&obtimezone=local&qc=all&recent=60&stid='+station_id)
        wq1 = simplejson.loads(wq.content)
        #wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
        try :
            wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
        except (KeyError, IndexError, TypeError) or wqtemp < -30 or wqtemp > 130 or wq1['QC_SUMMARY']['TOTAL_OBSERVATIONS_FLAGGED'] > 0 :
           random_station = random.choice(sq1['STATION'])
           station_id = random_station['STID']
            #print(station_id)
           wq = requests.get('http://api.mesowest.net/v2/stations/timeseries?&token='+APItoken+'&units=english&obtimezone=local&recent=60&stid='+station_id)
           wq1 = simplejson.loads(wq.content)
           #wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
           try :
               wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
           except (KeyError, IndexError, TypeError) or wqtemp < -30 or wqtemp > 130 or wq1['QC_SUMMARY']['TOTAL_OBSERVATIONS_FLAGGED'] > 0 :
               random_station = random.choice(sq1['STATION'])
               station_id = random_station['STID']
               #print(station_id)
               wq = requests.get('http://api.mesowest.net/v2/stations/timeseries?&token='+APItoken+'&units=english&obtimezone=local&recent=60&stid='+station_id)
               wq1 = simplejson.loads(wq.content)
               wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_set_1'][0]
               
wqtemp1 = str(wqtemp)+u'\N{DEGREE SIGN}'+'F'
#print(wqtemp1)            
wq1sn = wq1['STATION'][0]['NAME']
wq1st = wq1['STATION'][0]['STATE']
wqtime = wq1['STATION'][0]['OBSERVATIONS']['date_time']
wqresult = 'The current weather at ' + wq1sn + ', '+wq1st+' is ' + wqtemp1 + ' (provisional)'         
#print(wqresult)          
api.update_status(wqresult)
#print('Just tweeted: "' + wqresult + '"')             
           
time.sleep(300)    
#prints all tweets from twitter account
#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print (tweet.text)    
#sends new tweet for chosen station's temperature, prints tweet to screen
    
all_states = ['al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga', 'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md', 'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', \
                 'nv', 'nh', 'nj', 'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx','ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy', 'dc']  
random_state = random.choice(all_states)
r = requests.get('http://api.mesowest.net/v2/stations/timeseries?&state='+random_state+'&token='+APItoken+'&vars=air_temp&status=active&qc=all&recent=10&units=english&obtimezone=local');
r1 = simplejson.loads(r.content)
r2 = []
for i in range(len(r1['STATION'])):
    if int(r1['STATION'][i]['MNET_ID']) in good_networks:
        r2.append(r1['STATION'][i])      
max_temp_stations = []
for i in range(len(r2)):
    temp_var = (r2[i]['OBSERVATIONS']['air_temp_set_1'][0])
    if temp_var >= -30 and temp_var <= 130 :
        max_temp_stations.append(r2[i])
max_temps = []
for j in range(len(max_temp_stations)):
    if max_temp_stations[j]['QC_FLAGGED'] == False:         
        max_temps.append(max_temp_stations[j]['OBSERVATIONS']['air_temp_set_1'][0])
    mt = max((max_temps))
    mi = (max_temps).index(mt)  
m_name = max_temp_stations[mi]['NAME']
m_stid = max_temp_stations[mi]['STID']
m_st = max_temp_stations[mi]['STATE']
mtresult = 'The current high temperature in the state of '+m_st+', is '+str(mt)+u'\N{DEGREE SIGN}'+'F at '+m_name+' (provisional)'
#print(mtresult)
api.update_status(mtresult)
#print('Just tweeted: "' + mtresult + '"') 

time.sleep(300)

random_state2 = random.choice(all_states)
s = requests.get('http://api.mesowest.net/v2/stations/timeseries?&state='+random_state2+'&token='+APItoken+'&vars=air_temp&status=active&qc=all&recent=60&units=english&obtimezone=local');
s1 = simplejson.loads(s.content)
s2 = []
for i in range(len(s1['STATION'])):
    if int(s1['STATION'][i]['MNET_ID']) in good_networks:
        s2.append(s1['STATION'][i])      
min_temp_stations = []
for i in range(len(s2)):
    temp_var2 = (s2[i]['OBSERVATIONS']['air_temp_set_1'][0])
    if temp_var2 >= -30 and temp_var2 <= 130 :
        min_temp_stations.append(s2[i])
min_temps = []
for j in range(len(min_temp_stations)): 
    if min_temp_stations[j]['QC_FLAGGED'] == False:       
        min_temps.append(min_temp_stations[j]['OBSERVATIONS']['air_temp_set_1'][0])
    mt2 = min((min_temps))
    mi2 = (min_temps).index(mt2)  
m2_name = min_temp_stations[mi2]['NAME']
m2_stid = min_temp_stations[mi2]['STID']
m2_st = min_temp_stations[mi2]['STATE']
mt2result = 'The current low temperature in the state of '+m2_st+', is '+str(mt2)+u'\N{DEGREE SIGN}'+'F at '+m2_name+' (provisional)'
#print(mt2result)
api.update_status(mt2result)
#print('Just tweeted: "' + mt2result + '"') 

sys.exit()
