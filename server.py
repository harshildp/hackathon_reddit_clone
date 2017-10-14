from flask import Flask, redirect, render_template, session, flash, request
from mysqlconnection import MySQLConnector
import md5, re, os, binascii
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

app = Flask(__name__)
mysql = MySQLConnector(app, 'reddit')
app.secret_key = 'kittens'


def validation():
    error = False
    if len(request.form['email']) < 1:
        flash('Email cannot be blank', 'Error:Email')
        error = True
    elif not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid email address', 'Error:Email')
        error = True

    if len(request.form['username']) < 1:
        flash('Username cannot be blank', 'Error:Username')
        error = True
    elif len(request.form['username']) < 4:
        flash('Username must be at least 4 characters', 'Error:Username')
        error = True
    elif request.form['username'].isalnum() == False:
        flash('Invalid username. Alphanumeric characters only.', 'Error:Username')
        error = True

    if len(request.form['password']) < 1:
        flash('Password cannot be blank', 'Error:Password')
        error = True
    elif len(request.form['password']) < 8:
        flash('Password must be greater than 7 characters', 'Error:Password')
        error = True
    elif not PASSWORD_REGEX.match(request.form['password']):
        flash('Password must contain at least one lowercase, uppercase and digit',
              'Error:Password')
        error = True

    if len(request.form['cpassword']) < 1:
        flash('Password confirmation cannot be blank',
              'Error:PasswordConfirmation')
        error = True
    elif request.form['password'] != request.form['cpassword']:
        flash('Passwords don\'t match', 'Error:PasswordConfirmation')
        error = True

    return error != True

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if validation() == False:
        return redirect('/')
    else:
        data = {
            'email': request.form['email'],
            'username':request.form['username'],
            'salt': binascii.b2a_hex(os.urandom(15)),
        }
        data['password'] = md5.new(request.form['password'] + data['salt']).hexdigest()
        query = 'INSERT INTO users(username, email, salt, password, created_at, updated_at) VALUES(:username, :email, :salt, :password, NOW(), NOW())'
        new_id = mysql.query_db(query, data)
        session['username'] = data['username']
        session['id'] = new_id
        return redirect('/home')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    query = 'SELECT * FROM users where username = :username'
    data = {
        'username': username
    }
    user = mysql.query_db(query, data)

    if len(user) < 1:
        flash('Not a valid username / password', 'Error:LoginError')
        return redirect('/')
    else:
        if md5.new(password + user[0]['salt']).hexdigest() == user[0]['password']:
            session['username'] = user[0]['username']
            session['id'] = user[0]['id']
            return redirect('/home')
        else:
            flash('Not a valid username / password', 'Error:LoginError')
            return redirect('/')


@app.route('/home')
def home():
    query = "SELECT messages.text, users.username as name, date_format(messages.created_at, '%M %D, %Y %r') as time, " +\
            "messages.id FROM users JOIN messages ON messages.author_id = users.id ORDER BY messages.created_at DESC"
    messages = mysql.query_db(query)
    return render_template('home.html', messages=messages)

@app.route('/subscriptions')
def subscriptions():
    if 'id' not in session:
        return redirect('/')
    query = "SELECT subreddits.url, subreddits.description, DATE_FORMAT(subscriptions.updated_at, '%m/%d/%Y') as since, subscriptions.moderator FROM subscriptions " +\
            "JOIN subreddits on subreddits.id = subscriptions.subreddit_id " +\
            "WHERE subscriptions.user_id = :id"
    data = {'id': session['id']}
    subscriptions = mysql.query_db(query, data)
    print subscriptions
    return render_template('subscriptions.html', subscriptions=subscriptions)

@app.route('/subreddits/create')
def new_subreddit_page():
    if 'id' not in session:
        return redirect('/')
    return render_template('createsubreddit.html')

@app.route('/subreddits/generate', methods=['POST'])
def create_subreddit():
    if 'id' not in session:
        return redirect('/')
    ret = redirect('/subreddits/create')
    valid = True
    data = {
        'url': 'r/'+request.form['name'],
        'desc': request.form['description']
    }
    if len(data['url']) > 45:
        flash('Your subreddit name must be 43 characters or less.', 'Error:CreateSubError')
        valid = False
    if len(data['desc']) > 255:
        flash('Your subreddit description must be 255 characters or less.', 'Error:CreateSubError')
        valid = False
    if valid:
        query = "INSERT INTO subreddits (url, created_at, updated_at, description) " +\
                "VALUES (:url, NOW(), NOW(), :desc);"
        sub_id = mysql.query_db(query, data)
        query = "INSERT INTO subscriptions (user_id, subreddit_id, moderator, created_at, updated_at) " +\
                "VALUES (:user_id, :sub_id, 1, NOW(), NOW());"
        data = {
            'user_id': session['id'],
            'sub_id': sub_id
        }
        mysql.query_db(query, data)
        flash("You successfully created a new community!", "Success:CreateSub")
        ret = redirect('/subscriptions')
    return ret

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


app.run(debug=True)
