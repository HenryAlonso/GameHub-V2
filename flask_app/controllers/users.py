from flask import render_template, redirect, flash, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.game import Game
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/user/login')

@app.route('/user/login')
def login():
    if 'user_id' in session:
        return redirect('/dashboard')
    session.modified = True

    if not session:
        session['user_register_data'] = request.form
        session['user_data'] = request.form
    return render_template("index.html", user_register_data = session.get('user_register_data'), user_data = session.get('user_data'))

@app.route('/user/register/process', methods = ["POST"])
def create_user():
    if not User.validate_user_form(request.form):
        session['user_register_data'] = request.form
        return redirect('/')

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "username": request.form['username'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.add_user(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/user/login/process', methods = ["POST"])
def login_user():

    user = User.validate_user_login(request.form)
    if user:
        session['user_id'] = user.id
    
    if not user or 'user_id' not in session:
        session['user_data'] = request.form
        return redirect('/')
    
    return redirect('/dashboard')

@app.route('/user/update/process/<int:id>', methods = ["POST"])
def update_user(id) :
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id,
        'username' : request.form['username'],
        'age' : request.form['age'],
        'description' : request.form['description']
    }
    User.edit_user(data)
    return redirect('/dashboard')

@app.route('/user/account/<int:id>')
def account(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    
    return render_template("account.html", user = User.get_user_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/user/login')