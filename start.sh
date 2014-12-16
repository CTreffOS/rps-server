#!/bin/bash
if [ $# -eq 2 ];
then
	/usr/bin/redis-server &
	# Make sure redis is ready to go
	until [ $(redis-cli ping) ]
		do sleep 0.01
	done
	echo "Initialize redis"
	redis-cli rpush player $1
	redis-cli rpush player $2
	redis-cli set played 0
	redis-cli set $1:won 0
	redis-cli set $2:won 0
	redis-cli set $1:rock 0
	redis-cli set $1:paper 0
	redis-cli set $1:scissors 0
	redis-cli set $2:rock 0
	redis-cli set $2:paper 0
	redis-cli set $2:scissors 0
	echo "Start Server"
	cd $(dirname $0)
	gunicorn --log-level debug --log-file - -w 32 -b 0.0.0.0:4441 rps_server:app
else
	echo "Wrong arguments"
fi
