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
  apiKey = 'a4bffb33bb8ef59165086204d8fd3db8'
  cityId = '2638580'
  forecastUrl = 'https://api.openweathermap.org/data/2.5/forecast?id={}&APPID={}'.format(cityId, apiKey)
  forecastResponse = requests.get(url=forecastUrl)

  for forecast in forecastResponse.json().get('list'):
    forecastMinTempKelvin = int(forecast['main']['temp_min'])
    if forecastMinTempKelvin <= minTempThresholdKelvin:
      minTempThresholdHit = True
      forecastMinTempCelsius = round(forecastMinTempKelvin - zeroCelsiusInKelvin, 1)
      forecastDt = int(forecast['dt'])
      forecastDtFriendly = time.strftime('%H:%M on %a, %d %b %Y', time.localtime(forecastDt))
      print('{} at {}'.format(forecastMinTempCelsius, forecastDtFriendly))

  if not minTempThresholdHit:
    print('None')

except:
  print(sys.exc_info()[0])
