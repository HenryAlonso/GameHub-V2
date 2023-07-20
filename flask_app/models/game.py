from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Game:
    db = 'gamehub_db'

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

    @classmethod
    def create_game(cls, data):
        query = '''
        INSERT INTO games (title, platform, genre, release_date, description, created_at, user_id)
        VALUES (%(title)s, %(platform)s, %(genre)s, %(release_date)s, %(description)s, NOW(), %(user_id)s);
        '''
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def validate_game(cls, data):
        is_valid = True
        if int(len(data['species'])) <= 0 or int(len(data['location'])) <= 0:
            is_valid = False
            flash('All fields required')
            return is_valid
        if len(data['species']) <3:
            flash('Species must be at least 3 characters')
            is_valid = False
        if len(data['location']) <3:
            flash('Location must be at least 3 characters')
            is_valid = False
        if int(len(data['reason'])) <=0:
            flash('Reason must not be blank')
            is_valid = False
        if not data['date']:
            flash('Date must not be blank')
            is_valid = False
        return is_valid

    @classmethod
    def get_all(cls):
        query = '''
        SELECT * FROM games
        LEFT JOIN users ON games.user_id = users.id;
        '''
        results = connectToMySQL(cls.db).query_db(query)
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
            game = {
                'id': row['id'],
                'species': row['species'],
                'location': row['location'],
                'reason': row['reason'],
                'date': row['date'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'user_id': row['user_id'],
                'user': user_data
            }
            games.append(game)
        return games

    @classmethod
    def get_one_game(cls, data):
        query = '''
        SELECT * FROM games
        LEFT JOIN users ON games.user_id = users.id
        WHERE games.id = %(id)s;
        '''
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            user_data = {
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            game = {
                'id': row['id'],
                'species': row['species'],
                'location': row['location'],
                'reason': row['reason'],
                'date': row['date'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'user_id': row['user_id'],
                'user': user_data
            }
        return game

    @classmethod
    def update_game(cls, data):
        query = '''
        UPDATE games SET species = %(species)s, location = %(location)s, reason = %(reason)s, date = %(date)s, updated_at = NOW()
        WHERE id = %(id)s;
        '''
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM games WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)