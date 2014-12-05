rps-server
==========
This is a small server application to manage a game of rock, paper, scissors.
It is intended to run in a Docker (see https://github.com/CTreffOS/rps-docker
for more information).

Execute start.sh to start the server. Also start.sh needs two arguments to
identify the two players. All other ids will be tracked and causing the server
to stop the game.

REST
----
For REST look at the source code in rps_server.py

Errorcodes
----------
- ERRORCODE 1 : Wrong id used
- ERRORCODE 2 : More or less than 2 players
- ERRORCODE 3 ; id : illegal choice (e.g. lizard or Spock) from id
- ERRORCODE 4 : Error in Calculation
- ERRORCODE 5 : Converting ids to integers failed

Requirements
------------

 - python
 - python redis
 - redis
 - gunicorn
 - python flask
