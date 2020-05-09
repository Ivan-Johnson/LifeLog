#!/bin/env bash
set -euo pipefail
#set -x
DIR="$(dirname "$0")"
cd "$DIR"

export FLASK_APP=./
export FLASK_ENV=development

if [ "${1:-}" = "reinit" ] ; then
	flask init-db
elif [ "${1:-}" = "run" ] ; then
	flask run --host=0.0.0.0
else
	if [ "${1:-}" != "help" ]; then
		echo "No valid subcommand recognized. Defaulting to \"help\""
	fi
	echo "The syntax for using this command is \"$0 \${subcommand}\"."
	echo "Valid subcommands are:"
	echo -e "\thelp: show this menu"
	echo -e "\treinit: run the flask command for reinitializing the database"
	echo -e "\trun: run the flask server locally"
	exit 1
fi
