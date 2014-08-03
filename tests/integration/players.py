#!/usr/bin/env python

import requests


def create_player(username, password, email):
    url = 'https://localhost:3000/players'
    values = {'username' : username,
              'password' : password,
              'email'    : email }

    r = requests.post(url, params=values, verify=False)

    r.raise_for_status()

    if (r.status_code == 201):
        print("Created user \'{}\' with password \'{}\' and email \'{}\'".format(username,
                                                                                 password,
                                                                                 email))


if __name__ == '__main__':
    create_player("chapmang", "password", "chapmang@dropshot.com")
    create_player("idlee", "deadparrot", "idlee@dropshot.com")
    create_player("gilliamt", "lumberjack", "gilliamt@dropshot.com")
    create_player("jonest", "trojanrabbit", "jonest@dropshot.com")
    create_player("cleesej", "generaldirection", "cleesej@dropshot.com")
    create_player("palinm", "fleshwound", "palinm@dropshot.com")
