rps-server
==========
This is a small server application to manage a game of rock, paper, scissors.

Execute start.sh to start the server. But be *carefull* by running this
application on your machine because it will flush the database 0 on your redis
server.

Also start.sh needs two arguments to identify the two players. All other
ids will be tracked and causing the server to stop the game.

The address of the server is 127.0.0.1:4441 but you can change this in the
start.sh.

REST
----
For REST look at the source code in rps_server.py

Errorcodes
----------
- ERRORCODE 1 : Wrong id used
- ERRORCODE 2 : More or less than 2 players
- ERRORCODE 3 ; id : illegal choice (e.g. lizard or Spock) from id
- ERRORCODE 4 : Error in Calculation

Player
------
An example player is added to this server.

Requirements
------------

 - python
 - python redis
 - redis
 - gunicorn
 - python flask
