from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.game import Game

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    if 'game_data' in session:
        session.pop('game_data')
    user = User.get_user_by_id({"id": session['user_id']})
    users = User.get_all()
    return render_template("dashboard.html", user = user, games = Game.retrieve_all(), users = users)

@app.route('/new/game')
def add_game():
    if 'user_id' not in session:
        return redirect('/')
    if 'game_data' not in session:
        session['game_data'] = request.form
    user = User.get_user_by_id({"id": session['user_id']})
    return render_template("games_new.html", user = user, game=session['game_data'])


@app.route('/game/edit/<int:id>')
def edit_game(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_user_by_id({"id": session['user_id']})
    return render_template("games_edit.html", user = user, game = Game.retrieve_by_id({"id": id}))

@app.route('/show/<int:id>')
def show_game(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_user_by_id({"id": session['user_id']})
    return render_template("games_info.html", user = user, game = Game.retrieve_by_id({"id": id}))

@app.route('/new/game/process', methods = ["POST"])
def process_new_game():
    if 'user_id' not in session:
        return redirect('/')
    if not Game.validate_game_form(request.form):
        session['game_data'] = request.form
        return redirect('/new/game')
    data = {
        'user_id': session['user_id'],
        'title': request.form['title'],
        'platform': request.form['platform'],
        'genre': request.form['genre'],
        'release_date': request.form['release_date'],
        'description': request.form['description']
    }
    Game.new_game(data)
    return redirect('/dashboard')

@app.route('/game/update/process/<int:id>', methods = ["POST"])
def process_update(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Game.validate_game_form(request.form):
        return redirect(f'/game/edit/{id}')
    data = {
        'id': id,
        'title': request.form['title'],
        'platform': request.form['platform'],
        'genre': request.form['genre'],
        'release_date': request.form['release_date'],
        'description': request.form['description']
    }
    Game.edit_game(data)
    return redirect('/dashboard')
