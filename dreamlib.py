#!/usr/bin/python
import pygame
from time import sleep
from random import random
from math import sin,cos
import sys
class swirl:
	def __init__(self,pos=(100,100),radius=10,center=(500,250),omega=random()*0.09,angle=90,color=(255,100,0),radius_mod=1,mod_max=200,width=5):
		self.pos = pos
		self.r = radius
		self.omega = omega
		self.angle = angle
		self.center = center	
		self.color = color
		self.radius_mod = radius_mod 
		self.radius_mod_max = mod_max
		self.width = width
	def pulse_radius(self):
		if (int(random()*100)%5) == 1:
			self.r += random()*5*((0.8,0.15)[int(random()*10)%2])
	def move_circle(self,radius_mod=1):
		self.angle += self.omega
		self.pos = ((int(self.center[0]-(cos(self.angle) * (self.r*radius_mod)))),(int(self.center[1]-(sin(self.angle) * (self.r*radius_mod)))))
	def move_circle_phase(self,phase):
		self.angle += self.omega
		self.pos = ((int((phase*0.001*self.center[0])-(cos(self.angle) * (self.r)))),(int(phase*0.001*self.center[1]-(sin(self.angle) * (self.r)))))

	def move_ellipse(self,l,r):
		self.angle += self.omega
		self.pos = ((int(self.center[0]-(cos(self.angle) * (self.r*l)))),(int(self.center[1]-(sin(self.angle) * (self.r*r)))))
			
	def move_spiral(self,mod):
		self.move_circle(radius_mod=mod)
	
	def move_spiral_scale_up(self,factor):
		self.radius_mod = ((self.radius_mod + factor)*100 % self.radius_mod_max)/100.0
		print self.radius_mod
		self.move_circle(radius_mod=self.radius_mod)
	def draw_swirl(self,screen):
			#need to check for pygame import errors perhaps
			pygame.draw.circle(screen,self.color,self.pos,self.width)
def gen_random_swirl():
	return swirl(color=gen_random_color(base=(255,255,255)),radius=int(100 + random()*20),omega=random()*0.09,pos=(int(random()*10 + 1) + 100, int(random()*10 + 1) + 100),mod_max=400) 
def gen_random_color(base=(1,1,1)):
	return ((255 - (int(random()*100)%base[0]))%255,(255 - (int(random()*1000)%base[1]))%255,(255 - (int(random()*1000)%base[2]))%255)	

#implementation testing code
if __name__=="__main__":
	if len(sys.argv) < 2:
		print "./Usage: %s [sprites]" % (sys.argv[0])
		sys.exit(1)
	pygame.init()
	screen = pygame.display.set_mode((1000,500))
	swirls = [swirl(color=gen_random_color(base=(255,255,255)),radius=int(100 + random()*20),omega=random()*0.09,pos=(int(random()*10 + 1) + 100, int(random()*10 + 1) + 100),mod_max=400) for i in range(int(sys.argv[1]))]
	#swirl_alpha = swirl(radius=100,omega=0.09)
	done = False
	clock = pygame.time.Clock()
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

		for swirl in swirls:
			if int(random()*100)%5 == 1:
				swirl.pulse_radius()
			swirl.move_circle()
			pygame.draw.circle(screen,swirl.color,swirl.pos,int(random()*12 * (random()*1.5)))
		pygame.display.flip()
		clock.tick(20)
		screen.fill((0,0,0))
