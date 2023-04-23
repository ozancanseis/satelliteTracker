# =========== MAGNETIC DECLINATON =========== #

#Learn Magnetic Declination with given Location

import json
import requests
import geocoder
from datetime import datetime 

def calculate_declination():

  headers = {"API-Key" : "HxiQaAuMQ2A6TCN8HwO8eK4UtsiEIryb"}

  hostname = "https://geomag.amentum.io/wmm/magnetic_field"


  params = dict(
      altitude = 0, # [km]
      longitude = geocoder.ip('me').lng, # [deg]
      latitude = geocoder.ip('me').lat, 
      year = datetime.now().year # decimal year, half-way through 2020
  )

  try: 
    response = requests.get(hostname, params=params, headers=headers)
    # extract JSON payload of response as Python dictionary
    json_payload = response.json()
    # raise an Exception if we encoutnered any HTTP error codes like 404 
    response.raise_for_status()
  except requests.exceptions.ConnectionError as e: 
    # handle any typo errors in url or endpoint, or just patchy internet connection
    print(e)
  except requests.exceptions.HTTPError as e:  
    # handle HTTP error codes in the response
    print(e, json_payload['error'])
  except requests.exceptions.RequestException as e:  
    # general error handling
    print(e, json_payload['error'])
  else:
    json_payload = response.json()
    print(json.dumps(json_payload, indent=4, sort_keys=True))
    return json_payload["declination"]["value"]
