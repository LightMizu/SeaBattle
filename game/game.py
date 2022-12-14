import sys

import pygame
from pygame.locals import *
from globals import *


def update(dt):

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()


def draw(screen):
	screen.fill((0, 0, 0))
	for i in range(0, 801, 80):
		pygame.draw.line(screen,(255,255,255),(i,0),(i,height-100))
	for i in range(0, height-99,(height-100)//10):
		pygame.draw.line(screen,(255,255,255),(0,i),(800,i))

	for i in range(900, 1701, 80):
		print(i)
		pygame.draw.line(screen,(255,255,255),(i,0),(i,height-100))
	for i in range(0, height-99,(height-100)//10):
		pygame.draw.line(screen,(255,255,255),(900,i),(1700,i))
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