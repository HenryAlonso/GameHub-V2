from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'gamehub_db'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.birthday = data['birthday']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(cls, data):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if int(len(data['first_name'])) <= 0 or int(len(data['last_name'])) <= 0 or int(len(data['email'])) <= 0 or int(len(data['password'])) <= 0:
            is_valid = False
            flash('All fields required', 'register')
            return is_valid
        if int(len(results)) >= 1:
            flash('Email already in use', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid Email format', 'register')
            is_valid = False
        if int(len(data['first_name'])) < 3:
            flash('First name must be at least 3 characters', 'register')
            is_valid = False
        if int(len(data['last_name'])) < 3:
            flash('Last name must be at least 3 characters', 'register')
            is_valid = False
        if int(len(data['password'])) < 8:
            flash('Password must be at least 8 characters', 'register')
            is_valid = False
        if data['password'] != data['confirm']:
            flash('Passwords must match', 'register')
            is_valid = False
        return is_valid

    @classmethod
    def create_user(cls, data):
        query = '''
        INSERT INTO users (first_name, last_name, email, password)
        VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );
        '''
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        if results:
            return cls(results[0])

    @classmethod
    def user_games(cls, data):
        query = '''
        SELECT * FROM games
        LEFT JOIN users ON games.user_id = users.id
        WHERE games.user_id = %(id)s;
        '''
        results = connectToMySQL(cls.db).query_db(query, data)
        games = []
        for row in results:
            user_data = {
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            games = {
                'id': row['id'],
                'title': row['title'],
                'platform': row['platform'],
                'genre': row['genre'],
                'release_date': row['release_date'],
                'description': row['description'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'user_id': row['user_id'],
                'user': user_data
            }
            games.append(game)
        return games

    @classmethod
    def check_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])