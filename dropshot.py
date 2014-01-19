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
def get_player_by_username(username):
    playerQuery = models.session.query(models.Player).filter(models.Player.username == username)
    if (playerQuery.count() == 0):
        return { 'error' : 'no player found' }
    player = playerQuery.first()
    return player.to_json()

@get('/players/<username>/games')
def get_games_by_username(username):
    return template('No games associated with player <b>{{username}}</b>.', username=username)

@get('/games/<game_id>')
def get_game_by_id(game_id):
    gameQuery = models.session.query(models.Game).filter(models.Game.id == gameId)
    if(gameQuery.count() == 0)
        return { 'error' : 'CANTFINDGAME' }
    game = gameQuery.first()
    return game.to_json()

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
