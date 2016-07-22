#Created by Randall Vowles, API token= belongs to me
#Twitter account also belongs to me

import tweepy, requests, simplejson, random, time
 
CONSUMER_KEY = 
CONSUMER_SECRET = 
ACCESS_TOKEN = 
ACCESS_TOKEN_SECRET = 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
APItoken = 
nq = requests.get('http://api.mesowest.net/v2/networks?&token='+APItoken)
nq1 = simplejson.loads(nq.content)
random_network = random.choice(nq1['MNET'])
network_id = int(random_network['ID'])
while network_id > 1000 or network_id == 134 or network_id == 203 or network_id == 192 or network_id == 92 or network_id == 72 \
    or network_id == 106 or network_id == 48 or network_id == 77 or network_id == 126 or network_id == 211 or network_id == 208 \
    or network_id == 197 or network_id == 146 or network_id == 196 or network_id == 131 or network_id == 23 or network_id == 169 \
    or random_network['ACTIVE_STATIONS'] == 0 or random_network['REPORTING_STATIONS'] == 0 or network_id == 80 :
    random_network = random.choice(nq1['MNET'])
    network_id = int(random_network['ID'])
print(random_network['LONGNAME'])    
sq = requests.get('http://api.mesowest.net/v2/stations/metadata?&token='+APItoken+'&status=active&network='+str(network_id))
sq1 = simplejson.loads(sq.content)
random_station = random.choice(sq1['STATION'])
station_id = random_station['STID']
print(station_id)
wq = requests.get('http://api.mesowest.net/v2/stations/latest?&token='+APItoken+'&units=english&obtimezone=local&vars=air_temp&within=240&stid='+station_id)
wq1 = simplejson.loads(wq.content)
while wq1['SUMMARY']['NUMBER_OF_OBJECTS'] == 0 : 
    random_station = random.choice(sq1['STATION'])
    station_id = random_station['STID']
    print(station_id)
    wq = requests.get('http://api.mesowest.net/v2/stations/latest?&token='+APItoken+'&units=english&obtimezone=local&within=240&stid='+station_id)
    wq1 = simplejson.loads(wq.content)
    try :
        wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_value_1']['value']
    except (KeyError, IndexError, TypeError) or wqtemp < -50 or wqtemp > 150 :
        random_station = random.choice(sq1['STATION'])
        station_id = random_station['STID']
        print(station_id)
        wq = requests.get('http://api.mesowest.net/v2/stations/latest?&token='+APItoken+'&units=english&obtimezone=local&within=240&stid='+station_id)
        wq1 = simplejson.loads(wq.content)
        try :
            wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_value_1']['value']
        except (KeyError, IndexError, TypeError) or wqtemp < -50 or wqtemp > 150 :
            random_station = random.choice(sq1['STATION'])
            station_id = random_station['STID']
            print(station_id)
            wq = requests.get('http://api.mesowest.net/v2/stations/latest?&token='+APItoken+'&units=english&obtimezone=local&within=240&stid='+station_id)
            wq1 = simplejson.loads(wq.content)
            wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_value_1']['value']
            try :
                wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_value_1']['value']
            except (KeyError, IndexError, TypeError) or wqtemp < -50 or wqtemp > 150 :
                random_station = random.choice(sq1['STATION'])
                station_id = random_station['STID']
                print(station_id)
                wq = requests.get('http://api.mesowest.net/v2/stations/latest?&token='+APItoken+'&units=english&obtimezone=local&within=240&stid='+station_id)
                wq1 = simplejson.loads(wq.content)
                wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_value_1']['value']
else:
    wqtemp = wq1['STATION'][0]['OBSERVATIONS']['air_temp_value_1']['value']
    wqtemp1 = str(wqtemp)+u'\N{DEGREE SIGN}'+'F'
print(wqtemp1)            
wq1sn = wq1['STATION'][0]['NAME']
wq1st = wq1['STATION'][0]['STATE']
wqtime = wq1['STATION'][0]['OBSERVATIONS']['air_temp_value_1']['date_time']
wqresult = 'The current weather at ' + wq1sn + ', '+wq1st+' is ' + wqtemp1          
#print(wqresult)          
api.update_status(wqresult)
print('Just tweeted: "' + wqresult + '"')             
           
time.sleep(300)    
#prints all tweets from twitter account
#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print (tweet.text)    
#sends new tweet for chosen station's temperature, prints tweet to screen
    
all_states = ['al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga', 'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md', 'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', \
                 'nv', 'nh', 'nj', 'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx','ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy', 'dc']  
random_state = random.choice(all_states)
r = requests.get('http://api.mesowest.net/v2/stations/latest?&state='+random_state+'&token='+APItoken+'&vars=air_temp&status=active&within=60&units=english&obtimezone=local');
r1 = simplejson.loads(r.content)
max_temp_stations = []
for i in range(len(r1['STATION'])):
    temp_var = (r1['STATION'][i]['OBSERVATIONS']['air_temp_value_1']['value'])
    if temp_var >= -30 and temp_var <= 130 :
        max_temp_stations.append(r1['STATION'][i])
max_temps = []
for j in range(len(max_temp_stations)):        
    max_temps.append(max_temp_stations[j]['OBSERVATIONS']['air_temp_value_1']['value'])
    mt = max((max_temps))
    mi = (max_temps).index(mt)  
m_name = max_temp_stations[mi]['NAME']
m_stid = max_temp_stations[mi]['STID']
m_st = max_temp_stations[mi]['STATE']
mtresult = 'The current high temperature in the state of '+m_st+', is '+str(mt)+u'\N{DEGREE SIGN}'+'F at '+m_name
#print(mtresult)
api.update_status(mtresult)
print('Just tweeted: "' + mtresult + '"') 

time.sleep(300)

random_state2 = random.choice(all_states)
s = requests.get('http://api.mesowest.net/v2/stations/latest?&state='+random_state2+'&token='+APItoken+'&vars=air_temp&status=active&within=60&units=english&obtimezone=local');
s1 = simplejson.loads(s.content)
min_temp_stations = []
for i in range(len(s1['STATION'])):
    temp_var2 = (s1['STATION'][i]['OBSERVATIONS']['air_temp_value_1']['value'])
    if temp_var2 >= -30 and temp_var2 <= 130 :
        min_temp_stations.append(s1['STATION'][i])
min_temps = []
for j in range(len(min_temp_stations)):        
    min_temps.append(min_temp_stations[j]['OBSERVATIONS']['air_temp_value_1']['value'])
    mt2 = min((min_temps))
    mi2 = (min_temps).index(mt2)  
m2_name = min_temp_stations[mi2]['NAME']
m2_stid = min_temp_stations[mi2]['STID']
m2_st = min_temp_stations[mi2]['STATE']
mt2result = 'The current low temperature in the state of '+m2_st+', is '+str(mt2)+u'\N{DEGREE SIGN}'+'F at '+m2_name
#print(mt2result)
api.update_status(mt2result)
print('Just tweeted: "' + mt2result + '"') 



