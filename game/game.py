import sys

import pygame
from pygame.locals import *
from globals import *

field_one = [[None for i in range(10)] for i in range(10)]
field_two = [[None for i in range(10)] for i in range(10)]
field_two[0] = []



class Boat():
	size = 1
	rotated = False
	color = None
	rect = None
	default = None
	picked = False
	def __init__(self, x, y, color, rotated = False) -> None:
		self.color = color
		self.rect = Rect(x, y, step, step*self.size)
		self.default = [Rect(x, y, step, step*self.size), rotated, color]
		if rotated:
			self.rotate()
	
	def __str__(self) -> str:
		return f'{self.rect.x} {self.rect.y} {self.color} {self.rotated} {self.__class__.__name__}'
	
	def reset(self):
		self.rect = self.default[0]
		self.rotated = self.default[1]
		self.color = self.default[2]
		self.picked = False
	def rotate(self):
		self.rotated = not self.rotated
		if not self.rotated:
			self.rect.width = step
			self.rect.height = step*self.size
		else:
			self.rect.width = step*self.size
			self.rect.height = step
	
	def pick(self):
		self.picked = not self.picked
	
	def move(self,x,y,relative = False):
		if relative:
			self.rect.x += x
			self.rect.y += y
		else:
			self.rect.x = x
			self.rect.y = y
	
	def is_pick(self):
		return self.picked

	def is_rotated(self):
		return self.rotated

	def draw(self,screen):
		if self.picked:
			print(self.default)
		pygame.draw.rect(screen, self.color, self.rect)
class Destroyer(Boat):
	size = 2

class Cruiser(Boat):
	size = 3
class Ship(Boat):
	size = 4

def update(dt, boats):
	global field_one, field_two
	pos = pygame.mouse.get_pos()
	for boat in boats:
		if boat.picked:
			boat.move(pos[0]-boat.rect.width//2, pos[1]-boat.rect.height//2)
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				i = event.pos
				positon = (i[0],i[1])
				for boat in boats:
					if boat.picked:
						if pos[0] >= (width-100)//2:
							boat.reset()
							return
						boat.move(positon[0]//step*step, positon[1]//step*step)
						boat.pick()
						continue
					if boat.rect.collidepoint(*positon):
						boat.pick()
						continue
			elif event.button == 3:
				if pos[0] <= (width-100)//2:
					for boat in boats:
						if boat.rect.collidepoint(*event.pos):
							boat.rotate()
		if event.type == QUIT:
			pygame.quit()
			sys.exit()


def draw(screen, boats):
	global field_one, field_two
	screen.fill((0, 0, 0))
	for i in range(0, step*10+1, step):
		pygame.draw.line(screen,(255,255,255),(i,0),(i,height))
	for i in range(0, step*10+1,step):
		pygame.draw.line(screen,(255,255,255),(0,i),((width-100)//2-1,i))
	for boat in boats:
		boat.draw(screen)
	pygame.display.flip()

def runPyGame():
	
	pygame.init()
	
	fps = 60.0
	fpsClock = pygame.time.Clock()
	screen = pygame.display.set_mode((width, height))

	dt = 1/fps
	boats = [Boat(step*10+step*2*i,0,(0,255,0)) for i in range(1,6)] + [Destroyer(step*10+step*2*i,step*2,(0,255,0)) for i in range(1,5)] + [Cruiser(step*10+step*2*i,step*5,(0,255,0)) for i in range(1,4)] + [Ship(step*10+step*2,step*9,(0,255,0),True)]
	while True:
		update(dt ,boats)
		draw(screen, boats)
		dt = fpsClock.tick(fps)

if __name__ == '__main__':
	runPyGame()