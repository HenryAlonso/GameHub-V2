from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import game
import re
from flask import flash
from flask_app import bcrypt

EMAIL_REGEX =  re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "gamehub_db"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name= data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.birthday = data['birthday']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.games = []

    @classmethod
    def add_user(cls, data):
        query = """
                INSERT into users ( first_name, last_name, username, email, password )
                VALUES ( %(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s );
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        return results
    
    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM users;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user in results:
            users.append( cls(user))
        return users

    @classmethod
    def get_user_by_id(cls, data):
        query = """
                SELECT * FROM users WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        return cls(results[0])
    
    @classmethod
    def get_user_by_email(cls, data):
        query = """
                SELECT * FROM users WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_user_with_games(cls, data):
        query = """
                SELECT * FROM users
                LEFT JOIN games
                ON users.id = games.user_id
                WHERE users.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        user = cls(results[0])
        for row in results:
            game_data = {
                "id": row['games.id'],
                "title": row['games.title'],
                "platform": row['games.platform'],
                "genre": row['games.genre'],
                "release_date": row['games.release_date'],
                "description": row['games.description'],
                "created_at": row['games.created_at'],
                "updated_at": row['games.updated_at'],
                "user_id" : row['user_id']
            }
            user.games.append( game.Game(game_data))
        return user

    
    @staticmethod
    def validate_user_form(user):
        is_valid = True
        if not user.get('email') or not user.get('first_name') or not user.get('last_name') or not user.get('username') or not user.get('password') or not user.get('confirm'):
            flash("All fields are required.", "register")
            is_valid = False
        else:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL(User.DB).query_db(query, user)
            if len(results) >= 1:
                flash("Email already taken", "register")
                is_valid = False
            if not EMAIL_REGEX.match(user['email']):
                flash("Invalid email address.", "register")
                is_valid = False
            if not user['first_name'].isalpha():
                flash("First name must contain only alphabetic letters.", "register")
                is_valid = False
            elif len(user['first_name']) < 2:
                flash("First name must be at least 2 characters.", "register")
                is_valid = False
            if len(user['username']) < 3:
                flash("Username must be at least 3 characters.", "register")
                is_valid = False
            if not user['last_name'].isalpha():
                flash("Last name must contain only alphabetic letters.", "register")
                is_valid = False
            elif len(user['last_name']) < 2:
                flash("Last name must be at least 2 characters.", "register")
                is_valid = False
            if len(user['password']) < 8:
                flash("Password must contain at least 8 characters", "register")
                is_valid = False
            elif not re.search(r"\d", user['password']):
                flash("Password must contain at least one number", "register")
                is_valid = False
            elif not re.search(r"[A-Z]", user['password']):
                flash("Password must contain at least one uppercase letter", "register")
                is_valid = False
            if user['password'] != user['confirm']:
                flash("Passwords do not match", "register")
                is_valid = False
        return is_valid
    
    @staticmethod
    def validate_user_login(user_form):
        if not EMAIL_REGEX.match(user_form['email']):
            flash("Invalid email/password.", "login")
            return False
        user = User.get_user_by_email(user_form)
        if not user:
            flash("Invalid email/password", "login")
            return False
        if not bcrypt.check_password_hash(user.password, user_form['password']):
            flash("Invalid email/password", "login")
            return False
        return user