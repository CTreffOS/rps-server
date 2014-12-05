 #!/bin/bash
if [ $# -eq 2 ];
	then
		if [ -z "$DB_PORT_6379_TCP_ADDR" ];
			then
				echo "Database not found"
			else
				echo "Change directory"
				cd $(dirname $0)
				echo "Initialize redis"
				redis-cli -h $DB_PORT_6379_TCP_ADDR select 0
				redis-cli -h $DB_PORT_6379_TCP_ADDR rpush player $1
				redis-cli -h $DB_PORT_6379_TCP_ADDR rpush player $2
				redis-cli -h $DB_PORT_6379_TCP_ADDR set played 0
				redis-cli -h $DB_PORT_6379_TCP_ADDR set $1:won 0
				redis-cli -h $DB_PORT_6379_TCP_ADDR set $2:won 0
				echo "DATABASE = \"$DB_PORT_6379_TCP_ADDR\"" > config.py
				echo "Start Server"
				gunicorn --log-level info --log-file - -w 3 -b 127.0.0.1:4441 rps_server:app
		fi
	else
		echo "Wrong arguments"
fi
