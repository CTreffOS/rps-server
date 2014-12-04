from flask import Flask, jsonify
from time import sleep, time
import redis


# Create aplication
app = Flask(__name__)


MAX_GAMES = 1000
DATABASE = 'rps-server.db'

def calc(id, player, r):
	''' Calculate the winner of a game.

	Returns a tupel of a string and a boolean.
	The string is the choice of the other player.
	The boolean ist true if id won the game and false otherwise.
	If the Input is wrong, the function  logs an error.
	'''

	value1 = r.get('%s:current' % id)
	if str(id) == player[0]:
		value2 = r.get('%s:current' % player[1])
	else:
		value2 = r.get('%s:current' % player[0])

	if value1 == value2:
		return (value2, False)
	elif value1 == 'rock':
		if value2 == 'paper':
			return (value2, False)
		if value2 == 'scissors':
			return (value2, True)
	elif value1 == 'paper':
		if value2 == 'scissors':
			return (value2, False)
		if value2 == 'rock':
			return (value2, True)
	elif value1 == 'scissors':
		if value2 == 'rock':
			return (value2, False)
		if value2 == 'paper':
			return (value2, True)
	r.set('error', 'ERRORCODE 4')
	return ('', False)


@app.route('/')
def info():
	'''Manage the output of this server.
	If an error occurs this function return this error
	While the game is not over this function return playing
	Otherwise this function returns the result the won games by each player in
	json. For example if the player 123 won 12 games and the player 321 won 11
	games the output is the dictionary {123 : 12, 321 : 11}.

	HTTP return codes:

		====  =====================  =====================
		Code  Status                 Meaning
		====  =====================  =====================
		200   OK                     Return result
		====  =====================  =====================
	'''

	r = redis.StrictRedis(host='localhost', port=6379, db=0)

	# Check for error
	error = r.get('error')
	if error:
		return error, 200

	# Check for number of played games
	played = int(r.get('played'))
	if not played == 2* MAX_GAMES:
		return 'playing', 200

	# Get player
	player = r.lrange('player', 0, -1)

 	# Get result
	result = {}
	for p in player:
		result[p] = r.get('%s:won' % p)
	return jsonify(result), 200


@app.route('/<int:id>/<choice>')
def game(id, choice):
	'''Function to call for a game. This function waits until both player has chosen.

	player is the integer of the player, so possible values are 1 and 2
	choice is the choice of the player limited to rock, paper and scissors

	Returns if the player that call this function has won, lost oder draw.

	HTTP return codes:

		====  =========  ============
		Code  Status     Meaning
		====  =========  ============
		200   OK         game played
		404   NOT FOUND  game is over
		====  =========  ============
	'''

	r = redis.StrictRedis(host='localhost', port=6379, db=0)

	# Check errorstatus
	error = r.get('error')
	if error:
		return 'game over', 404

	# Get player
	player = r.lrange('player', 0, -1)

	# Check id
	if not str(id) in player:
		r.set('error', 'ERRORCODE 1')
		return 'game over', 404

	# Check number of players
	if not len(player) == 2:
		r.set('error', 'ERRORCODE 2')
		return 'game over', 404

	# Check number of played games
	played = int(r.get('played'))
	if played == 2*MAX_GAMES:
		return 'game over', 404

	# Check choice
	if not choice in ['rock', 'paper', 'scissors']:
		r.set('error', 'ERRORCODE 3 ; ID %s', id)
		return 'game over', 404

	# Check current
	if r.get('%s:current' % id):
		return 'current already set', 200

	# Set current
	r.set('%s:current' % id, choice)

	# Sleep until all player has chosen
	while not (r.exists('%s:current' % player[0]) and r.exists('%s:current' % player[1])):
		sleep(0.00000001)

	# Calculate result
	(ret, won) = calc(id, player, r)

	# If won
	if won:
		r.incr('%s:won' % id)

	# Increase number of played games (This is done twice.)
	r.incr('played')

	# Wait until both players are ready with calculation
	while not (played == int(r.get('played')) - 2):
		sleep(0.00000001)

	# Delete own current
	r.delete('%s:current' % id)

	# Return choice of the other player
	return ret, 200


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=4441, threaded=True)
