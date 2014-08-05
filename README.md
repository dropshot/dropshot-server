Dropshot Server
===============

Dropshot is a ping-pong ladder ranking tracker.

[![Build Status](https://travis-ci.org/dropshot/dropshot-server.svg?branch=dev)](https://travis-ci.org/dropshot/dropshot-server)


## Install directions
```
virtualenv --no-site-packages -p /usr/bin/python3 ServerVenv
cd ServerVenv
git clone https://github.com/dropshot/dropshot-server.git
. bin/activate
pip install -r requirements.txt
./tools/create_test_pem.sh
python dropshot.py
```
