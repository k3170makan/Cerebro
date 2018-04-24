# Cerebro : PROJECT IN PROGRESS
![alt text](https://raw.githubusercontent.com/k3170makan/Cerebro/master/loading_screen2.png "loading screen")

##Brain art with raspberrypi and Mind Muse EEG
Cerebro is a digital mandala generator. It generates a mandala using
a pygame animation that evolves through color stages according to how relaxed you are. Some examples are shown below.

*This is a fun little, personal project of mine, its still a bit
clunky but it works to some extent, I'm sharing it here for those 
who would be able to use it in this state (Python, RaspberryPi, 
EEG Artists) so they can get in on the action!*


### Setting up Cerebro for Raspberry Pi
In order to get Cerebro going on your raspberry pi, all you need to do is
make sure you do these:

1. Install Muse Monitor for Android
2. Install pygame, python-liblo
3. Grab a copy of the Cerebro Github project

### Running and Visualizing your relaxtion state
You should now be good to go, the following runs cerebro and syncs with
the mind muse
1. Launch the Muse Monitor app on your Android, configure the OSC Streaming options to hit your Raspberry Pi.
2. Run it here's an example of a simple configuration that will use your alpha and delta waves to actuate - other modes have not been implemented yet

		```
			./Cerebro_dreamlib.py --alpha --delta --port 5000 --sprits 250
		```
This will spin up a Cerebro instance that hosts a UDP server on
port 5000 for data from the muse monitor app (this app follows the
MuseIO data standard so there's tons of things you can pull from it
and there also a usefull amount of info about it too!). 

You should see a screen like this show up:
	 	
DISCLAIMER: There's about a minute delay right now in getting it
	connected this, I'm working on getting around this.

Currently the idea is to meditate for a minute or so as deeply 
	as possible,either staring at the screen of your pi OR with 
	your eyes closed.

	After a minute or so you should see the state of your brain on the
	screen a minute ago - this is due to the delay. Although this ironically
	turns out to be an ideal mode of use for deep meditation, since you can
	only meditate so deeply with your eyes open :) and you wouldn't be able
	to see the spectacular art you're making then!!

### Using the Cerebro Stock Mandala

The Cerebro Animation I've included here is merely meant as a template
for the kind of stuff you can do with the 3 technologies here. The core
idea of Cerebro is that you are able to easily plugin in and script your
own visualations (and physical actuations - that will come later ;). But
 if you're interested in using the stock animation then here's how it works.
If you are in a non-relaxed state the mandala will look like this or disappear completely:
![alt text](https://raw.githubusercontent.com/k3170makan/Cerebro/master/low_alpha.png "low alpha")

When you are very relaxed and maintain this state for long enough it will
go through a couple of transitions in color and speed and eventually 
turn gold and look like this:

![alt text](https://raw.githubusercontent.com/k3170makan/Cerebro/master/high_alpha.png "high alpha")

Good luck and relax its easy :)!

### Depedencies
Cerebro is a project that ties together a couple things:
* Mind Muse EEG 2016 : https://www.amazon.com/Muse-Brain-Sensing-Headband-Black/dp/B00LOQR37C
* Muse Monitor for Android : https://play.google.com/store/apps/details?id=com.sonicPenguins.museMonitor
* PyGame :  https://www.pygame.org/news
* Raspberry Pi : https://www.raspberrypi.org/
* liblo OSC for Python: http://das.nasophon.de/pyliblo/

You need to get a muse device, ill add support for more as the need arises. But for now all is support is the Muse 2016, its as far as i know the most
bang for your buck in the dry electrode eeg game ;)

### TODO
Here's a couple of stuff I'm going to work on getting done in future in
case you where thinking of going off your own tangent in some ways i 
thought might be interesting ;) Happy thought hacking!!

1. FINISH THE TODO LIST lol
2. Add a replay and record mode - simple mode that plays your data back
		using a swirl you implement or the stock one included
3. Design implement swirl scripting API (possibly design an "inteface" to a swirl object definition so it can be scripted in certain ways)
4. Design arb game buliding api
5. implement api to hook into physical actuations pump out events like:
	* ideal (the user is attaning a good state)
	* negative (the user is moving away from ideal state)
	* maintain (keep the progress in the game steady) commands that the acutation handles in its own way. 
	
	example: a game where a user fills a cup to overflowing to win
			* ideal : full/overflowing cup
			* neurtral: cup empties instead
			* maintain : cup level doesnt change 
	here the physical actuation will obviously actuate what the script says
	about the user according to the brain waves.

	6. implement means to automatically learn ideal and baseline state
		and automatically spin up arbitrary games of a certain type

