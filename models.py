from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import os
import binascii

engine = create_engine('sqlite:///db.sqlite', echo=True)
Base = declarative_base()


class Player(Base):
    """
    Player

    The class that defines a player, its attributes, and the methods that act on
    it. This class also defines the schema for the players table in the
    database.

    Attributes:
        id: An auto-incrementing numerical identifier.
        username: The player's username.
        password: The player's plain text password.
        email: The player's email address.
        authToken: The player's current authentication token.
        games: A list of game objects that the player has participated in.
    """
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    authToken = Column(String, unique=True)
    games = relationship("Game",
                         primaryjoin="or_(Player.id==Game.loser_id," +
                         " Player.id==Game.winner_id)")

    def to_dictionary(self):
        """
        Convert a player to a dictionary with limited information.

        Args:
            self

        Returns:
            A dictionary with the player's username and the number of games
            they have played.
        """
        return {'username': self.username, 'gamesPlayed': len(self.games)}

    def generate_auth_token(self):
        """
        Generate an authentication token for the player.

        Args:
            self

        Returns:
            True after having generated the authentication token.
        """
        self.authToken = str(binascii.b2a_hex(os.urandom(15)))
        return True


class Game(Base):
    """
    Game

    The class that defines a game, its attributes, and the methods that act on
    it. This class also defines the schema for the games table in the database.

    Attributes:
        id: An auto-incrementing numerical identifier.
        winner_id: The id of the player who won the game.
        winner: The player object of the game's winner.
        loser_id: The id of the player who lost the game.
        loser: The player object of the game's loser.
        winner_score: The winner's score.
        loser_score: The loser's score.
        timestamp: A Unix formatted timestamp.
        state: The state of the game. Possible values are pending or accepted.
    """
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    winner_id = Column(Integer, ForeignKey('players.id'))
    winner = relationship("Player", foreign_keys=[winner_id])
    loser_id = Column(Integer, ForeignKey('players.id'))
    loser = relationship("Player", foreign_keys=[loser_id])
    winner_score = Column(Integer)
    loser_score = Column(Integer)
    timestamp = Column(Integer)
    state = Column(String)

    submitted_by_id = Column(Integer, ForeignKey('players.id'))
    submitted_by = relationship("Player", foreign_keys=[submitted_by_id])

    def to_dictionary(self):
        """
        Convert a game object to a dictionary with limited information.

        Args:
            self

        Returns:
            A dictionary with the game's id, the game's winner and loser,
            their respective scores, the time the game was created, and the
            current state of the game.
        """
        return {'id': self.id, 'winner': self.winner.username,
                'loser': self.loser.username,
                'loserScore': self.loser_score,
                'winnerScore': self.winner_score,
                'timestamp': self.timestamp,
                'state': self.state}

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
