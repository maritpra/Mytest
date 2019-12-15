#!/usr/bin/python3

import pexpect

devices = {
    'R1':{'prompt':'#R1', 'ip':'192.168.122.188'},
    'R2':{'prompt':'#R2', 'ip':'192.168.122.164'}
}
username="cisco"
password="cisco"

for device in devices.keys():
    device_prompt = devices[device['prompt']]
    child = pexpect.spawn('telnet ' + devices[device]['ip'])
    child.expect('Username')
    child.sendline('username')