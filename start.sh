 #!/bin/bash
echo "Create Database"
sqlite3 rps-server.db < schema.sql
echo "Create Player $1"
echo "INSERT INTO player (id) VALUES($1);" | sqlite3 rps-server.db
echo "Create Player $2"
echo "INSERT INTO player (id) VALUES($2);" | sqlite3 rps-server.db
echo "Start Server"
gunicorn -w 4 -b 127.0.0.4441 rps-server:app
