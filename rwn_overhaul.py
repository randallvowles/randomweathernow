#!/uufs/chpc.utah.edu/common/home/u0540701/MyVenv/bin/python

# Created by Randall Vowles, API token and twitter account belong to me
import configparser
import random
import time
import sys
import tweepy
import urllib
import datetime
import numpy as np
import json
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime


config = configparser.RawConfigParser()
config.read(r'rwnconfig.txt')
consumer_key = config.get('rwn', 'CONSUMER_KEY')
consumer_secret = config.get('rwn', 'CONSUMER_SECRET')
access_token = config.get('rwn', 'ACCESS_TOKEN')
access_token_secret = config.get('rwn', 'ACCESS_TOKEN_SECRET')
api_token = config.get('rwn', 'API_TOKEN')
bitlytoken = config.get('rwn', 'BITLYTOKEN')
gps_token = config.get('rwn', 'GPS_TOKEN')
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
error_log = open('./error_log.txt', 'a')
baseurl = 'http://api.mesowest.net/v2/stations/timeseries'
#case_n = random.choice([1, 2, 3, 4])
case_n = 4
#results1 = {}
#parameters = {}
#api_url = ''
#nq_url = ''

#if case_n == 1 or case_n == 2 or case_n == 3 or case_n ==4:
variable = 'air_temp'
#elif case_n == 4:
#    variable = 'wind_gust'
random_state = random.choice(all_states)


def findExtreme(results1):
    if case_n == 2:
#        print results1
        _temp = results1['STATION'][0]['OBSERVATIONS'][variable + '_set_1'][0]
        _stid = results1['STATION'][0]['STID']
        for i in range(len(results1['STATION'])):
            a = len(results1['STATION'][i]['OBSERVATIONS'][variable + '_set_1']) - 1
            if results1['STATION'][i]['OBSERVATIONS'][variable + '_set_1'][a] > _temp and results1['STATION'][i]['OBSERVATIONS'][variable + '_set_1'][a] is not None:
                _temp = results1['STATION'][i]['OBSERVATIONS'][variable + '_set_1'][a]
                _stid = results1['STATION'][i]['STID']
        max_temp = _temp
        stid_max = _stid
        print stid_max, max_temp
        return stid_max, max_temp
    elif case_n == 3:
        for i in range(len(results1['STATION'])):
            a = len(results1['STATION'][i]['OBSERVATIONS'][variable + '_set_1']) - 1
            _temp = results1['STATION'][i]['OBSERVATIONS'][variable + '_set_1'][a]
            _stid = results1['STATION'][i]['STID']
            if results1['STATION'][i]['OBSERVATIONS'][variable + '_set_1'][a] < _temp and results1['STATION'][i]['OBSERVATIONS'][variable + '_set_1'][a] is not None:
                results1['STATION'][i]['OBSERVATIONS'][variable + '_set_1'][a] = _temp
                results1['STATION'][i]['STID'] = _stid
        min_temp = _temp
        stid_min = _stid
        print stid_min, min_temp
        return stid_min, min_temp


def apiCall(PARAMETERS):
    results = requests.get(baseurl, params=PARAMETERS)
    results1 = results.json()
#    findExtreme(results1)
    return results1


def random_STID():
    network_id = "1"
    params = {'token': api_token, 'status': 'active', 'qc': 'on',
              'recent': '65', 'units': 'english', 'network': network_id,
              'vars': variable}
    nq1 = apiCall(params)
    random_station = random.choice(nq1['STATION'])
    random_stid = random_station['STID']
    return random_stid

random_stid = random_STID()

if case_n == 1:
    parameters = {'token': api_token, 'status': 'active', 'qc': 'on', 'qc_remove_data': 'on', 'qc_checks': 'synopticlabs',
                  'recent': '65', 'units': 'english', 'stid': random_stid,
                  'vars': 'air_temp'}
elif case_n == 2:
    parameters = {'token': api_token, 'status': 'active', 'qc': 'on', 'qc_remove_data': 'on', 'qc_checks': 'synopticlabs',
                  'recent': '65', 'units': 'english', 'state': random_state,
                  'vars': 'air_temp', 'network': '1'}
elif case_n == 3:
    parameters = {'token': api_token, 'status': 'active', 'qc': 'on', 'qc_remove_data': 'on', 'qc_checks': 'synopticlabs',
                  'recent': '65', 'units': 'english', 'state': random_state,
                  'vars': 'air_temp', 'network': '1'}
elif case_n == 4:
    parameters = {'token': api_token, 'status': 'active', 'qc': 'on', 'qc_remove_data': 'on', 'qc_checks': 'synopticlabs',
                  'recent': '43200', 'units': 'english', 'stid': random_stid,
                  'vars': 'air_temp', 'network': '1'}


def create30DayPlot(results):
    x = [md.date2num(datetime.datetime.strptime(val,'%Y-%m-%dT%H:%M:%SZ')) for val in results['STATION'][0]['OBSERVATIONS']['date_time']]
#    print results
    hour=md.HourLocator(interval=24)
    fmt=md.DateFormatter('%m-%d')
    fig,ax=plt.subplots()
    ax.plot(x, (results['STATION'][0]['OBSERVATIONS'][variable + '_set_1']), 'b-')
    plt.title('Temperatures at ' + results['STATION'][0]['NAME'])
    plt.ylabel('Temperature (' + u'\N{DEGREE SIGN}' + 'F)')
    plt.xlabel('Previous 30 Days')
    ax.xaxis.set_major_locator(hour)
    ax.xaxis.set_major_formatter(fmt)
    fig.autofmt_xdate(rotation=90)
    plt.legend(loc=0)
    plt.savefig('30_day_image.png', bbox_inches='tight')
    plt.show()


def findCity(results1):
    lat = results1['STATION'][0]['LATITUDE']
    lon = results1['STATION'][0]['LONGITUDE']
    try:
        loc = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng='+ lat +','+ lon +'key='+ gps_token)
        loc1 = loc.json()
        loc_city = loc1['results'][0]['address_components'][2]['long_name']
        return loc_city
    except:
        loc_city = results1['STATION'][0]['STID']
        return loc_city


def sendToTwitter(result_tw):
#    DATETIME = results1['STATION'][0]['OBSERVATIONS']['date_time'][-1]
#    DATETIME_P = arrow.get(DATETIME)
#    LINKBASE = 'mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi'
#    LINKPARAMS = {'product=': '', 'past=': '1',
#                  'stn=': str(RESULTS1['STATION'][0]['STID']),
#                  'day1': str(DATETIME_P.day), 'month1': str(DATETIME_P.month),
#                  'year1': str(DATETIME_P.year), 'hour1': str(DATETIME_P.hour)}
#    TR = urllib.urlopen(LINKBASE, params=LINKPARAMS)
#    LONGURL = requests.utils.get_unicode_from_response(TR)
    loc_st = result_tw['STATION'][0]['STATE']
    stid = result_tw['STATION'][0]['STID']
    start_time = datetime.date.today().strftime('%Y%m%d%H%M')
    end_time = (datetime.datetime.now()).strftime('%Y%m%d%H%M')
    long_url = "https://synopticlabs.org/demos/tabtable/?stid" + stid + "&start=" + start_time + "&end=" + end_time
    BITLYR = requests.get('https://api-ssl.bitly.com/v3/shorten?access_token='+
                          bitlytoken + '&longUrl=' + long_url + '%2F&format=txt')
    linkurl = str(BITLYR.text)
    hashtag = ' #'+loc_st+'wx'
    if case_n == 1:
        tweet = 'The current temperature at ' + findCity(result_tw) + ', ' + loc_st +' is '\
                 + result_tw + u'\N{DEGREE SIGN}' + 'F ' + hashtag + linkurl
    elif case_n == 2:
        tweet = 'The state of '+ loc_st +' currently has a high temperature of '+\
                result_tw + u'\N{DEGREE SIGN}' + 'F ' + hashtag + linkurl
    elif case_n == 3:
        tweet = 'The state of '+ loc_st +' currently has a low temperature of '+\
                result_tw + u'\N{DEGREE SIGN}' + 'F ' + hashtag + linkurl
#    elif case_n == 4:
#        tweet = 'The current strongest wind gust in ' + loc_st + \
#                ' is ' + result_tw + ' mph' + hashtag + linkurl
    api.update_status(tweet)



create30DayPlot(apiCall(parameters))


