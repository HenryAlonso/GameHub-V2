from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Game:
    DB = "gamehub_db"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.platform = data['platform']
        self.genre = data['genre']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def retrieve_all(cls):
        query = """
                SELECT * FROM games
                LEFT JOIN users
                ON games.user_id = users.id
        """
        results = connectToMySQL(cls.DB).query_db(query)
        games = []
        for row in results:
            game = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "username" : row['username'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            game.creator = user.User(user_data)
            games.append(game)
        return games
        
    @classmethod
    def retrieve_by_id(cls, data):
        query = """
                SELECT * from games
                JOIN users
                ON games.user_id = users.id
                WHERE games.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return False
        result = results[0]
        this_game = cls(result)
        user_data = {
            "id": result['users.id'],
            "first_name": result['first_name'],
            "last_name": result['last_name'],
            "username": result['username'],
            "email": result['email'],
            "password": "",
            "created_at": result['users.created_at'],
            "updated_at": result['users.updated_at']
        }
        this_game.creator = user.User(user_data)
        return this_game
    
    @classmethod
    def new_game(cls, data):
        query = """
                INSERT INTO games 
                ( title, platform, genre, release_date, description, created_at, user_id )
                VALUES
                ( %(title)s, %(platform)s, %(genre)s, %(release_date)s, %(description)s, NOW(), %(user_id)s )
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        return results
    
    @classmethod
    def edit_game(cls, data):
        query = """
                UPDATE games
                # SET title = %(title)s, platform = %(platform)s, genre = %(genre)s, release_date = %(release_date)s, description = %(description)s, updated_at = NOW()
                WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        return results
    
    @classmethod
    def remove_game(cls, data):
        query = """
                DELETE FROM games
                WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        print("##########################")
        print(results)
        return results
    
    @staticmethod
    def validate_game_form(games):
        is_valid = True
        if not games.get('title') or not games.get('platform') or not games.get('genre') or not games.get('release_date') or not games.get('description'):
            flash("All fields required.", "games")
            is_valid = False
        if len(games['title']) < 1:
            flash("Title must contain at least 1 characters.", "games")
            is_valid = False
        if len(games['platform']) < 2:
            flash("Platform must contain at least 2 characters.", "games")
            is_valid = False
        if len(games['genre']) < 3:
            flash("Genre must be at least 3 characters.", "games")
            is_valid = False
        if not games['release_date']:
            flash("Release date is required. Please enter a date.", "games")
            is_valid = False
        if len(games['description']) < 20:
            flash("Description must be at least 20 characters.", "games")
            is_valid = False
        return is_valid
