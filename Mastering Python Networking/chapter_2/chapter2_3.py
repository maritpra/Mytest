#!/usr/bin/python3

import paramiko
import getpass
import time

devices = {
    'R1': {'ip': '192.168.122.14'},
    'R4': {'ip': '192.168.122.252'}
    }
commands = ['show version\n', 'show run\n']

max_buffer = 10000
def clear_buffer(connection):
    if connection.recv_ready():
        return connection.recv(max_buffer)

username = input('Username: ')
password = getpass.getpass('Password: ')

for device in devices.keys():
    outputFileName = device + '_output.txt'
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(devices[device]['ip'], username=username, password=password, look_for_keys=False, allow_agent=False)
    new_connection = connection.invoke_shell()
    output = clear_buffer(new_connection)
    time.sleep(2)
    new_connection.send("term len 0\n")
    output = clear_buffer(new_connection)
    with open(outputFileName, 'wb') as f:
        for command in commands:
            new_connection.send(command)
            time.sleep(2)
            output = new_connection.recv(max_buffer)
            print(output)
            f.write(output)
    new_connection.close()
