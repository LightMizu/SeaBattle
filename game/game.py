import pygame
import sys
import socket
from globals import *
from json import dumps, loads

args = sys.argv[1:]
if not args:
	exit()
args = {'Token':args[0]}

field_opponent = [[(0,0,0) for _ in range(10)] for _ in range(10)]
class Network():
	host = None
	port = None
	token = None
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	def __init__(self, port, token, host = '127.0.0.1'):
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
	def shoot(self, x, y):
		message = {'type': 'shoot',
					'token': self.token}
		message['args'] = {'position':(y,x)}
		self.send(message)
		data = self.get()
		return data


def update(network):
	global field_opponent
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = event.pos
			if event.button == 1:
				positon = (pos[0]//step-11,pos[1]//step)
				data = network.shoot(*positon)
				x,y = positon[1], positon[0]
				print(data)
				match data:
					case 'Miss':
						field_opponent[x][y] = (150,50,50)
					case 'Hit':
						field_opponent[x][y] = (50,150,50)
					case 'Killed':
						pos = [(0,1),(0,-1),(1,0),(-1,0)]
						pos1 = [(-1,1),(1,-1),(1,1),(-1,-1)] + pos
						q = [(x,y)]
						print(x,y)
						while q:
							print(*field_opponent,sep = '\n')
							print(q)
							n = q[-1]
							q.pop()
							field_opponent[n[0]][n[1]] = (0,0,150)
							for i in pos:
								try:
									print(n[0]+i[0],n[1]+i[1])
									print(field_opponent[n[0]+i[0]][n[1]+i[1]])
									if field_opponent[n[0]+i[0]][n[1]+i[1]] == (50,150,50):
										q.append((n[0]+i[0],n[1]+i[1]))
								except IndexError:
									pass
							for j in pos1:
								try:
									if n[0]+j[0] >= 0 and n[1]+j[1] >= 0:
										field_opponent[n[0]+j[0]][n[1]+j[1]] = (0,0,150)
								except IndexError:
									pass
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

def draw(screen,field_one,field_two):

	for i in range(len(field_one)):
		for j, boat in enumerate(field_one[i]):
			pygame.draw.rect(screen,(boat*100,boat*255,boat*100),pygame.Rect(j*step,i*step,step,step))
	for i in range(len(field_two)):
		for j, boat in enumerate(field_two[i]):
			pygame.draw.rect(screen,boat,pygame.Rect((j+11)*step,i*step,step,step))         

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
	global field_opponent
	print(token)
	screen = pygame.display.set_mode((width,height))
	network = Network(8001,token)
	field = network.get_field()
	while True:
		draw(screen,field,field_opponent)
		update(network)

if __name__ == '__main__':
	if args.get('Token',None):
		main(args['Token'])

