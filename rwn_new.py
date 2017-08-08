#!/uufs/chpc.utah.edu/common/home/u0540701/MyVenv/bin/python

# Created by Randall Vowles, API token and twitter account belong to me
import configparser
import random
import time
import sys
import tweepy
import requests
import arrow
import numpy
import json
# import bitly_api
CONFIG = configparser.ConfigParser()
CONFIG.read(r'./rwnconfig.txt')  # /uufs/chpc.utah.edu/common/home/u0540701/randomweathernow
CONSUMER_KEY = CONFIG.get('rwn', 'CONSUMER_KEY')
CONSUMER_SECRET = CONFIG.get('rwn', 'CONSUMER_SECRET')
ACCESS_TOKEN = CONFIG.get('rwn', 'ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = CONFIG.get('rwn', 'ACCESS_TOKEN_SECRET')
API_TOKEN = CONFIG.get('rwn', 'API_TOKEN')
BITLYTOKEN = CONFIG.get('rwn', 'BITLYTOKEN')
GPS_TOKEN = CONFIG.get('rwn', 'GPS_TOKEN')
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
API = tweepy.API(AUTH)
DICT = open('dictionaries.json', 'r')
GOOD_NETWORKS = CONFIG.get('rwn', 'GOOD_NETWORKS')
ALL_STATES = CONFIG.get('rwn', 'ALL_STATES')
ERROR_LOG = open('./error_log.txt', 'a')
BASEURL = 'http://api.mesowest.net/v2/stations/timeseries'
goFLAG = False
CASE_N = random.choice([1, 2, 3, 4])
RESULT1 = {}
PARAMETERS = {}
API_URL = ''
NQ_URL = ''
if CASE_N == 1 or CASE_N == 2 or CASE_N == 3:
    VARIABLE = 'air_temp_set_1'
elif CASE_N == 4:
    VARIABLE = 'wind_gust_set_1'

def randomSTID():
    NETWORK_ID = str(random.choice(GOOD_NETWORKS))
    PARANET = {'token': API_TOKEN, 'status': 'active', 'qc': 'on',
               'recent': '60', 'units': 'english', 'network': NETWORK_ID,
               'vars': VARIABLE}
    NQ = requests.get(BASEURL, params=PARANET)
    NQ1 = NQ.json()
    NQ_URL = NQ.url
    RANDOM_STATION = random.choice(NQ1['STATION'])
    RANDOM_STID = RANDOM_STATION['STID']
    return RANDOM_STID


def pickOne(randomSTID):
    RANDOM_STATE = random.choice(ALL_STATES)
    if CASE_N == 1:
        RANDOM_STID = randomSTID()
        PARAMETERS = {'token': API_TOKEN, 'status': 'active', 'qc': 'all',
                      'recent': '60', 'units': 'english', 'stid': RANDOM_STID,
                      'vars': 'air_temp'}
        return PARAMETERS
    elif CASE_N == 2:
        PARAMETERS = {'token': API_TOKEN, 'status': 'active', 'qc': 'all',
                      'recent': '60', 'units': 'english', 'state': RANDOM_STATE,
                      'vars': 'air_temp', 'network': '1,2'}
        return PARAMETERS
    elif CASE_N == 3:
        PARAMETERS = {'token': API_TOKEN, 'status': 'active', 'qc': 'all',
                      'recent': '60', 'units': 'english', 'state': RANDOM_STATE,
                      'vars': 'air_temp', 'network': '1,2'}
        return PARAMETERS
    elif CASE_N == 4:
        PARAMETERS = {'token': API_TOKEN, 'status': 'active', 'qc': 'all',
                      'recent': '60', 'units': 'english', 'state': RANDOM_STATE,
                      'vars': 'wind_gust', 'network': '1,2'}
        return PARAMETERS


def apiCall(PARAMETERS):
    RESULTS = requests.get(BASEURL, params=PARAMETERS)
    RESULTS1 = RESULTS.json()
    if CASE_N == 2:
        for i in range(len(RESULTS1['STATION'])):
            MAX_TEMP = numpy.amax(RESULTS1['STATION'][i]['OBSERVATIONS'][VARIABLE])
    elif CASE_N == 3:
        for i in range(len(RESULTS1['STATION'])):
            MIN_TEMP = numpy.amin(RESULTS1['STATION'][i]['OBSERVATIONS'][VARIABLE])

    RESULTS_V = RESULTS1['STATION'][0]['OBSERVATIONS'][VARIABLE][-1]
    API_URL = RESULTS.url
    return RESULTS1 and RESULTS_V


def valueQC(RESULTS1, RESULTS_V):
    try:
        if RESULTS1['STATION'][0]['QC_FLAGGED'] is True or \
           RESULTS_V < -30 or RESULTS_V > 130 or \
           RESULTS1['SUMMARY']['RESPONSE_CODE'] != 1:
                ERROR_LOG.write('ERROR! bad value at ' +
                                RESULTS1['STATION'][0]['OBSERVATIONS']['date_time'][-1] +
                                ' with API RESULTS: ' + API_URL + '\n')
        else:
            goFLAG = True
            return goFLAG
    except (KeyError, IndexError, TypeError):
        ERROR_LOG.write('ERROR! bad station results ' + API_URL + '\n')
        goFLAG = False
        return goFLAG


def sendToTwitter(RESULTS_TW):
    LAT = RESULTS1['STATION'][0]['LATITUDE']
    LON - RESULTS1['STATION'][0]['LONGITUDE']
    try:
        LOC = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng='+LAT+','+LON+'key='+GPS_TOKEN)
        LOC1 = LOC.json()
        LOC_CITY = LOC1['results'][0]['address_components'][2]['long_name']
    except:
        LOC_CITY = RESULTS1['STATION'][0]['STID']
    LOC_ST = RESULTS1['STATION'][0]['STATE']
    STN = RESULTS1['STATION'][0]['STID']
    DATETIME = RESULTS1['STATION'][0]['OBSERVATIONS']['date_time'][-1]
    DATETIME_P = arrow.get(DATETIME)
    LINKBASE = 'mesowest.utah.edu/cgi-bin/droman/meso_base_dyn.cgi'
    LINKPARAMS = {'product=': '', 'past=': '1',
                  'stn=': str(RESULTS1['STATION'][0]['STID']),
                  'day1': str(DATETIME_P.day), 'month1': str(DATETIME_P.month),
                  'year1': str(DATETIME_P.year), 'hour1': str(DATETIME_P.hour)}
    TR = requests.get(LINKBASE, params=LINKPARAMS)
    LONGURL = requests.utils.get_unicode_from_response(TR)
    BITLYR = requests.get('https://api-ssl.bitly.com/v3/shorten?access_token='+
                          BITLYTOKEN + '&longUrl='+LONGURL1+'%2F&format=txt')
    LINKURL = str(BITLYR.text)
    HASHTAG = ' #'+LOC_ST+'wx'
    if CASE_N == 1:
        TWEET = 'The current temperature at ' + LOC_CITY + ', ' +LOC_ST+' is '\
                 + RESULT_TW + HASHTAG
    elif CASE_N == 2:
        TWEET = 'The state of '+LOC_ST+' currently has a high temperature of '+\
                RESULT_TW + HASHTAG + LINKURL
    elif CASE_N == 3:
        TWEET = 'The state of '+LOC_ST+' currently has a low temperature of '+\
                RESULT_TW + HASHTAG + LINKURL
    elif CASE_N == 4:
        TWEET = 'The current strongest wind gust in ' + LOC_ST + \
                ' is ' + RESULT_TW + HASHTAG + LINKURL
    API.update_status(TWEET)


while goFLAG is False:
    RESULT = apiCall(pickOne(randomSTID))
    goFLAG = valueQC(RESULT)
    RESULT_TW = round(RESULTS_V, 1) + ' ' + RESULTS1['UNITS'][0]
sendToTwitter(RESULT_TW)
ERROR_LOG.close
sys.exit

# TODO: round results to tenths, units
