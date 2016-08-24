#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import xml.etree.ElementTree as dom
import sys
import getopt
import urllib
import ConfigParser


config = ConfigParser.ConfigParser()
config.read('ns.properties')

baseUrl = config.get('ns api', 'url')
params = {}

try:
    opts, args = getopt.getopt(sys.argv[1:], "hs:", ["station=", "help"])
except getopt.GetoptError:
    print 'ns.py -s <stationName>'    

if (len(opts) == 0):
    params['actual'] = 'true'
    params['unplanned'] = 'false'
    
for opt, arg in opts:
      if opt == '-h':
         print 'ns.py -s <station>'
         sys.exit()
      elif opt in ("-s", "--station"):
          params['station'] = arg
      else:
          print 'invalid arguments. use -h for help'
          sys.exit()


#print(baseUrl + urllib.urlencode(params))

response = requests.get(baseUrl + urllib.urlencode(params), auth=(config.get('ns api', 'username'), config.get('ns api', 'password')))

if (response.status_code == 200) :
    root = dom.fromstring(response.content)    

     # root = dom.parse('nsResponse.xml').getroot()
    if(root.tag == 'error'):
        print 'Request Failed with error : ' + root.find('message').text
    else:        
        unplanned = root.find('Ongepland')
        if (unplanned is not None):
            print('***********Unplanned Disruptions***********')
            for el in unplanned.findall('Storing') :
                print(el.find('Traject').text + ' : ' + el.find('Bericht').text)        
         
        planned = root.find('Gepland')
        if (planned is not None):
            print('***********Planned Disruptions***********')        
            for el in planned.findall('Storing'):
                print(el.find('Traject').text + ' : ' + el.find('Periode').text)

else:
    print('Request failed with response status code {}'.format(response.status_code))

