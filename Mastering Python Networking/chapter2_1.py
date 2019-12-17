#!/usr/bin/python3

import pexpect

devices = {
    'R1':{'prompt':'#R1', 'ip':'192.168.122.14'},
    'R2':{'prompt':'#R2', 'ip':'192.168.122.25'}
}
username="cisco"
password="cisco"

for device in devices.keys():
    device_prompt = devices[device]['prompt']
    child = pexpect.spawn('telnet ' + devices[device]['ip'])
    child.expect('Username')
    child.sendline(username)
    child.expect('Password')
    child.sendline(password)
    child.expect(device_prompt)
    child.sendline('show ver | i V')
    child.expect(device_prompt)
    print(child.before)
    child.sendline('exit')