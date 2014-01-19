#!/usr/bin/env python
import urllib.parse
import urllib.request

def create_player(username, password, email):
    url = 'http://localhost:3000/players'
    values = {'username' : username,
              'password' : password,
              'email'    : email }

    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8') # data should be bytes
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    print("Created user \'{}\' with password \'{}\' and email \'{}\'".format(username, password, email))

if __name__ == '__main__':
    create_player("chapmang", "password", "chapmang@dropshot.com")
    create_player("idlee", "deadparrot", "idlee@dropshot.com")
    create_player("gilliamt", "lumberjack", "gilliamt@dropshot.com")
    create_player("jonest", "trojanrabbit", "jonest@dropshot.com")
    create_player("cleesej", "generaldirection", "cleesej@dropshot.com")
    create_player("palinm", "fleshwound", "palinm@dropshot.com")
