from flask import Flask, redirect, render_template, session, flash, request
from mysqlconnection import MySQLConnector
from collections import OrderedDict
import md5, re, os, binascii
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

app = Flask(__name__)
mysql = MySQLConnector(app, 'reddit')
app.secret_key = 'kittens'

def check_member(sub):
    if 'id' not in session:
        return None
    info = None
    for char in sub[0]['list_subs']:
        if char == str(session['id']):
            query = "SELECT DATE_FORMAT(subscriptions.created_at, '%m/%d/%Y') as since FROM subscriptions " +\
                    "JOIN users ON subscriptions.user_id = users.id " +\
                    "WHERE users.id = :id;"
            data = {'id': session['id']}
            info = mysql.query_db(query, data)
            return info

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"

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
    query = "SELECT posts.id AS id, SUM(IFNULL(post_votes.type, 0)) as net_votes, posts.title AS title, posts.updated_at AS posted, users.username AS user, subreddits.url AS suburl FROM posts " +\
            "JOIN users ON posts.user_id = users.id " +\
            "JOIN post_votes ON posts.id = post_votes.post_id " +\
            "JOIN subreddits ON posts.subreddit_id = subreddits.id " +\
            "GROUP BY posts.id " +\
            "ORDER BY net_votes DESC LIMIT 50;"
    posts = mysql.query_db(query)

    for i in posts:
        i['posted'] = pretty_date(i['posted'])
        
    return render_template('home.html', posts=posts)

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
    if ' '  in data['url']:
        flash("Your subreddit name may not contain spaces.", "Error:CreateSubError")
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

@app.route('/r/<suburl>/')
def subreddit(suburl):
    member = False
    ret = redirect('/home')
    data = {'url': 'r/'+suburl}
    query = "SELECT url, COUNT(subscriptions.user_id) as num_subs, subreddits.created_at as created, description, GROUP_CONCAT(subscriptions.user_id SEPARATOR ', ') as list_subs FROM subreddits " +\
            "JOIN subscriptions ON subreddits.id = subscriptions.subreddit_id " +\
            "WHERE url = :url GROUP BY subscriptions.subreddit_id;"
    sub = mysql.query_db(query, data)

    for i in sub:
        i['created'] = pretty_date(i['created'])

    if len(sub) > 0:
        query = "SELECT posts.id AS id, SUM(IFNULL(post_votes.type, 0)) as net_votes, posts.title AS title, posts.created_at AS posted, users.username AS user FROM posts " +\
            "JOIN users ON posts.user_id = users.id " +\
            "JOIN post_votes ON posts.id = post_votes.post_id " +\
            "JOIN subreddits ON posts.subreddit_id = subreddits.id " +\
            "WHERE subreddits.url = :url " +\
            "GROUP BY posts.id " +\
            "ORDER BY net_votes DESC LIMIT 50;"
        posts = mysql.query_db(query, data)

        for i in posts:
            i['posted'] = pretty_date(i['posted'])

        info = check_member(sub)
        ret = render_template('subreddit.html', sub=sub[0], member=member, posts=posts)
        if info:
            member = True
            ret = render_template('subreddit.html', sub=sub[0], member=member, info=info[0], posts=posts)
    return ret

@app.route('/r/<suburl>/<postid>/')
def post(suburl, postid):
    query = "SELECT users.id AS user_id, posts.id AS post_id, posts.title AS title, posts.text AS text, users.username AS op, " +\
            "posts.created_at AS posted, " +\
            "posts.updated_at AS edited, SUM(post_votes.type) AS net_votes FROM posts " +\
            "JOIN users ON posts.user_id = users.id " +\
            "JOIN post_votes on posts.id = post_votes.post_id " +\
            "WHERE posts.id = :id"
    data = {'id': postid}
    post = mysql.query_db(query, data)

    for x in post:
        x['edited'] = pretty_date(x['edited'])
        x['posted'] = pretty_date(x['posted'])
        
    if len(post) > 0:
        #check if they are mod
        query = "SELECT moderator FROM subscriptions JOIN subreddits ON subreddits.id = subscriptions.subreddit_id WHERE user_id = :userid and subreddits.url = :suburl;"
        data['userid'] = session['id']
        data['suburl'] = 'r/'+suburl
        mod = mysql.query_db(query, data)
        if len(mod) == 0:
            mod = [{'moderator': 0}]
        query = "SELECT users.username AS commenter, comments.text AS content, comments.id AS com_id,comments.created_at AS comment_time, " +\
                "comments.comment_id AS comment_on_id, SUM(IFNULL(comment_votes.type, 0)) AS net_votes FROM comments " +\
                "JOIN users ON comments.user_id = users.id " +\
                "JOIN comment_votes ON comments.id = comment_votes.comment_id " +\
                "WHERE comments.post_id = :id and comments.comment_id is NULL " +\
                "GROUP BY comments.id ORDER BY net_votes DESC"
        comments = mysql.query_db(query, data)
        query = "SELECT users.username AS commenter, comments.text AS content, comments.id AS com_id, comments.created_at AS comment_time, " +\
                "comments.comment_id AS comment_on_id, SUM(IFNULL(comment_votes.type, 0)) AS net_votes FROM comments " +\
                "JOIN users ON comments.user_id = users.id " +\
                "JOIN comment_votes ON comments.id = comment_votes.comment_id " +\
                "WHERE comments.post_id = :id and comments.comment_id > 0 " +\
                "GROUP BY comments.id ORDER BY net_votes DESC"
        replies = mysql.query_db(query, data)
        for c in comments:
            c['comment_time'] = pretty_date(c['comment_time'])
        for r in replies:
            r['comment_time'] = pretty_date(r['comment_time'])
        data = {'url': 'r/'+suburl}
        query = "SELECT url, COUNT(subscriptions.user_id) as num_subs, subreddits.created_at as created, description, GROUP_CONCAT(subscriptions.user_id SEPARATOR ', ') as list_subs FROM subreddits " +\
            "JOIN subscriptions ON subreddits.id = subscriptions.subreddit_id " +\
            "WHERE url = :url GROUP BY subscriptions.subreddit_id;"
        # making comments and replies into nested dictionary with children as dictionaries
        comment_list = []
        for idx, comment in enumerate(comments):
            comment_list.append(comment)
            for response in replies:
                if response['comment_on_id'] == comment['com_id']:
                    if 'children' not in comment:
                        comment['children'] = []
                    comment['children'].append(response)
                for response2 in replies:
                    if response2['comment_on_id'] == response['com_id']:
                        if 'children' not in response:
                            response['children'] = []
                        if response2 not in response['children']:
                            response['children'].append(response2)
        sub = mysql.query_db(query, data)
        for i in sub:
            i['created'] = pretty_date(i['created'])
        info = check_member(sub)
        member = False
        ret = render_template('post.html', post=post[0], sub=sub[0], member=member, comments=comments, comment_list=comment_list, mod=mod[0])
        if info:
            member = True
            ret = render_template('post.html', post=post[0], sub=sub[0], member=member, comments=comments, comment_list=comment_list, info=info[0], mod=mod[0])
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
        postid = mysql.query_db(query, data)
        # give post a default post_votes of zero
        query = "INSERT INTO post_votes (post_id, user_id, type, created_at, updated_at) " +\
                "VALUES (:postid, :userid, 0, NOW(), NOW())"
        data['postid'] = postid
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

@app.route('/r/<suburl>/<postid>/<updown>')
def vote(suburl, postid, updown):
    url = '/r/' + suburl + '/' + postid
    if 'id' not in session:
        return redirect(url)
    # check if user already voted on this post
    query = "SELECT user_id FROM post_votes WHERE post_id = :postid and user_id = :userid"
    data = {
        'postid': postid,
        'userid': session['id']
    }
    user = mysql.query_db(query, data)
    # using 1 for upvote, -1 for downvote, to make getting net easy
    if updown == "upvote":
        data['vote'] = 1
    elif updown == "downvote":
        data['vote'] = -1
    # if finds nothing, we can insert a vote
    if len(user) == 0:
        query = "INSERT INTO post_votes (post_id, user_id, type, created_at, updated_at) " +\
                "VALUES (:postid, :userid, :vote, NOW(), NOW())"
        mysql.query_db(query, data)
    # if vote already exists for this post and user, we need to update
    else:
        query = "UPDATE post_votes SET type = :vote WHERE user_id = :userid and post_id = :postid"
        mysql.query_db(query, data)
    # redirect to that post
    return redirect(url)

@app.route('/r/<suburl>/<postid>/addcomment', methods=['post'])
def add_comment(suburl, postid):
    url = '/r/' + suburl + '/' + postid
    if 'id' not in session:
        return redirect(url)
    data = {
        'content': request.form['text'],
        'postid': postid,
        'userid': session['id']
    }
    # verify comment is not empty
    if len(data['content']) < 1:
        flash("Comment may not be empty.", "Error:Comment")
    else:
        query = "INSERT INTO comments (text, user_id, post_id, created_at, updated_at) " +\
                "VALUES (:content, :userid, :postid, NOW(), NOW());"
        comment_id = mysql.query_db(query, data)
        # give that comment a default votes of zero
        query = "INSERT INTO comment_votes (user_id, comment_id, type, created_at, updated_at) " +\
                "VALUES (:userid, :commentid, 0, NOW(), NOW())"
        data['commentid'] = comment_id
        mysql.query_db(query, data)
    # go back to main page for that subreddit
    return redirect(url)

@app.route('/r/<suburl>/<postid>/<commentid>/<updown>')
def comment_vote(suburl, postid, commentid, updown):
    url = '/r/' + suburl + '/' + postid
    if 'id' not in session:
        return redirect(url)
    # check if user already voted on this comment
    query = "SELECT user_id FROM comment_votes WHERE comment_id = :commentid and user_id = :userid"
    data = {
        'commentid': commentid,
        'userid': session['id']
    }
    user = mysql.query_db(query, data)
    # using 1 for upvote, -1 for downvote, to make getting net easy
    if updown == "upvote":
        data['vote'] = 1
    elif updown == "downvote":
        data['vote'] = -1
    # if finds nothing, we can insert a vote
    if len(user) == 0:
        query = "INSERT INTO comment_votes (comment_id, user_id, type, created_at, updated_at) " +\
                "VALUES (:commentid, :userid, :vote, NOW(), NOW())"
        mysql.query_db(query, data)
    # if vote already exists for this post and user, we need to update
    else:
        query = "UPDATE comment_votes SET type = :vote WHERE user_id = :userid and comment_id = :commentid"
        mysql.query_db(query, data)
    # redirect to that post
    url = '/r/' + suburl + '/' + postid
    return redirect(url)

@app.route('/r/<suburl>/<postid>/<commentid>/reply', methods=['post'])
def comment_reply(suburl, postid, commentid):
    # send user back to post if they aren't logged in
    url = '/r/' + suburl + '/' + postid
    if 'id' not in session:
        return redirect(url)
    data = {
        'content': request.form['text'],
        'postid': postid,
        'commentid': commentid,
        'userid': session['id']
    }
    # verify comment is not empty
    if len(data['content']) < 1:
        flash("Comment may not be empty.", "Error:Reply")
    else:
        query = "INSERT INTO comments (text, user_id, post_id, created_at, updated_at, comment_id) " +\
                "VALUES (:content, :userid, :postid, NOW(), NOW(), :commentid);"
        comment_id = mysql.query_db(query, data)
        # give that comment a default votes of zero
        query = "INSERT INTO comment_votes (user_id, comment_id, type, created_at, updated_at) " +\
                "VALUES (:userid, :commentid, 0, NOW(), NOW())"
        data['commentid'] = comment_id
        mysql.query_db(query, data)
    # go back to main page for that subreddit
    return redirect(url)

@app.route('/messages/<username>')
def allMessages(username):
    query = 'SELECT authors.username AS author,messages.text AS message, messages.created_at AS time, messages.id as id FROM messages JOIN users ON recipient_id = users.id JOIN users AS authors ON author_id = authors.id WHERE recipient_id = :user_id ORDER by messages.created_at DESC'
    data = {
        'user_id':session['id']
    }
    messages = mysql.query_db(query, data)
    for message in messages:
        message['time'] = pretty_date(message['time'])
        
    return render_template('messages.html', messages = messages)

@app.route('/newMessage', methods=['POST'])
def newMessage():
    data = {
        'message': request.form['message'],
        'username': request.form['username'],
        'userid': session['id']
    }
    valid = True
    if len(data['message']) < 1 or len(data['username']) < 1:
        flash("Username and Message may not be empty.", "Error:DirectMessage")
        valid = False
    elif data['username'] == session['username']:
        flash('Why you talking to yourself?','Error:DirectMessage')
        valid = False
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
            return redirect('/messages/'+session['username'])
    else:
        return redirect('/messages/'+session['username'])

@app.route('/reply/<recipient>')
def reply(recipient):
    session['dm'] = recipient
    return redirect('/messages/'+session['username'])

@app.route('/delete/r/<url>/<post_id>')
def deletePost(url, post_id):
    queryComSel = 'SELECT comment_votes.comment_id as com_id from comment_votes JOIN comments on comment_votes.comment_id = comments.id WHERE post_id = :post_id'
    data = {
        'post_id': post_id
    }
    comvotes = mysql.query_db(queryComSel, data)
    print comvotes
    if len(comvotes) >= 1:
        comment_ids = []
        for i in range(len(comvotes)):
            comment_ids.append(comvotes[i]['com_id'])

        print comment_ids
        data = {
            'comment_id':comment_ids,
            'post_id': post_id        
        }
        print data
        querycomvotes = 'DELETE FROM comment_votes WHERE comment_id IN :comment_id'
        mysql.query_db(querycomvotes, data)
    query = 'DELETE FROM comments WHERE post_id = :post_id'
    mysql.query_db(query, data)
    queryVot = 'DELETE FROM post_votes WHERE post_id = :post_id'
    mysql.query_db(queryVot, data)
    queryDel =  'DELETE FROM posts WHERE posts.id = :post_id'
    mysql.query_db(queryDel, data)
    return redirect('/r/'+url)

@app.route('/newEdit/r/<url>/<post_id>/')
def editPost(url, post_id):
    query = 'SELECT * FROM posts where posts.id = :post_id'
    data = {
        'post_id':post_id
    }
    post = mysql.query_db(query,data)
    return render_template('edit.html', post = post[0], url = url)

@app.route('/edit/r/<url>/<post_id>', methods=['POST'])
def edit(url, post_id):
    query = 'UPDATE posts SET title = :title, text = :text, updated_at = NOW() WHERE posts.id = :post_id'
    data = {
        'title':request.form['title'],
        'text': request.form['text'],
        'post_id':post_id
    }
    mysql.query_db(query, data)
    return redirect('/r/'+ url)

@app.route('/deleteMessage/<mes_id>')
def deleteMessage(mes_id):
    query = 'DELETE from Messages where messages.id = :id'
    data = {
        'id':mes_id
    }
    mysql.query_db(query,data)
    return redirect('/messages/'+session['username'])

@app.route('/logoff')
def logout():
    session.clear()
    return redirect('/')

app.run(debug=True)