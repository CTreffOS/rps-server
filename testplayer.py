from urllib2 import urlopen
from random import randint
from sys import argv

SERVER = 'http://localhost:4441'

class testplayer():
	def run(self, id):
		while True:
			choices = ['rock', 'paper', 'scissors']
			choice = choices[randint(0,2)]
			try:
				result = urlopen('%s/%i/%s' % (SERVER, id, choice)).read()
			except:
				break


if __name__ == '__main__':
	if len(argv) == 2:
		testplayer().run(int(argv[1]))
	else:
		print('Wrong arguments')
