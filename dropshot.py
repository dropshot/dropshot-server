#!/usr/bin/env python
from bottle import Bottle, request, response, template, server_names
from bottle.ext import sqlalchemy
from sqlalchemy import or_, and_, create_engine
import models
from time import time
from sslcherrypy import SSLCherryPy

# Register SSLCherryPy as a wsgi capable server.
server_names['sslcherrypy'] = SSLCherryPy

app = Bottle()

current_player = None

# ---- GET REQUESTS -----------------------------------------------------------


@app.get('/')
def home():
    """Return a status message if the root of the app is requested."""
    return "dropshot is online"


@app.get('/ping')
def pong():
    """If ping is requested, naturally we return pong."""
    return "pong"


@app.get('/players')
def get_players(db):
    """
    Get players.

    Args:
        db: An injected SQLAlchemy session.

    Returns:
        A dictionary including player count, a list of players, and an offset
        for player pagination.
    """
    input_count = int(request.query.get('count') or 100)
    input_offset = int(request.query.get('offset') or 0)

    playersQuery = db.query(models.Player).\
        slice(input_offset, input_offset + input_count)
    playersAsJson = list(map(lambda player: player.to_dictionary(),
                             playersQuery))

    return {'count': len(playersAsJson), 'offset': input_offset,
            'players': playersAsJson}


@app.get('/players/<username>')
def get_player_by_username(username, db):
    """
    Get a player by their username.

    Args:
        username: The name of the user to look up.
        db: An injected SQLAlchemy session.

    Returns:
        The result of calling the player object's to_dictionary method.
    """
    playerQuery = db.query(models.Player).\
        filter(models.Player.username == username)
    if (playerQuery.count() == 0):
        return {'error': 'no player found'}
    player = playerQuery.first()
    return player.to_dictionary()


@app.get('/players/<username>/games')
def get_games_by_username(username):
    """
    Get games associated with a given username.

    Args:
        username: The name of the user to use for looking up games.

    Returns:
        HTML saying no games are associated with the given user.
    """
    return template('No games associated with player <b>{{username}}</b>.',
                    username=username)


@app.get('/games/<game_id>')
def get_game_by_id(game_id, db):
    """
    Get a game by its id.

    Args:
        game_id: The id of the game to return.
        db: An injected SQLAlchemy session.

    Returns:
        The result of calling the game object's to_dictionary method.
    """
    gameQuery = db.query(models.Game).\
        filter(models.Game.id == game_id)
    if(gameQuery.count() == 0):
        return {'error': 'CANTFINDGAME'}
    game = gameQuery.first()
    return game.to_dictionary()


@app.get('/games')
def get_games(db):
    """
    Get games.

    Args:
        db: An injected SQLAlchemy session.

    Returns:
        A dictionary including game count, a list of games, and an offset
        for for game pagination.
    """
    input_count = int(request.query.get('count') or 100)
    input_offset = int(request.query.get('offset') or 0)

    gamesQuery = db.query(models.Game).\
        filter(models.Game.state == 'accepted').\
        slice(input_offset, input_offset + input_count)

    gamesAsJson = list(map(lambda game: game.to_dictionary(), gamesQuery))

    return {'count': len(gamesAsJson), 'offset': input_offset,
            'games': gamesAsJson}


@app.get('/pendingGames')
def get_pending_games(db):
    """
    Get pending games.

    Args:
        db: An injected SQLAlchemy session.

    Returns:
        A dictionary including pending games count, a list of pending games,
        and an offset for for pending game pagination.
    """
    if(current_player is None):
        response.status = 401
        return {'error': 'NOTLOGGEDIN'}

    input_count = int(request.query.get('count') or 100)
    input_offset = int(request.query.get('offset') or 0)

    gamesQuery = db.query(models.Game).\
        filter(models.Game.state == 'pending').\
        filter(models.Game.submitted_by != current_player).\
        filter(or_(models.Game.loser == current_player,
                   models.Game.winner == current_player))

    gamesAsJson = list(map(lambda game: game.to_dictionary(), gamesQuery))
    return {'count': len(gamesAsJson), 'offset': input_offset,
            'games': gamesAsJson}


@app.get('/logout')
def logout():
    """
    Log the current player out.

    Args:
        none

    Returns:
        A string saying goodbye.
    """
    if(current_player is None):
        response.status = 401
        return {'error': 'NOTLOGGEDIN'}
    response.set_cookie('authtoken', 'pingpong')
    return 'goodbye'

# ---- POST REQUESTS ----------------------------------------------------------


@app.post('/games')
def post_games(db):
    """
    Create a new game.

    Args:
        db: An injected SQLAlchemy session.

    Returns:
        The result of calling the newly created game object's to_dictionary
        method.
    """
    if (current_player is None):
        response.status = 401
        return {'error': 'NOTLOGGEDIN'}

    input_winner = request.forms.get('winner')
    input_loser = request.forms.get('loser')
    input_winner_score = request.forms.get('winnerScore')
    input_loser_score = request.forms.get('loserScore')

    if (not (current_player.username == input_winner or
             current_player.username == input_loser)):
        response.status = 400
        return {'error': 'INVALIDPLAYERS'}

    if (not (input_winner_score.isdigit() and input_loser_score.isdigit())):
        response.status = 400
        return {'error': 'INVALIDSCORES'}

    winnerQuery = db.query(models.Player).\
        filter(models.Player.username == input_winner)
    loserQuery = db.query(models.Player).\
        filter(models.Player.username == input_loser)

    if (not (winnerQuery.count() == 1 and loserQuery.count() == 1)):
        response.status = 400
        return {'error': 'INVALIDPLAYERS'}

    winner = winnerQuery.one()
    loser = loserQuery.one()

    game = models.Game(winner=winner,
                       loser=loser,
                       winner_score=input_winner_score,
                       loser_score=input_loser_score,
                       timestamp=int(time.time()),
                       state='pending',
                       submitted_by=current_player)

    db.add(game)

    response.status = 201
    return game.to_dictionary()


@app.post('/acceptGame')
def accept_game(db):
    """
    Accept a pending game.

    Args:
        db: An injected SQLAlchemy session.

    Returns:
        The result of calling the game object's to_dictionary method.
    """
    if (current_player is None):
        response.status = 401
        return {'error': 'NOTLOGGEDIN'}

    input_game_id = request.forms.get('gameId')

    gameQuery = db.query(models.Game).\
        filter(models.Game.id == input_game_id)
    if(gameQuery.count() == 0):
        return {'error': 'CANTFINDGAME'}
    gameQuery = gameQuery.filter(models.Game.state == 'pending').\
        filter(models.Game.submitted_by != current_player).\
        filter(or_(models.Game.loser == current_player,
                   models.Game.winner == current_player))
    if(gameQuery.count() == 0):
        return {'error': 'CANTACCEPT'}
    game = gameQuery.one()
    game.state = 'accepted'
    return game.to_dictionary()


@app.post('/players')
def post_players(db):
    """
    Create a new player.

    Args:
        db: An injected SQLAlchemy session.

    Returns:
        If a player is logged in, a dictionary with a logout error. If the
        requested player already exists, then a dictonary with an error saying
        so. Otherwise, there is no return.
    """
    if (current_player is not None):
        response.status = 403
        return {'error': 'MUSTLOGOUT'}
    input_username = request.forms.get('username')
    input_password = request.forms.get('password')
    input_email = request.forms.get('email')

    playerQuery = db.query(models.Player).\
        filter(or_(models.Player.username == input_username,
                   models.Player.email == input_email))
    if (playerQuery.count() > 0):
        response.status = 409
        return {'error': 'USEREXISTS'}

    player = models.Player(username=input_username, password=input_password,
                           email=input_email)
    db.add(player)

    response.status = 201


@app.post('/login')
def login(db):
    """
    Login.

    Args:
        db: An injected SQLAlchemy session.

    Returns:
        A dictionary containing an auth token for the player or, if the login
        was unsuccessful then dictionary with a GETDUNKED error.
    """
    input_username = request.forms.get('username')
    input_password = request.forms.get('password')

    playerQuery = db.query(models.Player).\
        filter(and_(models.Player.username == input_username,
                    models.Player.password == input_password))
    if (not playerQuery.count() == 1):
        response.status = 401
        return {'error': 'GETDUNKED'}

    player = playerQuery.first()

    if (player.authToken is None):
        player.generate_auth_token()

    response.set_cookie('authtoken', player.authToken)
    return {'authToken': player.authToken}


# ---- DELETE REQUESTS ---------------------------------------------------------

@app.delete('/players/<username>')
def delete_players(username, db):
    """
    Delete a player.

    Args:
        username: The name of the user to be deleted.
        db: An injected SQLAlchemy session.

    Returns:
        If the player is not found a dictionary containing an error, otherwise
        there is no return.
    """
    playerQuery = db.query(models.Player).\
        filter(models.Player.username == username).delete()
    if (playerQuery.count() == 0):
        return {'error': 'no player found'}
    response.status = 204


@app.delete('/games/<game_id>')
def delete_games(game_id, db):
    """
    Delete a game.

    Args:
        game_id: The id of the game to be deleted.
        db: An injected SQLAlchemy session.

    Returns:
        If the game is not found a dictionary saying there was an error,
        otherwise there is no return.
    """
    gameQuery = db.query(models.Game).\
        filter(models.Game.id == game_id).delete()
    if(gameQuery.count() == 0):
        return {'error': 'CANTFINDGAME'}
    response.status = 204


def configure_app():
    engine = create_engine('sqlite:///db.sqlite', echo=True)
    plugin = sqlalchemy.Plugin(
        engine,
        models.Base.metadata,
        keyword='db',
        create=True,
        commit=True,
        use_kwargs=False
    )
    app.install(plugin)


if __name__ == '__main__':
    configure_app()
    app.run(host="localhost", port='3000', cert='/var/tmp/server.pem',
            key='/var/tmp/server.pem', server='sslcherrypy')
