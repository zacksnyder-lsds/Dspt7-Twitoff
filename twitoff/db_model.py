from flask import Flask
from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()


class User(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    username = DB.Column(DB.String(80), unique=True, nullable=False)
    followers = DB.Column(DB.String(120), unique=True, nullable=False)
    newest_tweet_id = DB.column(DB.BigInteger)

    def __repr__(self):
        return '<User %r>' % self.username

class Tweet(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    tweet = DB.Column(DB.String(280), unique=True, nullable=False)
    embedding = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweet', lazy=True))

    def __repr__(self):
        return '<Tweet %r>' % self.tweet