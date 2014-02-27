#!/bin/sh
openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
cp server.pem /var/tmp/server.pem
