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
  return {'APIC-Cookie':token}

def gettenant(apic_ip, cookie):
  url = apic_ip + "/api/node/class/fvTenant.json"
  #header = {'content-type':'application-json', 'X-Auth-Token':cookie}
  #header = {'content-type':'application-json', 'APIC-Cookie':token}
  #payload = {}
  response = requests.get(url, cookies=cookie, verify=False)
  r_json = response.json()
  return r_json

thetoken = gettoken(controller, user, password)
print(thetoken)
tenants = gettenant(controller, thetoken)
print(tenants)