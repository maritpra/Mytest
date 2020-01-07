#!/usr/bin/python3

import pexpect
import getpass

devices = {
    'R1': {'prompt': 'R1#', 'ip': '192.168.122.14'},
    'R2': {'prompt': 'R2#', 'ip': '192.168.122.25'}
    }
commands = ['term len 0', 'show version', 'show run']

username = input('Username: ')
password = getpass.getpass('Password: ')

for device in devices.keys():
    outputFileName = device + '_output.txt'
    device_prompt = devices[device]['prompt']
    child = pexpect.spawn('telnet ' + devices[device]['ip'])
    child.expect('Username')
    child.sendline(username)
    child.expect('Password')
    child.sendline(password)
    child.expect(device_prompt)
    with open('outputFileName', 'wb') as f:
        for command in commands:
            child.sendline(command)
            child.expect(device_prompt)
            f.write(child.before)
            child.logout()
            