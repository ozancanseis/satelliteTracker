# =========== MAGNETIC DECLINATON =========== #

#Learn Magnetic Declination with given Location

import json
import requests
import geocoder
from datetime import datetime 
from magnetic_field_calculator import MagneticFieldCalculator


def calculate_declination():

  calculator = MagneticFieldCalculator(
    model='wmm',
    revision='2020',
    sub_revision='2',
  )

  result = calculator.calculate(
    latitude=geocoder.ip('me').lat, # [deg]
    longitude=geocoder.ip('me').lng, # [deg],
    altitude=0,
    date=datetime.now().strftime("%Y-%m-%d")
  )

  print(json.dumps(result, indent=4, sort_keys=True)) 
  print(result["secular-variation"])

  return result["field-value"]["declination"]["value"]

  # try: 
  #   response = requests.get(hostname, params=params, headers=headers)
  #   # extract JSON payload of response as Python dictionary
  #   json_payload = response.json()
  #   # raise an Exception if we encoutnered any HTTP error codes like 404 
  #   response.raise_for_status()
  # except requests.exceptions.ConnectionError as e: 
  #   # handle any typo errors in url or endpoint, or just patchy internet connection
  #   print(e)
  # except requests.exceptions.HTTPError as e:  
  #   # handle HTTP error codes in the response
  #   print(e, json_payload['error'])
  # except requests.exceptions.RequestException as e:  
  #   # general error handling
  #   print(e, json_payload['error'])
  # else:
  #   json_payload = response.json()
  #   print(json.dumps(json_payload, indent=4, sort_keys=True))
  #   return json_payload["declination"]["value"]
