#!/usr/bin/python3

import sys
import string
import time
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--minTemp", default=0,
                    help="Minimum temperature threshold. Default 0°C.")
args = parser.parse_args()
print('Forecast temperatures below {}°C:'.format(args.minTemp))

zeroCelsiusInKelvin = 273.15
minTempThresholdKelvin = zeroCelsiusInKelvin + float(args.minTemp)
minTempThresholdHit = False

try:
  apiKey = 'xxxx'
  cityId = '2638580'
  forecastUrl = 'https://api.openweathermap.org/data/2.5/forecast?id={}&APPID={}'.format(cityId, apiKey)
  forecastResponse = requests.get(url=forecastUrl)

  nowDt = int(time.time())

  for forecast in forecastResponse.json().get('list'):
    forecastDt = int(forecast['dt'])
    forecastOffset = forecastDt - nowDt
    forecastMinTempKelvin = int(forecast['main']['temp_min'])
    if forecastMinTempKelvin < minTempThresholdKelvin:
      minTempThresholdHit = True
      forecastMinTempCelsius = round(forecastMinTempKelvin - zeroCelsiusInKelvin, 1)
      forecastDtFriendly = time.asctime(time.localtime(forecastDt))
      print('{} at {}'.format(forecastMinTempCelsius, forecastDtFriendly))

  if not minTempThresholdHit:
    print('None')

except:
  print(sys.exc_info()[0])
