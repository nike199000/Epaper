#
# test sample met office code - need to convert to request()
#
#
# Distributed under MIT License
# 
# Copyright (c) 2020 Greg Brougham
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os   # for environ()
import requests
import geojson  # the structure for the data
import http.client  # redundant as using requests

# retrieve the access keys from the environment
met_id = os.environ.get('MET_ID')
met_key = os.environ.get('MET_KEY')

if (met_id == "" or met_key == ""):
    print ("Please set MET_ID and MET_KEY")
    exit(1)

#

meturl = "https://api-metoffice.apiconnect.ibmcloud.com"
conn = http.client.HTTPSConnection("api-metoffice.apiconnect.ibmcloud.com")

# embeds the secret and access key
headers = {
    'x-ibm-client-id': met_id,
    'x-ibm-client-secret': met_key,
    'accept': "application/json"
    }

# lat/long are the figures from the windguru custom location for the club
metreq = "/metoffice/production/v0/forecasts/point/hourly?excludeParameterMetadata=false&includeLocationName=false&latitude=51.469&longitude=-0.2199"

"""
conn.request("GET", "/metoffice/production/v0/forecasts/point/hourly?excludeParameterMetadata=false&includeLocationName=false&latitude=51.469&longitude=-0.2199", headers=headers)

res = conn.getresponse()
data = res.read()
"""

#print(data.decode("utf-8"))

# use requests to retrieve the forecast
req = requests.get(meturl + metreq, headers=headers)
print (req.status_code)
#print (req.json())

#rgeo = geojson(req.text)
rdict = req.json()

# the lenght is 3 as there are 3 blocks: type, features and parameters
print (len(rdict))

#for x in range(len(rdict)):
#    print (rdict[x][0])

x = 0
for feature in rdict['features']:
    print ("Loop: ", x)
    print (feature['type'])
    print (feature['geometry']['type'])
    print (feature['geometry']['coordinates'])
    print (feature['properties']['requestPointDistance'])
    print (feature['properties']['modelRunDate'])
    timeseries = feature['properties']['timeSeries']
    #print (feature['properties']['location']['name'])
    x = x + 1

print (len(timeseries))
"""
# list the timeseries entries
for tentry in timeseries:
    print (tentry['time'],
            " ", tentry['windSpeed10m'],
            " ", tentry['windGustSpeed10m'],
            " ", tentry['windDirectionFrom10m'],
            " ", tentry['screenTemperature'])
"""

# knots = m/s * 1.943844
# list next 6 hours
for x in range(6):
    print (timeseries[x]['time'],
            " ", round(timeseries[x]['windSpeed10m'] * 1.943844, 1),
            " ", round(timeseries[x]['windGustSpeed10m'] * 1.943844, 1),
            " ", timeseries[x]['windDirectionFrom10m'],
            " ", timeseries[x]['screenTemperature'])

type = rdict['type']
print (type)

fdict = rdict['features']
#type = fdict['type']
#print (type)
#location = rdict['features']['properties']['location']['name']
#print (location)

# end of file
