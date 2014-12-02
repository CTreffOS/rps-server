from flask import Flask, jsonify
from time import sleep
import sqlite3
import logging


# Create aplication
app = Flask(__name__)


MAX_GAMES = 1000
DATABASE = 'rps-server.db'
LOGFILE = 'rps-server.log'

logging.basicConfig(filename=LOGFILE,level=logging.WARNING)

def calc(value1, value2):
	''' Calculate the winner of a game.

	value1 is the choice of player1 limited to rock, paper or scissors
	value2 is the choice of player2 limited to rock, paper or scissors

	Returns a tupel of 2 strings. The first value is the game result of player1
	and the second value is the game result of player2. Possible results are
	won, lost and draw.
	If the Input is wrong, the function returns error'''
	if value1 == value2:
		return ('draw', 'draw')
	elif value1 == 'rock':
		if value2 == 'paper':
			return ('lost', 'won')
		elif value2 == 'scissors':
			return ('won', 'lost')
	elif value1 == 'paper':
		if value2 == 'rock':
			return ('won', 'lost')
		elif value2 == 'scissors':
			return ('lost', 'won')
	elif value1 == 'scissors':
		if value2 == 'rock':
			return ('lost', 'won')
		elif value2 == 'paper':
			return ('won', 'lost')
	return 'error'


def read_db():
	db = sqlite3.connect(DATABASE, check_same_thread=False)
	cur = db.execute('SELECT * FROM player')
	player = cur.fetchall()
	if not len(player) == 2:
		logging.error('Not the correct number of players')
	if not len(player[0]) == 5 and len(player[1]) == 5:
		logging.error('Not the correct number of informations about player')
	player = {player[0][0] : { 'win' : player[0][1], 'played' : player[0][2],
		'current' : player[0][3], 'error' : player[0][4]}, player[1][0] : { 'win'
			: player[1][1], 'played' : player[1][2], 'current' : player[1][3],
			'error' : player[0][4]}}
	db.close()
	return player


def update_db(id, new):
	db = sqlite3.connect(DATABASE, check_same_thread=False)
	for n in new:
			cur = db.execute('UPDATE player set %s = \"%s\" where id=%s' % (n, new[n], id))
	db.commit()
	db.close()
	return True


@app.route('/')
def info():
	'''Output.

	HTTP return codes:

		====  =====================  =====================
		Code  Status                 Meaning
		====  =====================  =====================
		200   OK                     Nothing
		====  =====================  =====================
	'''

	player = read_db()
	return jsonify(player), 200


@app.route('/<int:id>/<choice>')
def game(id, choice):
	'''Function to call for a game. This function waits until both player has chosen.

	player is the integer of the player, so possible values are 1 and 2
	choice is the choice of the player limited to rock, paper and scissors

	Returns if the player that call this function has won, lost oder draw.

	HTTP return codes:

		====  =====================  ======================
		Code  Status                 Meaning
		====  =====================  ======================
		200   OK                     Game over, game played
		400   BAD REQUEST            player, choice wrong
		403   FORBIDDEN              Already chosen
		404   NOT FOUND              Not enought player
		====  =====================  ======================
'''
	# Get player
	player = read_db().get(id)
	if not player:
		logging.error('Somebody used the wrong id')
		return '', 400

	# Check number of played games
	if player.get('played') == MAX_GAMES:
		return 'game over', 404

	# Check choise
	if not choice in ['rock', 'paper', 'scissors']:
		logging.error('Wrong choise from %s' % id)
		return '', 400

	if player.get('current'):
		logging.warning('current already set from %s' % id)
		return '', 403

	player['current'] = choice
	update_db(id, {'current' : choice})

	return '', 200
'''
		player1['current'] = choice
		while not player2['current']:
			sleep(0.01)
		result = calc(player1['current'], player2['current'])
		a = result[0]
		player1[a] = player1[a] + 1
		player1['played_hands'].append(player1['current'])
		player1['current'] = None
		return a, 200
	elif player == 2:
		if player2['current']:
			return 'Current choice already set', 403
		player2['current'] = choice
		while not result[1]:
			sleep(0.01)
		b = result[1]
		player2[b] = player2[b] + 1
		player2['played_hands'].append(player2['current'])
		player2['current'] = None
		result = (None, None)
		played = played + 1
		return b, 200
'''


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=4441)
