import os
import platform
import socket
import subprocess

from sendrecv import *


def method():
    print('What do you want to do: ')
    print('1 - Make server')
    print('2 - Connect to another pc')
    print('0 - Exit')
    print("\n*Both pc's should connected to one router*\n")
    action = input('>>> ')
    make_folders()

    if action == '1':
        make_server()
    elif action == '2':
        connect()
    elif action == '0':
        exit_func()
    else:
        print('Input is incorrect. Try again.')
        method()

def do():
    print('1 - Send file')
    print('2 - Receive file')
    print('0 - Exit')
    action = input('>>> ')
    try:
        if server:
            if action == '1':
                server_send(con)
            elif action == '2':
                server_receive(con)
            elif action == '0':
                exit_func()
            else:
                print('Input is incorrect. Try again.')
                do()
    except:            
        if client:
            if action == '1':
                client_send(client)
            elif action == '2':
                client_receive(client)
            elif action == '0':
                exit_func()
            else:
                print('Input is incorrect. Try again.')
                do()
    
def make_folders():
    folder_1 = ('/ReceivedFiles')
    folder_path1 = str(os.path.dirname(os.path.realpath(__file__))) + folder_1
    if not os.path.exists(folder_path1):
        os.makedirs(folder_path1)

def make_server():
    global server, con
    ipv4 = ipv4_address()
    host = (ipv4, 8000)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(host)
    server.listen(1)
    print('Waiting for connection...')
    con, addr = server.accept()
    print('\nGot connection from ' + str(addr))
    do()

def connect():
    global client
    ipv4 = input('please enter host local ipv4 address: ')
    host = (ipv4, 8000)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(host)
    do()

def ipv4_address():
    ipv4 = osfinder()
    print('Your local ipv4 address is : ' + ipv4 + '. Enter this ip address on client pc.')
    print('If it is wrong enter ipv4 manually')
    print("\n1 - It's correct continue")
    print("2 - It's wrong")
    action = input('>>> ')
    if action == '1':
        pass
    elif action == '2':
        ipv4 = input('Enter your local ipv4: ')
    else:
        print('Input is incorrect. Try again.')
        ipv4_address()
    return ipv4

def ipfinder_win():
    ipconfig = list()
    ip = subprocess.check_output('ipconfig', shell=True, universal_newlines=True)
    ip = str(ip)
    ip = ip.splitlines()
    for i in ip:
        if 'IPv4 Address' in i:
            ip = i.strip()
            ip = ip.split(': ')
            ipconfig.append(ip)
    ipv4 = ipconfig[len(ipconfig)-1][1]
    return ipv4

def ipfinder_lin():
    ipconfig = list()
    try:
        ip = subprocess.check_output('ifconfig | grep "inet "', shell=True, universal_newlines=True)
    except:
        pass
    ip = str(ip)
    ip = ip.strip().split(' ')
    for i in ip:
        try:
            if i[0] in '1234567890':
                ipv4 = i
                break
        except:
            pass
    return ipv4

def osfinder():
    osname = platform.system()
    if osname.lower() == 'windows':
        return ipfinder_win()
    elif osname.lower() == 'linux':
        return ipfinder_lin()

def exit_func():
    print('Exiting program... ')
    exit()

method()