import os
import pymongo
import json

import requests


def getzip(ip):

    # url = "http://api.ipstack.com/134.201.250.155"

    url = "http://api.ipstack.com/" +ip

    querystring = {"access_key":"GET YOUR OWN ACCESS KEY"}

    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "bede3c2d-122d-45e5-be2d-b86b9a32e9ad"
        }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    # print(response.text)

    jin = json.loads(response.text)

    if 'zip' in jin:
        z = jin['zip']
        state = jin['region_code']
    else:
        z = "-1"
        state = 'none'

    return z, state




def dummy(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.method == 'OPTIONS':
        # Allows GET requests from origin https://mydomain.com with
        # Authorization header
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)

    # Set CORS headers for main requests
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    }

    request_json = request.get_json()
    mongostr = os.environ.get('MONGOSTR')
    client = pymongo.MongoClient(mongostr)
    db = client["greenergy"]
    col = db.powerprofile
    results = []
    maxid = 0


    egridsub = ""


    # action = request_json['action']

    ipaddress = request_json['ip']

    zipcode, state = getzip(ipaddress)

    for x in col.find():
        if zipcode == x['ZIP (character)']:
            egridsub = x['eGRID Subregion #1']
            break
        maxid +=1
    
    col = db.emissionsbystate

    for x in col.find():
        if state == x['state']:
            co2 = x['CO2']
            ch4 = x['CH4']
            n20 = x['N20']
            ozone = x['Ozone']
            so2 = x['SO2']

            break

    
    col = db.egridfuelmix

    for x in col.find():
        if egridsub == x['egrid']:
            coal = x['coal']
            oil = x['oil']
            gas = x['gas']
            otherfossil = x['otherfossil']

            nuclear = x['nuclear']
            hydro = x['hydro']
            biomass = x['biomass']
            solar = x['solar']
            wind = x['wind']
            geothermal= x['geothermal']

    
    retjson = {}

    retjson['egridsub'] = egridsub
    retjson['state'] = state
    retjson['co2'] = co2
    retjson['ch4'] = ch4
    retjson['n20'] = n20
    retjson['ozone'] = ozone
    retjson['so2'] = so2

    retjson['coal'] = coal
    retjson['oil'] = oil
    retjson['gas'] = gas
    retjson['otherfossil'] = otherfossil
    retjson['nuclear'] = nuclear
    retjson['hydro'] = hydro
    retjson['biomass'] = biomass
    retjson['solar'] = solar
    retjson['wind'] = wind
    retjson['geothermal'] = geothermal


    
    # retjson['mongoresult'] = str(maxid)

    return json.dumps(retjson)


    retstr = "action not done"

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return retstr
