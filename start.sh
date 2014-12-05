 #!/bin/bash
if [ $# -eq 2 ]
	then
		echo "Initialize redis"
		redis-cli select 0
		redis-cli rpush player $1
		redis-cli rpush player $2
		redis-cli set played 0
		redis-cli set $1:won 0
		redis-cli set $2:won 0
		echo "Start Server"
		gunicorn --log-level info --log-file - -w 3 -b 127.0.0.1:4441 rps_server:app
	else
		echo "Wrong arguments"
fi
