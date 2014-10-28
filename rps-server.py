#!/bin/env python
from flask import Flask, jsonify
from time import sleep

# Create aplication
app = Flask(__name__)

# Maximal Games
MAX_GAMES = 1000
# Number of games played by these players
played = 0
# globals for player1 and player2 (init in register())
player1 = {}
player2 = {}
# globals for the result of a game
result = (None, None)

def calc(value1, value2):
	''' Calculate the winner of a game.

	value1 is the choise of player1 limited to rock, paper or scissors
	value2 is the choise of player2 limited to rock, paper or scissors

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

@app.route('/')
def render():
	'''Dummy function for a nice output.

	HTTP return codes:

		====  =====================  =====================
		Code  Status                 Meaning
		====  =====================  =====================
		200   OK                     Nothing
		====  =====================  =====================
	'''
	return '', 200

@app.route('/register')
def register():
	'''Function to call at the beginning to register the player on the server
	and to initialize the player. The function waits until both players are
	registered

	Returns which player you are or if the game has enough player. Possible
	values are player1, player2, full

	HTTP return codes:

		====  =====================  =====================
		Code  Status                 Meaning
		====  =====================  =====================
		201   Created                Register new player
		403   Forbidden              Enough player
		====  =====================  =====================
	'''
	global player1, player2
	if player1 and player2:
		return 'full', 403
	if player1:
		player2 = {'won':0, 'lost':0, 'draw':0, 'played_hands': [], 'current':None}
		return 'player2', 201
	player1 = {'won':0, 'lost':0, 'draw':0, 'played_hands': [],
			'current':None}
	while not player2:
		sleep(0.01)
	return 'player1', 201

@app.route('/game/<int:player>/<choise>')
def game(player, choise):
	'''Function to call for a game. This function waits until both player has chosen.

	player is the integer of the player, so possible values are 1 and 2
	choise is the choise of the player limited to rock, paper and scissors

	Returns if the player that call this function has won, lost oder draw.

	HTTP return codes:

		====  =====================  ======================
		Code  Status                 Meaning
		====  =====================  ======================
		200   OK                     Game over, game played
		400   BAD REQUEST            player, choise wrong
		403   FORBIDDEN              Already chosen
		404   NOT FOUND              Not enought player
		====  =====================  ======================
'''
	global played, player1, player2, result
	while not result == (None, None):
		sleep(0.01)
	if not (player1 and player2):
		return 'Not enough player', 404
	if not player in [1,2]:
		return 'No player', 400
	if not choise in ['rock', 'paper', 'scissors']:
		return 'No legal choise', 400
	if played >= MAX_GAMES:
		return 'game over', 200

	if player == 1:
		if player1['current']:
			return 'Current choise already set', 403
		player1['current'] = choise
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
			return 'Current choise already set', 403
		player2['current'] = choise
		while not result[1]:
			sleep(0.01)
		b = result[1]
		player2[b] = player2[b] + 1
		player2['played_hands'].append(player2['current'])
		player2['current'] = None
		result = (None, None)
		played = played + 1
		return b, 200

	return '', 200


@app.route('/data/<int:player>')
def data(player):
	'''Function to get the data to the players. By a disconnect this is usefull to retrieve the data.

	player is the integer of the player, so possible values are 1 and 2

	Returns all data to one player in an JSON format.

	HTTP return codes:

		====  =====================  =====================
		Code  Status                 Meaning
		====  =====================  =====================
		200   OK                     Returns data
		404   NOT FOUND              No possible player
		====  =====================  =====================
	'''
	if player == 1:
		return jsonify(player1), 200
	elif player == 2:
		return jsonify(player2), 200
	return '', 404


@app.route('/reset')
def reset():
	'''Function to reset the server

	HTTP return codes:

		====  =====================  =====================
		Code  Status                 Meaning
		====  =====================  =====================
		200   OK                     Reset
		====  =====================  =====================
	'''
	global played, player1, player2
	played = 0
	player1 = {}
	player2 = {}
	return 'reset', 200

app.run(host='0.0.0.0', debug=True, port=5001, threaded=True)
