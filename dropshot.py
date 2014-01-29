#!/usr/bin/env python
from bottle import request, route, get, post, run, template, response, hook, abort
from sqlalchemy import or_, and_
import models

current_player = None

@hook('before_request')
def set_logged_in_player():
    global current_player
    authToken = request.get_cookie('authtoken')
    
    playerQuery = models.session.query(models.Player).filter(models.Player.authToken == authToken)
    if (playerQuery.count() != 1):
        current_player = None    
    else:
        current_player = playerQuery.one()

# ---- GET REQUESTS -----------------------------------------------------------

@get('/')
def home():
    return "dropshot is online"

@get('/ping')
def pong():
    return "pong"

@get('/players')
def get_players():
    input_count = int(request.query.get('count') or 100)
    input_offset = int(request.query.get('offset') or 0)
    
    playersQuery = models.session.query(models.Player).slice(input_offset, input_offset + input_count)
    playersAsJson = map(lambda player: player.to_dictionary(), playersQuery)

    return { 'count' : len(playersAsJson), 'offset' : input_offset, 'players' : playersAsJson }

@get('/players/<username>')
def get_player_by_username(username):
    playerQuery = models.session.query(models.Player).filter(models.Player.username == username)
    if (playerQuery.count() == 0):
        return { 'error' : 'no player found' }
    player = playerQuery.first()
    return player.to_dictionary()

@get('/players/<username>/games')
def get_games_by_username(username):
    return template('No games associated with player <b>{{username}}</b>.', username=username)

@get('/games/<game_id>')
def get_game_by_id(game_id):
    gameQuery = models.session.query(models.Game).filter(models.Game.id == gameId)
    if(gameQuery.count() == 0):
        return { 'error' : 'CANTFINDGAME' }
    game = gameQuery.first()
    return game.to_dictionary()

@get('/games')
def get_games():
    input_count = int(request.query.get('count') or 100)
    input_offset = int(request.query.get('offset') or 0)
    
    gamesQuery = models.session.query(models.Game).slice(input_offset, input_offset + input_count)
    gamesAsJson = map(lambda game: game.to_dictionary(), gamesQuery)

    return { 'count' : len(gamesAsJson), 'offset' : input_offset, 'players' : gamesAsJson }

@get('/logout')
def logout():
    if(current_player == None):
        response.status = 401
        return { 'error' : 'NOTLOGGEDIN'}
    response.set_cookie('authtoken', 'pingpong')
    return 'goodbye'

# ---- POST REQUESTS ----------------------------------------------------------

@post('/games')
def post_games():
    if (current_player == None):
        response.status = 401
        return { 'error' : 'NOTLOGGEDIN'}
    
    input_winner = request.forms.get('winner')
    input_loser = request.forms.get('loser')
    input_winner_score = request.forms.get('winnerScore')
    input_loser_score = request.forms.get('loserScore')
    
    if( not (current_player.username == input_winner or current_player.username == input_loser)):
        response.status = 400
        return { 'error' : 'INVALIDPLAYERS'}
    
    if( not (input_winner_score.isdigit() and input_loser_score.isdigit())):
        response.status = 400
        return { 'error' : 'INVALIDSCORES'}

    winnerQuery = models.session.query(models.Player).filter(models.Player.username == input_winner)
    loserQuery = models.session.query(models.Player).filter(models.Player.username == input_loser)

    if( not (winnerQuery.count() == 1 and loserQuery.count() == 1)):
        response.status = 400
        return { 'error' : 'INVALIDPLAYERS'}

    winner = winnerQuery.one()
    loser = loserQuery.one()

    game = models.Game(winner=winner, loser=loser)
    models.session.add(game)
    models.session.commit()
    
    response.status = 201
    return game.to_dictionary()

@post('/players')
def post_players():
    if (current_player != None):
        response.status = 403
        return { 'error' : 'MUSTLOGOUT'}
    input_username = request.forms.get('username')
    input_password = request.forms.get('password')
    input_email = request.forms.get('email')

    playerQuery = models.session.query(models.Player).filter(or_(models.Player.username == input_username, models.Player.email == input_email))
    if (playerQuery.count() > 0):
        response.status = 409
        return { 'error' : 'USEREXISTS' }

    player = models.Player(username = input_username, password = input_password, email = input_email)
    models.session.add(player)
    models.session.commit()
    
    response.status = 201

@post('/login')
def login():
    input_username = request.forms.get('username')
    input_password = request.forms.get('password')
    
    playerQuery = models.session.query(models.Player).filter(and_(models.Player.username == input_username, models.Player.password == input_password))
    if (not playerQuery.count() == 1):
        response.status = 401
        return { 'error' : 'GETDUNKED'}
    
    player = playerQuery.first()
    
    if (player.authToken == None):
        player.generate_auth_token()
        models.session.commit()
    
    response.set_cookie('authtoken', player.authToken)
    return { 'authToken' : player.authToken }

#@route('/db')
#def create_db():
#    return models.session.query(models.Player).all()[0].to_json()

if __name__ == '__main__':
    run(host='localhost', port='3000')
