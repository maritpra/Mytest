#!/usr/bin/env python3

import requests
import json

controller='https://sandboxapicdc.cisco.com'
user='admin'
password='ciscopsdt'

def gettoken(apic_ip, user, password):
    url = apic_ip + "/api/aaaLogin.json"
    payload = {
      "aaaUser":{
        "attributes":{
          "name":user,
          "pwd":password
        }
      }
    }
    header = {'content-type':'application/json'}
    response = requests.post(
      url,
      data= json.dumps(payload),
      headers= header,
      verify= False
    )
    r_json = response.json()
    token = r_json['imdata'][0]['aaaLogin']['attributes']['token']
    return token

thetoken = gettoken(controller, user, password)
#print(thetoken)
