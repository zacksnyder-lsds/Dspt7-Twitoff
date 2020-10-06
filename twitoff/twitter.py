from os import getenv
import tweepy
import spacy
from dotenv import load_dotenv
from .db_model import DB, User, Tweet

load_dotenv()


TWITTER_AUTH = tweepy.OAuthHandler(getenv('TWITTER_CONSUMER_API_KEY'), 
                                   getenv('TWITTER_CONSUMER_API_SECRET'))
TWITTER_AUTH.set_access_token(getenv('TWITTER_ACCESS_TOKEN'), 
                              getenv('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)


nlp = spacy.load('en_core_web_md', disable=['tagger', 'parser'])


def vectorize_tweet(nlp, tweet_text):
    '''This function returns the SpaCy embeddings for an input text'''
    return nlp(tweet_text).vector

def add_user_tweepy(username):
    '''Add a user and their tweets to database'''
    try:
        
        twitter_user = TWITTER.get_user(username)

        
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id,
                        username=username,
                        followers=twitter_user.followers_count))
        DB.session.add(db_user)

        
        tweets = twitter_user.timeline(count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       tweet_mode='extended',
                                       since_id=db_user.newest_tweet_id)

        
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
    
       
        for tweet in tweets:

            
            embedding = vectorize_tweet(nlp, tweet.full_text)

            
            db_tweet = Tweet(id=tweet.id,
                             tweet=tweet.full_text[:300],
                             embedding=embedding)
            db_user.tweet.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e

    else:
        
        DB.session.commit()