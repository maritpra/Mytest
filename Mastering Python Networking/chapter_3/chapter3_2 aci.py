#!/usr/bin/env python3

import requests
import json

url='http://sbx-nxos-mgmt.cisco.com/ins'
switchuser='admin'
switchpassword='Admin_1234!'

myheaders={'content-type':'application/json-rpc'}
payload=[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show version",
      "version": 1
    },
    "id": 1
  }
]
response = requests.post(
    url,
    data=json.dumps(payload), 
    headers=myheaders,
    auth=(switchuser,switchpassword)
).json()
print(response['result']['body']['sys_ver_str'])