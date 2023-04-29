from lexicon_legends.forms import SignInForm, SignUpForm, CreateRoom, JoinRoom
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request
from lexicon_legends.similarity import calculate_similarity
from lexicon_legends import app, db, bcrypt, socketio
from flask_socketio import join_room, leave_room
from lexicon_legends.models import User
import random


with open('lexicon_legends/static/data/words.txt') as file:
    words = [i for i in file.read().strip().split('\n')]
                           
                                                                                                
@app.route('/')
def welcome():
    return render_template('welcome.html')
                                                
                                                
@app.route('/about')
def about():
    return render_template('about.html')

rooms = {}

@app.route('/play', methods=['GET', 'POST'])
def play():
    form = JoinRoom()
    if form.validate_on_submit():
        room_key = form.key.data
        if room_key in rooms and len(rooms[room_key][0]) < 2:
            return redirect(url_for('game', room_key=room_key))
        else:
            form.key.errors.append('Invalid room key or room is full.')
    return render_template('play.html', form=form)


@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateRoom()
    if form.validate_on_submit():
        room_key = form.key.data
        random_word = random.choice(words)
        if room_key not in rooms:
            rooms[room_key] = [[], [random_word]]
            return redirect(url_for('game', room_key=room_key))
        else:
            form.key.errors.append('Room key already exists.')

    return render_template('create.html', form=form)


@app.route('/game/<room_key>')
def game(room_key):
    players = len(rooms[room_key][0])
    return render_template('game.html', room_key=room_key, players=players, word=rooms[room_key][1][0], current_user=current_user)


@socketio.on('join')
def on_join(data):
    room_key = data['room_key']
    join_room(room_key)
    rooms[room_key][0].append(request.sid)
    if len(rooms[room_key][0]) == 2:
        socketio.emit('start_game', room=room_key)


@socketio.on('leave')
def on_leave(data):
    room_key = data['room_key']
    leave_room(room_key)
    rooms[room_key][0].remove(request.sid)


@socketio.on('sync_timer')
def on_sync_timer(data):
    room_key = data['room_key']
    time = data['time']
    socketio.emit('update_timer', {'time': time}, room=room_key)

@socketio.on('send_word')
def on_send_word(data):
    room_key = data['room_key']
    word = data['word']
    sender = data['sender']
    socketio.emit('receive_word', {'word': word, 'sender': sender}, room=room_key)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', current_user=current_user)
                                                

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('create'))
                                                
    form = SignUpForm()
                                                    
    if request.method == 'POST' and form.validate_on_submit():
                                                
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
                                                
        return redirect(url_for('signin'))
                                                
                                                
    return render_template('signup.html', title='Sign Up', form=form)
                                                
                                                
@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('create'))
                                                
    form = SignInForm()
                                                
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('create'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
                                                
    return render_template('signin.html', title='Sign In', form=form)
                                                
                                                
@app.route("/signout")
def signout():
    logout_user()
    return redirect(url_for('signin'))
                                                
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            
                                                            