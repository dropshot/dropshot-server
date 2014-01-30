#!/bin/bash

TEMP=$(getopt -o '' -n $(basename $0) -- "$@")

if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

eval set -- "$TEMP"

while true; do
  case "$1" in
    -- ) shift; break ;;
  esac
done

# Save current database
DBFILE="db.sqlite"

mv $DBFILE $DBFILE.bak

./dropshot.py &
SERVERPID=$!

sleep 2 # Wait for server to fully start

python tests/integration/players.py

RET=$?

# Cleanups
kill $SERVERPID
rm $DBFILE
mv $DBFILE.bak $DBFILE

exit $RET
