from flask import Flask, redirect, render_template, session, flash, request
from mysqlconnection import MySQLConnector
import md5, re, os, binascii
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

app = Flask(__name__)
mysql = MySQLConnector(app, 'reddit')
app.secret_key = 'kittens'

def check_member(sub):
    info = None
    for char in sub[0]['list_subs']:
        if char == str(session['id']):
            query = "SELECT DATE_FORMAT(subscriptions.created_at, '%m/%d/%Y') as since FROM subscriptions " +\
                    "JOIN users ON subscriptions.user_id = users.id " +\
                    "WHERE users.id = :id;"
            data = {'id': session['id']}
            info = mysql.query_db(query, data)
            return info
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
    if 'id' in session:
        return redirect('/home')
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
    query = "SELECT COUNT(subscriptions.user_id) as num_subs, subreddits.url, subreddits.description FROM subscriptions " +\
            "JOIN subreddits ON subreddits.id = subscriptions.subreddit_id " +\
            "GROUP BY subscriptions.subreddit_id " +\
            "HAVING LOCATE(:id, GROUP_CONCAT(subscriptions.user_id SEPARATOR ', ')) = 0 " +\
            "ORDER BY num_subs DESC;"
    other_sub_reddits = mysql.query_db(query, data)
    return render_template('subscriptions.html', subscriptions=subscriptions, other_sub_reddits=other_sub_reddits)

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

@app.route('/r/<suburl>')
def subreddit(suburl):
    member = False
    ret = redirect('/home')
    data = {'url': 'r/'+suburl}
    query = "SELECT url, COUNT(subscriptions.user_id) as num_subs, date_format(subreddits.created_at, '%m/%d/%Y') as created, description, GROUP_CONCAT(subscriptions.user_id SEPARATOR ', ') as list_subs FROM subreddits " +\
            "JOIN subscriptions ON subreddits.id = subscriptions.subreddit_id " +\
            "WHERE url = :url GROUP BY subscriptions.subreddit_id;"
    sub = mysql.query_db(query, data)
    if len(sub) > 0:
        query = "SELECT posts.id AS id, posts.title AS title, posts.created_at AS posted, users.username AS user FROM posts " +\
            "JOIN users ON posts.user_id = users.id " +\
            "JOIN subreddits ON posts.subreddit_id = subreddits.id " +\
            "WHERE subreddits.url = :url;"
        posts = mysql.query_db(query, data)
        info = check_member(sub)
        ret = render_template('subreddit.html', sub=sub[0], member=member, posts=posts)
        if info:
            member = True
            ret = render_template('subreddit.html', sub=sub[0], member=member, info=info[0], posts=posts)
    return ret

@app.route('/r/<suburl>/<postid>')
def post(suburl, postid):
    query = "SELECT posts.title AS title, posts.text AS text, users.username AS op, " +\
            "DATE_FORMAT(posts.created_at, '%h:%i %p - %m/%d/%Y') AS posted, " +\
            "DATE_FORMAT(posts.updated_at, '%h:%i %p - %m/%d/%Y') AS edited FROM posts " +\
            "JOIN users ON posts.user_id = users.id " +\
            "WHERE posts.id = :id"
    data = {'id': postid}
    post = mysql.query_db(query, data)
    if len(post) > 0:
        data = {'url': 'r/'+suburl}
        query = "SELECT url, COUNT(subscriptions.user_id) as num_subs, date_format(subreddits.created_at, '%m/%d/%Y') as created, description, GROUP_CONCAT(subscriptions.user_id SEPARATOR ', ') as list_subs FROM subreddits " +\
            "JOIN subscriptions ON subreddits.id = subscriptions.subreddit_id " +\
            "WHERE url = :url GROUP BY subscriptions.subreddit_id;"
        sub = mysql.query_db(query, data)
        info = check_member(sub)
        member = False
        ret = render_template('post.html', post=post[0], sub=sub[0], member=member)
        if info:
            member = True
            ret = render_template('post.html', post=post[0], sub=sub[0], member=member, info=info[0])
        return ret
    else:
        url = '/r/' + suburl
        return redirect(url)

@app.route('/r/<suburl>/addpost', methods=['POST'])
def add_post(suburl):
    if 'id' not in session:
        return redirect('/')
    data = {
        'title': request.form['title'],
        'content': request.form['text'],
        'suburl': 'r/'+suburl,
        'userid': session['id']
    }
    valid = True
    if len(data['title']) < 1 or len(data['content']) < 1:
        flash("Post title and content may not be empty.", "Error:Post")
        valid = False
    if valid:
        # go get subid based on suburl
        query = "SELECT id FROM subreddits WHERE url = :suburl"
        sub_id = mysql.query_db(query, data)
        data['sub_id'] = sub_id[0]['id']
        # add that to data as sub_id, then insert post with that sub_id
        query = "INSERT INTO posts (text, user_id, subreddit_id, title, created_at, updated_at) " +\
                "VALUES (:content, :userid, :sub_id, :title, NOW(), NOW());"
        mysql.query_db(query, data)
    # go back to main page for that subreddit
    url = '/r/' + suburl
    return redirect(url)

@app.route('/r/<suburl>/subscribe')
def subscribe(suburl):
    if 'id' not in session:
        return redirect('/')
    query = "SELECT id FROM subreddits WHERE subreddits.url = :url"
    data = {'url': 'r/'+suburl}
    sub_id = mysql.query_db(query, data)
    if len(sub_id) > 0:
        query = "INSERT INTO subscriptions (user_id, subreddit_id, moderator, created_at, updated_at) " +\
                "VALUES (:user, :subreddit, 0, NOW(), NOW());"
        data = {
            'user': session['id'],
            'subreddit': sub_id[0]['id']
        }
        mysql.query_db(query, data)
        flash("You successfully subscribed!", "Success:Subscription")
        url = '/r/' + suburl
    return redirect(url)

@app.route('/r/<suburl>/unsubscribe')
def unsubscribe(suburl):
    if 'id' not in session:
        return redirect('/')
    query = "SELECT id FROM subreddits WHERE subreddits.url = :url"
    data = {'url': 'r/'+suburl}
    sub_id = mysql.query_db(query, data)
    if len(sub_id) > 0:
        query = "DELETE FROM subscriptions WHERE user_id = :user and subreddit_id = :subreddit"
        data = {
            'user': session['id'],
            'subreddit': sub_id[0]['id']
        }
        mysql.query_db(query, data)
        flash("You successfully unsubscribed!", "Success:Subscription")
        url = '/r/' + suburl
    return redirect(url)

@app.route('/messages/<username>')
def allMessages(username):
    query = 'SELECT authors.username AS author,messages.text AS message, DATE_FORMAT(messages.created_at, "%m/%d/%Y") AS time FROM messages JOIN users ON recipient_id = users.id JOIN users AS authors ON author_id = authors.id WHERE recipient_id = :user_id ORDER by messages.created_at DESC'
    data = {
        'user_id':session['id']
    }
    messages = mysql.query_db(query, data)
    return render_template('messages.html', messages = messages)

@app.route('/newMessage', methods=['POST'])
def newMessage():
    session.pop('dm')
    data = {
        'message': request.form['message'],
        'username': request.form['username'],
        'userid': session['id']
    }
    valid = True
    if len(data['message']) < 1 or len(data['username']) < 1:
        flash("Username and Message may not be empty.", "Error:DirectMessage")
        valid = False
        return redirect('/messages/'+session['username'])
    if valid:
        query = "SELECT id FROM users WHERE users.username = :username"
        recipient = mysql.query_db(query, data)
        if len(recipient) < 1:
            flash('Recipient user doesn\'t exist', 'Error:DirectMessage')
            return redirect('/messages/'+session['username']) 
        else: 
            data['recipient'] = recipient[0]['id']
            query = 'INSERT INTO messages(text, recipient_id, author_id, created_at, updated_at) VALUES(:message, :recipient, :userid, NOW(), NOW())'
            mysql.query_db(query, data)
            return redirect('/messages')

@app.route('/reply/<recipient>')
def reply(recipient):
    session['dm'] = recipient
    return redirect('/messages/'+session['username'])

@app.route('/logoff')
def logout():
    session.clear()
    return redirect('/')


app.run(debug=True)
