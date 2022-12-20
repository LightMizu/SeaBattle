import sys

import pygame
from pygame.locals import *
from globals import *
from copy import deepcopy
from loguru import logger 


class Button():
	color = None
	rect = None

	def __init__(self, x, y, w, h , color) -> None:
		self.rect = Rect(x, y, w, h)
		self.color = color
	def is_click(self, x, y):
		return self.rect.collidepoint(x,y)
	def draw(self, screen):
		logger.info(f'Button drawing in {self.rect} {self.color}')
		pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
		pygame.display.flip()
class Boat():
	size = 1
	rotated = False
	color = None
	rect = None
	default = None
	picked = False
	def __init__(self, x, y, color, rotated = False) -> None:
		self.color = color
		self.rect = Rect(x, y, step+1, step*self.size+1)
		self.rotated = rotated
		if rotated:
			self.rotate(False)
		self.default = [deepcopy(self.rect), self.rotated, color]
	
	def __str__(self) -> str:
		return f'{self.rect.x} {self.rect.y} {self.color} {self.rotated} {self.__class__.__name__}'
	
	def reset(self):
		self.rect = deepcopy(self.default[0])
		
		self.rotated = deepcopy(self.default[1])
		logger.info('Resetting')
		logger.info(f'{self.default[0]} {self.rotated} {self.default[2]}')
		self.color = deepcopy(self.default[2])
		self.picked = False

	def rotate(self, change = True):
		if change:
			self.rotated = not self.rotated
		if not self.rotated:
			self.rect.width = step+1
			self.rect.height = step*self.size+1
		else:
			self.rect.width = step*self.size+1
			self.rect.height = step+1
	def is_on_field(self):
		field = Rect(0, 0, field_size+step, field_size+step)
		return field.collidepoint(self.rect.topright) and field.collidepoint(self.rect.topleft) and field.collidepoint(self.rect.bottomleft) and field.collidepoint(self.rect.bottomright)

	def pick(self,boats):
		collaide = self.rect.collidelistall(boats)
		logger.info(f"Self rect collide with {collaide}")
		if not self.rect.colliderect(Rect((width-step)//2+1, 0, field_size+step*2, field_size+step*2)):
			if len(collaide) == 1:
				self.picked = not self.picked
		elif self.rect == self.default[0]:
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
		pygame.draw.rect(screen, self.color, self.rect)
class Destroyer(Boat):
	size = 2

class Cruiser(Boat):
	size = 3
class Ship(Boat):
	size = 4

def update(dt, boats):
	global field_one, field_two
	ans = False
	flag = True
	pos = pygame.mouse.get_pos()
	for boat in boats:
		if boat.picked:
			boat.move(pos[0], pos[1])
			flag = False
			continue
		if boat.rect.colliderect(Rect((width-step)//2+1, 0, field_size+step*2, field_size+step*2)):
			flag = False
	if flag:
		ans = True
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				i = event.pos
				positon = (i[0],i[1])
				for boat in boats:
					if boat.picked:
						if pos[0] >= (width-step)//2:
							boat.reset()
							return
						boat.move(pos[0]//step*step, pos[1]//step*step)
						boat.pick(boats)
						continue
					if boat.rect.collidepoint(*positon):
						boat.pick(boats)
						continue
			elif event.button == 3:
				for boat in boats:
					if boat.picked and boat.rect.collidepoint(*event.pos):
						boat.rotate()
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	return ans


def draw(screen, boats, buttons):
	screen.fill((0, 0, 0))
	for boat in boats:
		boat.draw(screen)
	for i in range(0, step*10+1, step):
		pygame.draw.line(screen,(255,255,255),(i,0),(i,height))
	for i in range(0, step*10+1,step):
		pygame.draw.line(screen,(255,255,255),(0,i),((width-step)//2,i))
	for button in buttons:
		button.draw(screen)
	
	pygame.display.flip()

@logger.catch
def runPyGame():
	
	pygame.init()
	
	fps = 60.0
	fpsClock = pygame.time.Clock()
	screen = pygame.display.set_mode((width, height))
	
	dt = 1/fps
	
	buttons = []
	boats = [Boat(step*10+step*2*i,0,(0,255,0)) for i in range(1,5)] + [Destroyer(step*10+step*2*i,step*2,(0,255,0)) for i in range(1,4)] + [Cruiser(step*10+step*2*i,step*5,(0,255,0)) for i in range(1,3)] + [Ship(step*10+step*2,step*9,(0,255,0),True)]
	while True:
		Do = update(dt ,boats)
		draw(screen, boats, buttons)
		if Do:
			buttons = [Button(field_size*2-step*1.35,field_size-step*1.25,100,50,(100,255,100))]
		else:
			buttons = []
		dt = fpsClock.tick(fps)

if __name__ == '__main__':
	runPyGame()