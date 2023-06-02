import socket
import os, os.path
import subprocess
import time
from collections import deque    
import random


sock_name = '/slick/control'
pier_path = '/home/amadeo/learn_hoon/tasseg-sophec-mopfel-winrux/'
vere_path = '/home/amadeo/learn_hoon/urbit-test'

sock_path = pier_path+'.urb/dev/'+sock_name


sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect(sock_path)

data="[%control %space]"
p = subprocess.Popen([vere_path, 'eval' ,'-jn', '--loom' ,'25'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout_data, stderr_data = p.communicate(input=data.encode())

sock.send(stdout_data)


while True:
    data = sock.recv(1024*2)
    p = subprocess.Popen([vere_path, 'eval' ,'-cn', '--loom' ,'25'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate(input=data)
    mark = stdout_data.decode().split(' ')[0][1:]
    noun = stdout_data.decode().split(' ')[1:]
    noun = ' '.join(noun)[:-1]
    if(mark == '%init'):
        print(f"init: {noun[:-1]}")
    if(mark == '%state'):
        print(noun)
    #data="[%control %r]"
    #p = subprocess.Popen([vere_path, 'eval' ,'-jn', '--loom' ,'25'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #stdout_data, stderr_data = p.communicate(input=data.encode())
