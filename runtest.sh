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

if [ -e $DBFILE ]; then
  mv $DBFILE $DBFILE.bak
fi

./dropshot.py &
SERVERPID=$!

sleep 2 # Wait for server to fully start

python tests/integration/players.py

RET=$?

# Cleanups
kill $SERVERPID
rm $DBFILE
if [ -e $DBFILE.bak ]; then
  mv $DBFILE.bak $DBFILE
fi

exit $RET
