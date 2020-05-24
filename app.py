from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from passlib.hash import pbkdf2_sha256 as sha256
from token_service import TokenService
import schedule
import time
import threading

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Movie, User, Rating

# Connect to Database and create database session
engine = create_engine('sqlite:///movies-collection.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route('/allusers', methods=['GET'])
def get_users():
    movies = session.query(User).all()
    return jsonify([movie.serialize for movie in movies])


@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    user = session.query(User).filter(User.email == email).all()
    if not user:
        abort(401, {'message': 'No user registered with email id'})
    else:
        if sha256.verify(password, user[0].password):
            user_id = user[0].serialize['id']
            token = TokenService.get_token(user_id)
            return jsonify({'message': 'successful', 'token': token})
        else:
            abort(401, {'message': 'Incorrect Password'})


@app.route('/signup', methods=['POST'])
def signup():
    email = request.json['email']
    password = request.json['password']
    name = request.json['name']

    if not password or not name or not email:
        abort(400, {'message': 'mandatory data is not present'})
    if session.query(User).filter(User.email == email).all():
        abort(409, {'message': 'Email ID already exists.'})
    else:
        user = User(name=name, password=sha256.hash(password), email=email)
        session.add(user)
        session.commit()

        return jsonify({'message': 'User Created', 'user': user.serialize})


@app.route('/movies', methods=['POST'])
def add_movie():
    user_id = TokenService().get_user(headers=request.headers)
    if user_id:
        new_movie = Movie(title=request.json['title'], created_by=user_id)
        session.add(new_movie)
        session.commit()

        return jsonify({'message': 'Movie Created', 'movie': new_movie.serialize})
    else:
        abort(401, {"message": "Bad token"})


@app.route('/movies', methods=['GET'])
def get_movies():
    movies = session.query(Movie).all()
    return jsonify([movie.serialize for movie in movies])


@app.route('/movies/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = session.query(Movie).get(movie_id)
    if not movie:
        abort(401, {'message': 'Invalid Movie id'})
    return jsonify(movie.serialize)


@app.route('/movies/<movie_id>', methods=['PUT'])
def edit_movie(movie_id):
    user_id = TokenService().get_user(headers=request.headers)
    if not user_id:
        abort(401, {'message': 'Invalid Token'})
    movie = session.query(Movie).get(movie_id)
    if not movie:
        abort(401, {'message': 'Invalid movie id'})
    if movie.created_by == user_id:
        movie.title = request.json['title']
        session.commit()
        return jsonify({'message': 'Movie Updated', 'movie': movie.serialize})
    else:
        abort(403, {'message': 'Dont have right to edit the movie'})


@app.route('/movies/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    user_id = TokenService().get_user(headers=request.headers)
    if not user_id:
        abort(401, {'message': 'Bad token'})

    movie = session.query(Movie).get(movie_id)

    if movie.created_by == user_id:
        session.delete(movie)
        session.commit()
        return jsonify({'message': 'Movie Deleted'})
    else:
        abort(403, {'message': 'Dont have right to delete the movie'})


@app.route('/ratings', methods=['POST'])
def add_rating():
    user_id = TokenService().get_user(headers=request.headers)
    movie_id = request.json['movie_id']
    value = request.json['value']

    if user_id:
        movie = session.query(Movie).get(movie_id)
        if movie.created_by == user_id:
            abort(403, {'message': 'You cannot rate your movie'})

        if session.query(Rating).filter(Rating.user_id == user_id).all():
            abort(401, {'message': 'Rating cannot be given twice'})

        rating = Rating(value=value, user_id=user_id, movie_id=movie_id)
        session.add(rating)
        session.commit()

        return jsonify({'message': 'Rating Created', 'movie': rating.serialize})
    else:
        abort(401, {"message": "Bad token"})


@app.route('/ratings', methods=['GET'])
def get_ratings():
    ratings = session.query(Rating).all()
    return jsonify([rating.serialize for rating in ratings])


@app.route('/ratings/<rating_id>', methods=['GET'])
def get_rating(rating_id):
    rating = session.query(Rating).get(rating_id)
    if not rating:
        abort(401, {'message': 'Invalid rating id'})
    return jsonify(rating.serialize)


@app.route('/ratings/<rating_id>', methods=['PUT'])
def edit_rating(rating_id):
    user_id = TokenService().get_user(headers=request.headers)
    if not user_id:
        abort(401, {'message': 'Invalid Token'})

    rating = session.query(Rating).get(rating_id)
    if not rating:
        abort(401, {'message': 'Invalid rating id'})

    if rating.user_id == user_id:
        rating.value = request.json['value']
        session.commit()
        return jsonify({'message': 'Rating Updated', 'movie': rating.serialize})
    else:
        abort(403, {'message': 'Dont have right to edit the rating'})


@app.route('/ratings/<rating_id>', methods=['DELETE'])
def delete_rating(rating_id):
    user_id = TokenService().get_user(headers=request.headers)
    if not user_id:
        abort(401, {'message': 'Bad token'})

    rating = session.query(Rating).get(rating_id)

    if rating.user_id == user_id:
        session.delete(rating)
        session.commit()
        return jsonify({'message': 'Rating Deleted'})
    else:
        abort(403, {'message': 'Dont have right to delete the movie'})


def schedule_average_rating_service():
    def job():
        print("hello")

    schedule.every().day.at("00:03").do(job)
    i = 1
    while True:
        schedule.run_pending()
        time.sleep(2)


if __name__ == '__main__':
    threading.Thread(target=schedule_average_rating_service).start()
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
