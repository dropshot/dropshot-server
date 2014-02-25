#!/bin/bash

TEMP=$(getopt -o '' -n $(basename $0) -- "$@")

if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

eval set -- "$TEMP"

while true; do
  case "$1" in
    -- ) shift; break ;;
  esac
done

#check if something is listening on tcp port 3000
nstat=`netstat -plnt 2> /dev/null | grep :3000`
if [ $? -eq 0 ]; then
  echo "============"
  echo "something is already listening on tcp port 3000"
  echo "============"
  echo NETSTAT
  echo $nstat
  echo "============"
  echo PS
  pid=`echo $nstat|tr / \ |cut -d\  -f7`
  ps up $pid
  echo "============"
  exit 2;
fi

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
