#!/usr/bin/python
import liblo
import sys
import time
from random import random
from optparse import OptionParser
from dreamlib import swirl
import pygame
"""
	Cerebro - an actuation tool for eeg from the Muse head band data via pygame
		tested and developed on a raspberry pi 3
	by Keith Makan

	License GPL
"""	

def eeg_callback(path, args,types,src,data):
	global active
	active = True	
	log_args(args)

def acc_callback(path,args,types,src,data):
	global active
	active = True	
	log_args(args)

def delta_callback(path,args,types,src,data):
	global active
	global packet_index
	global delta_level
	delta_level = args[0]
	packet_index += 1
	active = True
	print("delta:\t%d %s" % (packet_index,args[0]))

def alpha_callback(path,args,types,src,data):
	global active
	global packet_index
	global alpha_level
	packet_index += 1
	active = True
	alpha_level = args[0]

	print("alpha:\t%d %s" % (packet_index,args[0]))

def log_args(args):
	for arg in args:
		print "\t%s " % (arg),
	print
#to flesh out later when I'm adding command line options
def add_all(server):
	return
def add_absolutes(server):
	return
def add_alpha_only(server):
	server.add_method('/muse/elements/alpha_absolute','f',alpha_callback,"Abs Alpha Service")
#Add other call backs	
#TESTING CODE
if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("--alpha-out",
								dest="alpha_output_filename",\
								type="string",\
								action="store")

	parser.add_option("--beta-out",\
								dest="beta_output_filename",\
								type="string",\
								action="store")
	
	parser.add_option("--theta-out",\
								dest="theta_output_filename",\
								type="string",\
								action="store")

	parser.add_option("--delta-out",\
								dest="delta_output_filename",\
								type="string",\
								action="store")

	parser.add_option("--gamma-out",\
								dest="gamma_output_filename",\
								type="string",\
								action="store")

	parser.add_option("-s","--sprites",dest="sprites",action="store",type="int")
	parser.add_option("-p","--port",dest="port",action="store",type="int")
	parser.add_option("-a","--alpha",dest="alpha",action="store_true")
	parser.add_option("-b","--beta",dest="beta",action="store_true")
	parser.add_option("-d","--delta",dest="delta",action="store_true")
	parser.add_option("-t","--theta",dest="theta",action="store_true")
	parser.add_option("-g","--gamma",dest="gamma",action="store_true")
	options,args = parser.parse_args()

	active = False
	packet_index = 0
	if options.port != None:
		server_port = options.port
	else:
		server_port = 5000
	sys.stderr.write("[*] starting server on port %s\n" % (server_port))
	sys.stderr.flush()

	server = liblo.Server(server_port)
	if options.alpha:
		server.add_method('/muse/elements/alpha_absolute','f',alpha_callback,"Abs Alpha Service")
	if options.delta:
		server.add_method('/muse/elements/delta_absolute','f',delta_callback,"Abs Alpha Service")
	if options.beta:
		server.add_method('/muse/elements/beta_absolute','f',beta_callback,"Abs Alpha Service")
	#server.add_method('/muse/eeg','fffff',eeg_callback,"EEG Service")
	#server.add_method('/muse/acc','ffff',acc_callback,"ACC Service")
	#server.add_method('/muse/elements/theta_absolute','f',thetha_callback,"Abs Alpha Service")
	#server.add_method('/muse/elements/gamma_absolute','f',gamma_callback,"Abs Alpha Service")
	
	sys.stderr.write("[*] server started...\n")
	sys.stderr.flush()
	active = False
	event_index = 0

	timing_queue = []
	wait_start = time.time()
	first_run = False
	wait_index = 0
	pygame.init()
	pygame.font.init()
	myfont = pygame.font.SysFont("Comic Sans MS",30)
	title = myfont.render("CEREBRO",False,(255,255,255))
	author = myfont.render("by Keith Makan",False,(255,255,255))
	screen = pygame.display.set_mode((1000,500))

	if options.sprites:
		sprites = options.sprites
		swirls = [swirl(color=(255 - int(50*random()),255 - int(50*random()),255 - int(50*random())),width=(10 + int(random()*5)),radius=int(100 + random()*20),omega=random()*0.05,pos=(int(random()*10 + 1) + 50, int(random()*10 + 1) + 50),mod_max=400) for i in range(sprites)]
		swirls += [swirl(color=(255 - int(100*random()),255 - int(100*random()),255 - int(100*random())),width=(7 + int(random()*2)),radius=int(50 + random()*20),omega=random()*0.06,pos=(int(random()*10 + 1) + 50, int(random()*10 + 1) + 50),mod_max=400) for i in range(sprites/2)]
		swirls += [swirl(color=(255 - int(200*random()),255 - int(200*random()),255 - int(200*random())),width=(5 + int(random()*2)),radius=int(20 + random()*5),omega=random()*0.07,pos=(int(random()*10 + 1) + 50, int(random()*10 + 1) + 50),mod_max=400) for i in range(sprites/4)]
	else:
		sprites = 100
		swirls = [swirl(color=(255 - int(50*random()),255 - int(50*random()),255 - int(50*random())),radius=int(100 + random()*20),omega=random()*0.06,pos=(int(random()*10 + 1) + 50, int(random()*10 + 1) + 50),mod_max=400) for i in range(sprites)]
		swirls += [swirl(color=(255 - int(100*random()),255 - int(100*random()),255 - int(100*random())),radius=int(50 + random()*20),omega=random()*0.07,pos=(int(random()*10 + 1) + 50, int(random()*10 + 1) + 50),mod_max=400) for i in range(sprites/2)]
		swirls += [swirl(trail_len=2,color=(255 - int(200*random()),255 - int(200*random()),255 - int(200*random())),radius=int(20 + random()*5),omega=random()*0.08,pos=(int(random()*10 + 1) + 50, int(random()*10 + 1) + 50),mod_max=400) for i in range(sprites/3)]
	
	alpha_level = 0
	delta_level = 0
	sprites = 150
	loading_swirls = [swirl(sparkle=True,trail_len=2,width=int(5 + random()*2),color=(255 - int(200*random()),255 - int(200*random()),255 - int(200*random())),radius=int(10 + random()*5),omega=random()*0.07,pos=(int(random()*10 + 1) + 50, int(random()*10 + 1) + 50),mod_max=400) for i in range(sprites)]
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
		start = time.time()
		ret = server.recv(1)		
		if active:
			if first_run:
				wait_end = time.time()
				first_run = True
				sys.stderr.write("[*] server got first packet in '%s' seconds!" % (wait_end - wait_start))
				sys.stderr.flush()
			end = time.time()
			event_index+=1
			timing_queue.append((end - start))
			sys.stderr.write("\t\t\t%f %f %f\r" % ((end - start),sum(timing_queue),float(sum(timing_queue))/len(timing_queue)))
			sys.stderr.flush()
			if len(timing_queue) >= 400:
				timing_queue = []
		else:
			sys.stderr.write("waiting for connection %s\r" % (\
				["|","/","-","\\"][int(wait_index%4)]))
			wait_index += 1
		if active:
			for index,swirl in enumerate(swirls):
				if int(random()*100)%5 == 1:
					if options.delta:
						if int(delta_level*100) > 80: #bad case
							swirl.move_circle(radius_mod=(0.3 + delta_level))
							swirl.color = (swirl.color[0] + int( random()*(10 - swirl.color[0])),\
												swirl.color[1] + int( random()*(10 - swirl.color[1])),\
												swirl.color[2] + int( random()*(50 - swirl.color[2])))


							swirl.pulse_radius()
						else: #good case
							swirl.move_circle(radius_mod=abs(int(1+delta_level)))	
							if index%3 == 0:	
								swirl.color = (swirl.color[0] + int( random()*(205 - swirl.color[0])),\
												swirl.color[1] + int( random()*(127 - swirl.color[1])),\
												swirl.color[2] + int( random()*(50 - swirl.color[2])))
							else:
								swirl.color = (swirl.color[0] + int( random()*(255 - swirl.color[0])),\
												swirl.color[1] + int( random()*(127 - swirl.color[1])),\
												swirl.color[2] + int( random()*(0 - swirl.color[2])))

							swirl.pulse_radius()
							swirl.pulse_radius()
							swirl.pulse_radius()
							swirl.pulse_radius()
							swirl.pulse_radius()

							if options.alpha and abs(alpha_level - delta_level) > 5: #ideal
								swirl.move_circle(radius_mod=abs(int(alpha_level)))	
								swirl.color = (swirl.color[0] + int( alpha_level*(255 - swirl.color[0])),\
													swirl.color[1] + int( alpha_leve*(223 - swirl.color[1])),\
													swirl.color[1] + int( alpha_level*(0 - swirl.color[2])))

					#elif otions.alpha:
					#	swirl.move_cirlce(radius_mod=alpha_level)
					#	swirl.pulse_radius()
				
				swirl.pulse_radius()
				if swirl.r > 400:
						swirl.r = int(swirl.r*int(0.1 + random()))
				swirl.draw_swirl(screen)
		else:
			for swirl in loading_swirls:
				swirl.move_circle()	
				swirl.pulse_radius()
				swirl.pulse_radius()
				swirl.pulse_radius()
				swirl.pulse_radius()
				swirl.draw_swirl(screen)
				if swirl.r > 400:
						swirl.r = int(10 + random()*5)
			screen.blit(title,(450,250))
			screen.blit(author,(50,450))
		pygame.display.flip()
		screen.fill((0,0,0))
