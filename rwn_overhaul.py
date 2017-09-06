#!/uufs/chpc.utah.edu/common/home/u0540701/MyVenv/bin/python

# Created by Randall Vowles, API token and twitter account belong to me
import configparser
import random
import json
import tweepy
import datetime
from datetime import date
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as md
# plt.switch_backend('agg')

config = configparser.RawConfigParser()
config.read(r'rwnconfig.txt')
consumer_key = config.get('rwn', 'CONSUMER_KEY')
consumer_secret = config.get('rwn', 'CONSUMER_SECRET')
access_token = config.get('rwn', 'ACCESS_TOKEN')
access_token_secret = config.get('rwn', 'ACCESS_TOKEN_SECRET')
api_token = config.get('rwn', 'API_TOKEN')
darksky_api = config.get('rwn', 'DARKSKY_KEY')
darksky_url = "https://api.darksky.net/forecast/" + darksky_api + "/"
bitlytoken = config.get('rwn', 'BITLYTOKEN')
gps_token = config.get('rwn', 'GPS_TOKEN')
with open('capitals.json') as data_file:
    capitals = json.load(data_file)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
all_states = ['al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de',
              'fl', 'ga', 'hi', 'id', 'il', 'in', 'ia', 'ks',
              'ky', 'la', 'me', 'md', 'ma', 'mi', 'mn', 'ms',
              'mo', 'mt', 'ne', 'nv', 'nh', 'nj', 'nm', 'ny',
              'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc',
              'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv',
              'wi', 'wy']

# error_log = open('./error_log.txt', 'a')
baseurl = 'http://api.mesowest.net/v2/stations/timeseries'
case_n = random.choice([1, 2, 3, 4, 5, 6, 7, 8])
#case_n = 8
# results1 = {}
# parameters = {}
# api_url = ''
# nq_url = ''

# if case_n == 1 or case_n == 2 or case_n == 3 or case_n ==4:
variable = 'air_temp'
# elif case_n == 4:
#    variable = 'wind_gust'
random_state = random.choice(all_states)
# network_id = "1,2,25,65,170"
network_id = '1,2'


def findExtreme(results1):
    if case_n == 2:
        _temp = -100
        _stid = ""
        for i in range(len(results1['STATION'])):
            b = len(results1['STATION'][i]['OBSERVATIONS']
                    [variable + '_set_1']) - 1
            if (results1['STATION'][i]['OBSERVATIONS']
                [variable + '_set_1'][b]) > _temp and \
                (results1['STATION'][i]['OBSERVATIONS']
                    [variable + '_set_1'][b]) is not None:
                    _temp = (results1['STATION'][i]
                             ['OBSERVATIONS'][variable +
                             '_set_1'][b])
                    _stid = results1['STATION'][i]['STID']
            else:
                continue
        max_temp = _temp
        stid_max = _stid
        return [stid_max, max_temp]
    elif case_n == 3:
        _temp = 100
        _stid = ""
        for i in range(len(results1['STATION'])):
            b = len(results1['STATION'][i]['OBSERVATIONS']
                    [variable + '_set_1']) - 1
            if (results1['STATION'][i]['OBSERVATIONS']
                [variable + '_set_1'][b]) < _temp and \
                (results1['STATION'][i]['OBSERVATIONS']
                    [variable + '_set_1'][b]) is not None:
                    _temp = (results1['STATION'][i]
                             ['OBSERVATIONS'][variable +
                             '_set_1'][b])
                    _stid = results1['STATION'][i]['STID']
            else:
                continue
        min_temp = _temp
        stid_min = _stid
        return [stid_min, min_temp]


def apiCall(PARAMETERS):
    results = requests.get(baseurl, params=PARAMETERS)
    results1 = results.json()
    return results1


def random_STID():
    params = {'token': api_token, 'status': 'active',
              'qc': 'on', 'recent': '65', 'units': 'english',
              'network': network_id, 'vars': variable}
    nq1 = apiCall(params)
    random_station = random.choice(nq1['STATION'])
    random_stid = random_station['STID']
    return random_stid

random_stid = random_STID()

if case_n == 1:
    parameters = {'token': api_token, 'status': 'active',
                  'qc': 'on', 'qc_remove_data': 'on',
                  'qc_checks': 'synopticlabs', 'recent': '65',
                  'units': 'english', 'stid': random_stid,
                  'vars': 'air_temp'}
elif case_n == 2:
    parameters = {'token': api_token, 'status': 'active',
                  'qc': 'on', 'qc_remove_data': 'on',
                  'qc_checks': 'synopticlabs', 'recent': '65',
                  'units': 'english', 'state': random_state,
                  'vars': 'air_temp', 'network': network_id}
elif case_n == 3:
    parameters = {'token': api_token, 'status': 'active',
                  'qc': 'on', 'qc_remove_data': 'on',
                  'qc_checks': 'synopticlabs', 'recent': '65',
                  'units': 'english', 'state': random_state,
                  'vars': 'air_temp', 'network': network_id}
elif case_n == 4:
    parameters = {'token': api_token, 'status': 'active',
                  'qc': 'on', 'qc_remove_data': 'on',
                  'qc_checks': 'synopticlabs', 'recent': '20160',
                  'units': 'english', 'stid': random_stid,
                  'vars': 'air_temp'}
elif case_n == 5:
    parameters = {'token': api_token, 'status': 'active',
                  'qc': 'on', 'qc_remove_data': 'on',
                  'qc_checks': 'synopticlabs', 'recent': '4320',
                  'units': 'english', 'stid': random_stid,
                  'vars': 'air_temp,relative_humidity,dew_point_temperature'}


def create30DayPlot(results):
    x = [md.date2num(datetime.datetime.strptime(val, '%Y-%m-%dT%H:%M:%SZ'))
         for val in results['STATION'][0]['OBSERVATIONS']['date_time']]
#    print results
    hour = md.HourLocator(interval=24)
    fmt = md.DateFormatter('%m-%d')
    with plt.xkcd():
        fig, ax = plt.subplots()
        ax.plot(x, (results['STATION'][0]['OBSERVATIONS']
                    [variable + '_set_1']), 'r')
        plt.title('Temperatures at ' + results['STATION'][0]['NAME'], y=1.08)
        plt.ylabel('Temperature (' + u'\N{DEGREE SIGN}' + 'F)')
        plt.xlabel('Previous 14 Days')
        ax.xaxis.set_major_locator(hour)
        ax.xaxis.set_major_formatter(fmt)
        fig.autofmt_xdate(rotation=90)
        plt.savefig('14_day_image.png', bbox_inches='tight')
        #    plt.show()


def create7DayPlot(results):
    x = [md.date2num(datetime.datetime.strptime(val, '%Y-%m-%dT%H:%M:%SZ'))
         for val in results['STATION'][0]['OBSERVATIONS']['date_time']]
#    print results
    hour = md.HourLocator(interval=24)
    fmt = md.DateFormatter('%m-%d')
    with plt.xkcd():
        ax1 = plt.subplot()
        ax1.plot(x, (results['STATION'][0]['OBSERVATIONS']
                     ['air_temp_set_1']), 'r')
        ax1.plot(x, (results['STATION'][0]['OBSERVATIONS']
                     ['dew_point_temperature_set_1d']), 'b')
        ax2 = ax1.twinx()
        ax2.plot(x, (results['STATION'][0]['OBSERVATIONS']
                     ['relative_humidity_set_1']), 'g')
        ax1.set_ylabel('Temperature (' + u'\N{DEGREE SIGN}' + 'F)')
        ax1.set_xlabel('Previous 3 Days')
        ax1.xaxis.set_major_locator(hour)
        ax1.xaxis.set_major_formatter(fmt)
        ax2.set_ylabel('Relative Humidity (%)')
        plt.title('Temperature (red), Dew Point (blue), \
                  and Relative Humidity (green)', y=1.08)
        plt.savefig('3_day_image.png', bbox_inches='tight')
        #    plt.show()


def subtract_a_year(d):
    try:
        return d.replace(year=d.year - 1)
    except ValueError:
        return d - (date(d.year - 1, 1, 1) + date(d.year, 1, 1))


def historicalDates():
    now_time = datetime.datetime.utcnow()
    end_time = (now_time).strftime('%Y%m%d%H%M')
    start_time = (subtract_a_year(now_time)).strftime('%Y%m%d%H%M')
#    print [start_time, end_time]
    return [start_time, end_time]


def findCity(stid):
    r1 = requests.get(baseurl, params={"stid": stid,
                                       "recent": 120,
                                       "token": api_token})
    r2 = r1.json()
    lat = r2['STATION'][0]['LATITUDE']
    lon = r2['STATION'][0]['LONGITUDE']
    loc = requests.get('https://maps.googleapis.com/maps/' +
                       'api/geocode/json?latlng=' + lat +
                       ',' + lon + '&key=' + gps_token)
#    print loc.url
    loc1 = loc.json()
    loc_city = r2['STATION'][0]['NAME']
    for i in range(len(loc1['results'])):
        if loc1['results'][i]['types'][0] == "locality":
            loc_city = loc1['results'][i]['address_components'][0]['short_name']
        else:
            continue
#    print loc_city
    return loc_city


def sendToTwitter():
    loc_st = random_state
#    stid = result_tw['STATION'][0]['STID']
    start_time = datetime.date.today().strftime('%Y%m%d%H%M')
    end_time = (datetime.datetime.utcnow()).strftime('%Y%m%d%H%M')

    if case_n == 1:
        results_1 = apiCall(parameters)
        stid = results_1['STATION'][0]['STID']
        state_1 = results_1['STATION'][0]['STATE']
        a = len(results_1['STATION'][0]['OBSERVATIONS']
                [variable + '_set_1']) - 1
        tw_ob = str(results_1['STATION'][0]['OBSERVATIONS']
                    [variable + '_set_1'][a])
#        print results_1, stid, tw_ob
        long_url = ("https://synopticlabs.org/demos/tabtable/?stid=" +
                    stid + "&start=" + start_time + "&end=" + end_time)
        hashtag = (' #' + (results_1['STATION'][0]['STATE'])
                   .lower() + 'wx ')
        tweet = ('The current temperature at ' + findCity(stid) +
                 ', ' + state_1 + ' is ' + tw_ob + u'\N{DEGREE SIGN}' +
                 'F ' + hashtag + long_url)
        print tweet
#        api.update_status(tweet)

    elif case_n == 2:
#        apiCall(parameters)
        results_2 = findExtreme(apiCall(parameters))
        stid = results_2[0]
        tw_ob = str(results_2[1])
#        print results_2, stid, tw_ob
        long_url = ("https://synopticlabs.org/demos/tabtable/?stid=" +
                    stid + "&start=" + start_time + "&end=" + end_time)
        hashtag = ' #'+loc_st+'wx '
        tweet = ('The state of ' + loc_st.upper() +
                 ' currently has a high temperature of ' +
                 tw_ob + u'\N{DEGREE SIGN}' + 'F, at '+ findCity(stid) + hashtag + long_url)
        print tweet
#        api.update_status(tweet)

    elif case_n == 3:
#        apiCall(parameters)
        results_3 = findExtreme(apiCall(parameters))
        stid = results_3[0]
        tw_ob = str(results_3[1])
#        print results_3, stid, tw_ob
        long_url = ("https://synopticlabs.org/demos/tabtable/?stid=" +
                    stid + "&start=" + start_time + "&end=" + end_time)
        hashtag = ' #'+loc_st+'wx '
        tweet = ('The state of ' + loc_st.upper() +
                 ' currently has a low temperature of ' +
                 tw_ob + u'\N{DEGREE SIGN}' + 'F, at '+ findCity(stid) + hashtag + long_url)
        print tweet
#        api.update_status(tweet)

    elif case_n == 4:
        results_4 = apiCall(parameters)
        stid = results_4['STATION'][0]['STID']
#        print stid
        long_url = ("https://synopticlabs.org/demos/tabtable/?stid=" +
                    stid + "&start=" + start_time + "&end=" + end_time)
        hashtag = ' #' + (results_4['STATION'][0]['STATE']).lower() + 'wx '
        create30DayPlot(results_4)
        tweet = ('Check out the temperature over the past fortnight at ' +
                 findCity(stid) + hashtag + long_url)
#        print tweet
        api.update_with_media('14_day_image.png', tweet)

    elif case_n == 5:
        results_5 = apiCall(parameters)
        stid = results_5['STATION'][0]['STID']
#        print stid
        long_url = ("https://synopticlabs.org/demos/tabtable/?stid=" +
                    stid + "&start=" + start_time + "&end=" + end_time)
        hashtag = ' #' + (results_5['STATION'][0]['STATE']).lower() + 'wx '
        create7DayPlot(results_5)
        tweet = ('Check out the temperature and moisture over the past three days at ' +
                 findCity(stid) + hashtag + long_url)
        print tweet
#        api.update_with_media('3_day_image.png', tweet)

    elif case_n == 6:
        stid = random_stid
        times = historicalDates()
        _start = times[0]
        _end = times[1]
        r1 = requests.get(baseurl, params={"stid": stid,
                                           "start": _start,
                                           "end": _end,
                                           "vars": variable,
                                           "token": api_token,
                                           "units": "english"})
        r2 = r1.json()
        a = len(r2['STATION'][0]['OBSERVATIONS'][variable + '_set_1']) - 1
        old_ob = str(r2['STATION'][0]['OBSERVATIONS'][variable + '_set_1'][0])
        new_ob = str(r2['STATION'][0]['OBSERVATIONS'][variable + '_set_1'][a])
#        print old_ob, new_ob
        long_url = ("https://synopticlabs.org/demos/tabtable/?stid=" +
                    stid + "&start=" + start_time + "&end=" + end_time)
        hashtag = ' #' + (r2['STATION'][0]['STATE']).lower() + 'wx '
        tweet = ('Right now it is ' + new_ob + u'\N{DEGREE SIGN}' +
                 'F at ' + findCity(stid) + ', 1 year ago today it was ' +
                 old_ob + u'\N{DEGREE SIGN}' + 'F ' + hashtag + long_url)
        print tweet
#        api.update_status(tweet)

    elif case_n == 7:
        stid = random_stid
        times = historicalDates()
        _start = times[0]
        _end = times[1]
        r1 = requests.get(baseurl, params={"stid": stid,
                                           "start": _start,
                                           "end": _end,
                                           "vars": variable,
                                           "token": api_token,
                                           "units": "english"})
        r2 = r1.json()
        _highTemp = -100
        _lowTemp = 100
        for i in range(len(r2['STATION'][0]['OBSERVATIONS']
                           [variable + '_set_1'])):
            if (r2['STATION'][0]['OBSERVATIONS'][variable + '_set_1'][i]) >\
                _highTemp and (r2['STATION'][0]['OBSERVATIONS']
                               [variable + '_set_1'][i]) is not None:
                _highTemp = (r2['STATION'][0]['OBSERVATIONS']
                             [variable + '_set_1'][i])
                _hD = r2['STATION'][0]['OBSERVATIONS']['date_time'][i]
            else:
                continue
        for i in range(len(r2['STATION'][0]['OBSERVATIONS']
                           [variable + '_set_1'])):
            if (r2['STATION'][0]['OBSERVATIONS'][variable + '_set_1'][i]) <\
                _lowTemp and (r2['STATION'][0]['OBSERVATIONS']
                              [variable + '_set_1'][i]) is not None:
                _lowTemp = (r2['STATION'][0]['OBSERVATIONS']
                            [variable + '_set_1'][i])
                _lD = r2['STATION'][0]['OBSERVATIONS']['date_time'][i]
            else:
                continue
        _highDate = (datetime.datetime.strptime(_hD, '%Y-%m-%dT%H:%M:%SZ')).strftime('%Y-%m-%d')
        _lowDate = (datetime.datetime.strptime(_lD, '%Y-%m-%dT%H:%M:%SZ')).strftime('%Y-%m-%d')
        long_url = ("https://synopticlabs.org/demos/tabtable/?stid=" +
                    stid + "&start=" + start_time + "&end=" + end_time)
        hashtag = ' #' + (r2['STATION'][0]['STATE']).lower() + 'wx '
        tweet = ('Over the past year at ' + (r2['STATION'][0]['STID']) +
                 ', the highest temp was ' + str(_highTemp) +
                 u'\N{DEGREE SIGN}' + 'F on ' + _highDate +
                 ' and the lowest temp was ' + str(_lowTemp) +
                 u'\N{DEGREE SIGN}' + 'F on ' + _lowDate + hashtag)
        print tweet
#        api.update_status(tweet)

    elif case_n == 8:
        state = random_state
        state_info = capitals[state.upper()]
        print state_info
        r1 = requests.get(darksky_url + state_info['lat'] + ',' + state_info['long'])
        r2 = r1.json()
        hashtag = ' #' + state + 'wx '
        tweet = 'The forecast for ' + state_info['capital'] + ', ' + state.upper() + ' is ' + r2['daily']['summary'] + hashtag
        print tweet
#        api.update_status(tweet)

#    elif case_n == 9:
        # state high and low over past year
        # request data 3 months at a time and combine
        # then use findExtreme()


sendToTwitter()

# TODO: check qc for errors (illogical temp in september)
# round temperatures to one decimal place (not two)
