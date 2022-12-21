import socket
import select
from json import loads, dumps

players = []
field = {}
def process(data, connect):
	global players
	data = loads(data)
	match data['type']:
		case 'echo':
			connect.send(b'Success')
		case 'connect':
			token = data['token']
			if token in players:
				connect.send(b'You already connected')
			elif len(players) >= 2:
				connect.send(b'Maximum number of players')
			else:
				players.append(token)
				connect.send(b'Success')
		case 'build':
			token = data['token']
			if not token in field:
				field[token] = data['args']['field']
				print(f'{token} ', *data['args']['field'], sep='\n')
				connect.send(b'Success')
		case 'get_field':
			try:
				connect.send(dumps({'field': field[data['token']]}).encode())
			except KeyError:
				connect.send(b'No access')

s = socket.socket()
s.bind(('',8001))
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
				# read from a client
				data = rs.recv(1024)
				if not data:
					print('\r{}:'.format(rs.getpeername()),'disconnected')
					readable.remove(rs)
					rs.close()
				else:
					process(data, rs)