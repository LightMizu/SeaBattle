import pygame
import sys
import socket
from globals import *
from json import dumps, loads

args = sys.argv[1:]
if not args:
	exit()
args = {'Token':args[0]}


class Network():
	host = None
	port = None
	token = None
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	def __init__(self, port, token, host = ''):
		self.host = host
		self.port = port
		self.token = token
		self.sock.connect((host,port))
	def send(self,message):
		self.sock.send(dumps(message).encode())
	def get(self):
		data = self.sock.recv(1024)
		return data.decode()
	def get_field(self) -> list:
		message = {'type': 'get_field',
					'token': self.token}
		self.send(message)
		data = self.get()
		if data != 'No access':
			data = loads(data)
			return data['field']
		else:
			return []

def update():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

def draw(screen,field_one,field_two):

	for i in range(len(field_one)):
		for j, boat in enumerate(field_one[i]):
			pygame.draw.rect(screen,(boat*100,boat*255,boat*100),pygame.Rect(j*step,i*step,step,step))
	for i in range(len(field_two)):
		for j, boat in enumerate(field_two[i]):
			pygame.draw.rect(screen,(boat*255,boat*100,boat*100),pygame.Rect((j+11)*step,i*step,step,step))         

	for i in range(0,height,step):
		pygame.draw.line(screen,(255,255,255),(0,i),((width-step)//2,i))
	for i in range(0,(width-step)//2+1,step):
		pygame.draw.line(screen,(255,255,255),(i,0),(i,height))
	
	for i in range(0,height,step):
		pygame.draw.line(screen,(255,255,255),((width-step)//2+step,i),(width,i))
	for i in range((width-step)//2+step,width,step):
		pygame.draw.line(screen,(255,255,255),(i,0),(i,height))
	pygame.display.update()

def main(token):
	print(token)
	screen = pygame.display.set_mode((width,height))
	network = Network(8001,token)
	field = network.get_field()
	while True:
		draw(screen,field,[])
		update()

if __name__ == '__main__':
	if args.get('Token',None):
		main(args['Token'])

