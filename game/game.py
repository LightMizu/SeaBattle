import sys

import pygame
from pygame.locals import *
from globals import *

circle = []

def update(dt):
	global circle
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				i = event.pos
				step = height//10
				positon = (i[0]//step*step+step//2,i[1]//step*step+step//2)
				if not positon in circle:
					print(positon)
					if positon[0] < field_size:
						circle.append(positon)
		if event.type == QUIT:
			pygame.quit()
			sys.exit()


def draw(screen):
	global circle
	screen.fill((0, 0, 0))
	step  = height//10
	for i in range(0, step*10+1, step):
		pygame.draw.line(screen,(255,255,255),(i,0),(i,height))
	for i in range(0, step*10+1,step):
		pygame.draw.line(screen,(255,255,255),(0,i),((width-100)//2-1,i))
	for i in circle:
		pygame.draw.circle(screen,center=i,color=(255,0,0),radius = 10)
	pygame.display.flip()

def runPyGame():
	
	pygame.init()
	
	fps = 60.0
	fpsClock = pygame.time.Clock()
	screen = pygame.display.set_mode((width, height))

	dt = 1/fps
	while True:
		update(dt)
		draw(screen)
		dt = fpsClock.tick(fps)

if __name__ == '__main__':
	runPyGame()