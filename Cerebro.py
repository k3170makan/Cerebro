#!/usr/bin/python
import liblo
import sys
import time
from random import random
"""
	Cerebro - an actuation tool for eeg from the Muse head band data via pygame
		tested and developed on a raspberry pi 3
	by Keith Makan

	License GPL

	TODO:
		1 - check out timing between eeg packet events
			: - do I need to seperate callbacks into different threads? all call backs into single thread?
			: - do I need to stack up packets? can I do band pass filtering in time?
		2 - once we have timing data starting building thread cycle
				1 - get eeg packet (server thread needs to signal when its done with a packet)
					* - probably need a server thread? does it need to run all the time?
				2 - calculate alpha 
					* - calculationso on main thread?
				3 - add to animation
					* - perhaps the display thread must just be seperate? 
						[?] - display thread checks an array to see if it must update the animation
								array has a sequence number for each packet so it knows which one its displayed already?
"""	
def eeg_callback(path, args,types,src,data):
	global active
	active = True	
	log_args(args)

def acc_callback(path,args,types,src,data):
	global active
	active = True	
	log_args(args)
def alpha_callback(path,args,types,src,data):
	global active
	global packet_index
	packet_index += 1
	active = True
	sys.stderr.write("%d %s\n" % (packet_index,args[0]))
	sys.stderr.flush()

def log_args(args):
	sys.stderr.write("\t%s  %s  %s  %s  %s\r" % (args[0],args[1],args[2],args[3],args[4]))
	sys.stderr.flush()	

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
	active = False
	packet_index = 0
	rand_port = 5000
	print("[*] starting server on port %s" % (rand_port))
	server = liblo.Server(rand_port)
	#server.add_method('/muse/eeg','fffff',eeg_callback,"EEG Service")
	#server.add_method('/muse/acc','ffff',acc_callback,"ACC Service")
	server.add_method('/muse/elements/alpha_absolute','f',alpha_callback,"Abs Alpha Service")
	#server.add_method('/muse/elements/beta_absolute','f',beta_callback,"Abs Alpha Service")
	#server.add_method('/muse/elements/theta_absolute','f',thetha_callback,"Abs Alpha Service")
	#server.add_method('/muse/elements/delta_absolute','f',delta_callback,"Abs Alpha Service")
	#server.add_method('/muse/elements/gamma_absolute','f',gamma_callback,"Abs Alpha Service")
	
	print("[*] server started...")
	event_index = 0
	wait_start = time.time()
	first_run = False
	while True:
		start = time.time()
		ret = server.recv(128)		
		if active:
			if first_run:
				wait_end = time.time()
				first_run = True
				print("[*] server got first packet in '%s' seconds!" % (wait_end - wait_start))
			end = time.time()
			event_index+=1
			print("%d %s" % (event_index,end - start))
