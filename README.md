dropshot-server
===============

## install directions
1. virtualenv --no-site-pacakge ServerVenv
2. cd ServerVenv
3. git clone https://github.com/dropshot/dropshot-server.git
4. . bin/activate
5. pip install -r requirements.txt
6. ./tools/create_test_pem.sh
7. python dropshot.py
