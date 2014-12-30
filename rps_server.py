from flask import Flask, jsonify
import redis
import time

# Create aplication
app = Flask(__name__)


MAX_GAMES = 1000
POSSIBILITIES = ['rock', 'paper', 'scissors']
RELATIONS = [[False, False, True],[True, False, False],[False, True, False]]


@app.route('/')
def info():
	'''Manage the output of this server.
	If an error occurs this function return this error
	While the game is not over this function returns "playing"
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

	r = redis.StrictRedis(host='localhost', db=0)

	# Check for error
	error = r.get('error')
	if error:
		return error, 200

	# Check number of played games
	try:
		played = int(r.get('played'))
	except:
		r.set('error', 'Error in Redis database: Could not get played games')
		return 'Error in Redis database: Could not get played games', 200
	if not played == 2* MAX_GAMES:
		return 'playing', 200

	# Get player
	player = r.lrange('player', 0, -1)

 	# Get result
	result = {}
	for p in player:
		result[p] = {'won' : r.get('%s:won' % p)}
		for v in POSSIBILITIES:
			result[p][v] = r.get('%s:%s' % (p,v))
	return jsonify(result), 200


@app.route('/<int:id>/<choice>')
def game(id, choice):
	'''Function to call for a game. This function waits until both player has
	chosen.

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

	r = redis.StrictRedis(host='localhost', db=0)

	# Check errorstatus
	if r.exists('error'):
		return 'game over', 404

	# Check number of played games
	try:
		played = int(r.get('played'))
	except:
		r.set('error', 'Error in Redis database: Could not get played games')
		return 'game over', 404

	if played == 2*MAX_GAMES:
		return 'game over', 404

	# Get player
	player = r.lrange('player', 0, -1)

	# Check number of players
	if not len(player) == 2:
		r.set('error', 'Error in Redis database: More or less than two player')
		return 'game over', 404

	# Convert ids to int
	try:
		player[0] = int(player[0])
		player[1] = int(player[1])
	except:
		r.set('error', 'Error in Redis database: One or two player ids are no '
				'integer')
		return 'game over', 404

	# Check ids
	if id == player[0]:
		opponent = player[1]
	elif id == player[1]:
		opponent = player[0]
	else:
		r.set('error', 'Error in player input: Wrong id was used')
		return 'game over', 404

	# Set choice
	try:
		choice = POSSIBILITIES.index(choice)
	except:
		r.set('error', 'Error in player %s input: Choice not legal', id)
		return 'game over', 404

	# Check current
	if r.exists('%s:current' % id):
		return 'current already set', 200

	# Set current
	r.set('%s:current' % id, choice)

	# Sleep until all player has chosen or an error occured
	while not (r.exists('%s:current' % opponent) or r.exists('error')):
		#time.sleep(0.01)
		pass

	# Check errorstatus (again)
	if r.exists('error'):
		return 'game over', 404

	# Get current of the opponent
	try:
		opp_choice = int(r.get('%s:current' % opponent))
	except:
		r.set('error', 'Error in Redis database: Could not get %s:current' \
				% opponent)
		return 'game over', 404

	# Calculate result
	won = RELATIONS[choice][opp_choice]

	# If won
	if won:
		r.incr('%s:won' % id)

	# Set statistic
	r.incr('%s:%s' % (id, POSSIBILITIES[choice]))

	# Increase number of played games (This is done twice.)
	r.incr('played')

	# Wait until both players are ready with calculation
	while not (played == int(r.get('played')) - 2):
		pass

	# Delete own current
	r.delete('%s:current' % id)

	# Return choice of the other player
	return POSSIBILITIES[opp_choice], 200


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=4441, debug=True, threaded=True)
