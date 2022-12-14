import socket
from json import dumps
from serves import *

HOST = 'localhost'
PORT = 8000
TOKEN = get_token()

message = {'type':'connect',
			'token':TOKEN
			}
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))
sock.send(dumps(message).encode())
data = sock.recv(1024)
if data == 'Connected':
	message = {'type': 'build',
			'token': TOKEN,
			'args': {'field': []}}
print(data.decode())