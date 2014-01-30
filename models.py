from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import os, binascii

engine = create_engine('sqlite:///db.sqlite', echo=True)
Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    authToken = Column(String, unique=True)
    games = relationship("Game", primaryjoin = "or_(Player.id==Game.loser_id, Player.id==Game.winner_id)")

    def to_dictionary (self):
        return { 'username' : self.username, 'gamesPlayed' : len(self.games)}

    def generate_auth_token (self):
        self.authToken = str(binascii.b2a_hex(os.urandom(15)))
        return True

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    winner_id = Column(Integer, ForeignKey('players.id'))
    winner = relationship("Player", foreign_keys=[winner_id])
    loser_id = Column(Integer, ForeignKey('players.id'))
    loser = relationship("Player", foreign_keys=[loser_id])
    winner_score = Column(Integer)
    loser_score = Column(Integer)
    timestamp = Column(Integer)

    def to_dictionary(self):
        return { 'id' : self.id , 'winner' : self.winner.username, 'loser' : self.loser.username, 'loserScore' : self.loser_score, 'winnerScore' : self.winner_score, 'timestamp' : self.timestamp}

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session=Session()
