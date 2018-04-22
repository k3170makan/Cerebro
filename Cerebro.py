#!/usr/bin/python
import liblo
import sys
import time
from random import random
from optparse import OptionParser
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
	print("%d %s" % (packet_index,args[0]))

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
	#server.add_method('/muse/eeg','fffff',eeg_callback,"EEG Service")
	#server.add_method('/muse/acc','ffff',acc_callback,"ACC Service")
	server.add_method('/muse/elements/alpha_absolute','f',alpha_callback,"Abs Alpha Service")
	#server.add_method('/muse/elements/beta_absolute','f',beta_callback,"Abs Alpha Service")
	#server.add_method('/muse/elements/theta_absolute','f',thetha_callback,"Abs Alpha Service")
	#server.add_method('/muse/elements/delta_absolute','f',delta_callback,"Abs Alpha Service")
	#server.add_method('/muse/elements/gamma_absolute','f',gamma_callback,"Abs Alpha Service")
	
	sys.stderr.write("[*] server started...\n")
	sys.stderr.flush()
	event_index = 0
	timing_queue = []
	wait_start = time.time()
	first_run = False
	wait_index = 0
	while True:
		start = time.time()
		ret = server.recv(64)		
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
			if len(timing_queue) >= 100:
				timing_queue = []
		else:
			sys.stderr.write("waiting for connection %s\r" % (\
				["|","/","-","\\"][int(wait_index%4)]))
			wait_index += 1
