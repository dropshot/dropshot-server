dropshot-server
===============

## install directions
```
virtualenv --no-site-packages -p /usr/bin/python3 ServerVenv
cd ServerVenv
git clone https://github.com/dropshot/dropshot-server.git
. bin/activate
pip install -r requirements.txt
./tools/create_test_pem.sh
python dropshot.py
```
