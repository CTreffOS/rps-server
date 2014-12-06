 #!/bin/bash
	echo "change directory"
	cd $(dirname $0)
	echo "initialize redis"
	redis-cli select 0
	redis-cli del error
	redis-cli del player
	redis-cli rpush player $1
	redis-cli rpush player $2
	redis-cli set played 0
	redis-cli set $1:won 0
	redis-cli set $1:rock 0
	redis-cli set $1:paper 0
	redis-cli set $1:scissors 0
	redis-cli set $2:won 0
	redis-cli set $2:rock 0
	redis-cli set $2:paper 0
	redis-cli set $2:scissors 0
	echo "DATABASE = \"127.0.0.1\"" > server_config.py
	echo "start server"
	timeout 10 gunicorn --log-level info --log-file 'server.log' -w 3 -b 127.0.0.1:4441 rps_server:app &
	sleep 2
	echo "start player"
	echo "time"
	time -f "\t%E real" python testplayer.py $1 &
	time -f "\t%E real" python testplayer.py $2
	echo "played: $(redis-cli get played)"
	echo "error: $(redis-cli get error)"
	echo "Player $1:"
	echo "won: $(redis-cli get $1:won)"
	echo "rock: $(redis-cli get $1:rock)"
	echo "paper: $(redis-cli get $1:paper)"
	echo "scissors: $(redis-cli get $1:scissors)"
	echo "Player $2:"
	echo "won: $(redis-cli get $2:won)"
	echo "rock: $(redis-cli get $2:rock)"
	echo "paper: $(redis-cli get $2:paper)"
	echo "scissors: $(redis-cli get $2:scissors)"
	echo "Server output:"
	curl -i 127.0.0.1:4441
