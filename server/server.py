import socket
import select
from json import loads, dumps
from random import choice

players = []
fields = {}
turn = None
def process(data, connect):
	global players, turn, fields
	data = loads(data)
	match data['type']:
		case 'echo':
			connect.send(b'Success')
		case 'build':
			token = data['token']
			if not token in fields and len(players) < 2:
				fields[token] = data['args']['field']
				players.append(token)
				print(f'{token} ', *data['args']['field'], sep='\n')
				connect.send(b'Success')
			if len(players) == 2:
				if not turn:
					turn = choice(players)
					print(turn)
				else:
					connect.send(b'Max players')
		case 'get_field':
			try:
				connect.send(dumps({'field': fields[data['token']]}).encode())
			except KeyError:
				connect.send(b'No access')
		case 'shoot':
			token = data['token']
			if not turn:
				print('Ждём 2 игрока')
				connect.send(b'Waiting 2 player')
			else:
				if token in players:
					if turn == token:
						field = fields[players[players.index(turn)-1]]
						x,y = data['args']['position']
						pos = [(0,1),(0,-1),(1,0),(-1,0)]
						h = set()
						if field[x][y] == 2:
							print('Repeat')
							connect.send(b'Repeating')
						elif field[x][y] == 0:
							turn = players[players.index(turn)-1]
							print('Miss')
							connect.send(b'Miss')
						elif field[x][y] == 1:
							field[x][y] = 2
							h.add((x,y))
							q = [(x,y)]
							while q:
								n = q[-1]
								q.pop()
								for i in pos:
									try:
										if (field[n[0]+i[0]][n[1]+i[1]] == 2 or field[n[0]+i[0]][n[1]+i[1]] == 1) and ((n[0]+i[0],n[1]+i[1]) not in h):
											q.append((n[0]+i[0],n[1]+i[1]))
											h.add((n[0]+i[0],n[1]+i[1]))
									except IndexError:
										pass
							h = list(h)
							k = 0
							for i in h:
								if field[i[0]][i[1]] == 2: k+=1
							if k == len(h):
								print('Killed')
								connect.send(b'Killed')
							else:
								print('Hit')
								connect.send(b'Hit')
					else:
						connect.send(b'Not you turn')
				

s = socket.socket()
s.bind(('127.0.0.1',8001))
s.listen(1)
readable = [s] # list of readable sockets.  s is readable if a client is waiting.
i = 0
with s:
	while True:
		# r will be a list of sockets with readable data
		try:
			r,w,e = select.select(readable,[],[],0)
		except KeyboardInterrupt:
			s.close()
			break
		for rs in r: # iterate through readable sockets
			if rs is s: # is it the server
				c,a = s.accept()
				print('\r{}:'.format(a),'connected')
				readable.append(c) # add the client
			else:
				try:
					data = rs.recv(1024)
				except socket.error:
					pass
				else:
					if not data:
						print('\r{}:'.format(rs.getpeername()),'disconnected')
						readable.remove(rs)
						rs.close()
					else:
						process(data, rs)