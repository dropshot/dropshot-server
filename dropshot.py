#!/usr/bin/env python
from bottle import route, get, post, run, template
#import models

# ---- GET REQUESTS -----------------------------------------------------------

@get('/')
def home():
    return "dropshot is online"

@get('/ping')
def pong():
    return "pong"

@get('/players')
def get_players():
    return "No players."

@get('/players/<username>')
def get_players_by_username(username):
    return template('No player <b>{{username}}</b>.', username=username)

@get('/players/<username>/games')
def get_games_by_username(username):
    return template('No games associated with player <b>{{username}}</b>.', username=username)

@get('/games/<game_id>')
def get_games_by_id(game_id):
    return template('No game with ID=<b>{{game_id}}</b>.', game_id=game_id)

@get('/games')
def get_games():
    return "No games."

@get('/logout')
def logout():
    return "Cannot logout."

# ---- POST REQUESTS ----------------------------------------------------------

@post('/games')
def post_games():
    return "Cannot create game."

@post('/players')
def post_players():
    return "Cannot create player."

@post('/login')
def login():
    return "Cannot login."

#@route('/db')
#def create_db():
#    return models.session.query(models.Player).all()[0].to_json()

if __name__ == '__main__':
    run(host='localhost', port='3000')
