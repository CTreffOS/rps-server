#!/bin/env python

import urllib2
import random
from time import sleep

SERVER = 'http://localhost:5001'

class testplayer():

	playername = None

	def __init__(self):
		try:
			self.playername = urllib2.urlopen('%s/register' % SERVER).read()
		except:
			print ('Init error')

	def run(self):
		if self.playername:
			while True:
				if self.playername == 'player1':
					player = 1
				else:
					player = 2
				choises = ['rock', 'paper', 'scissors']
				choise = choises[random.randint(0,3) % 3]
				try:
					result = urllib2.urlopen('%s/game/%i/%s' % (SERVER, player, choise)).read()
					if result == 'game over':
						break
				except:
					print ('Run error')

if __name__ == '__main__':
	testplayer().run()
